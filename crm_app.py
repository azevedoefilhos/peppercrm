# crm_app.py — PepperCRM

import streamlit as st
from database import criar_tabelas, query
from cadastros import tela_fornecedores, tela_produtos, tela_tabelas_preco, tela_clientes
from pedido import tela_novo_pedido
from ver_pedidos import tela_ver_pedidos
from relatorios import tela_relatorios
from configuracao import tela_configuracao, get_nome_empresa
from comissoes import tela_comissoes
from visitas import tela_visitas
from mix_analise import tela_mix_analise
from pesquisa import tela_pesquisa
from concorrentes import tela_concorrentes
from analise_competitiva import tela_analise_competitiva
from contatos import tela_contatos, get_followups_vencidos, get_followups_hoje
from metas          import tela_metas
from contatos import tela_contatos, get_followups_vencidos, get_followups_hoje, get_negociacoes_urgentes

criar_tabelas()
_nome = get_nome_empresa()

st.set_page_config(page_title=_nome, page_icon="🌶", layout="wide")

if "pagina"         not in st.session_state: st.session_state["pagina"]         = "home"
if "id_selecionado" not in st.session_state: st.session_state["id_selecionado"] = None
# estado do módulo de pesquisa
if "pq_modo"        not in st.session_state: st.session_state["pq_modo"]        = "lista"


def ir(p):
    st.session_state["pagina"] = p
    st.session_state["_scroll_topo"] = True
    st.rerun()


def _scroll_topo():
    """Rola para o topo — injeta CSS anchor e JS via markdown."""
    if st.session_state.pop("_scroll_topo", False):
        import streamlit.components.v1 as components
        # Tenta múltiplos seletores para cobrir versões diferentes do Streamlit
        components.html("""
<script>
(function(){
    var sels = [
        'section[data-testid="stMain"]',
        'section.main',
        '.main .block-container',
        'section[data-testid="stAppViewContainer"] > div:first-child'
    ];
    for (var i=0; i<sels.length; i++){
        var el = window.parent.document.querySelector(sels[i]);
        if (el){ el.scrollTop = 0; break; }
    }
    window.parent.scrollTo(0,0);
})();
</script>
""", height=0, scrolling=False)


def _coletar_alertas_oportunidade():
    """Detecta proativamente situações que merecem atenção comercial."""
    alertas = []

    # 1. Negociação parada há mais de 15 dias sem nova interação
    neg_paradas = query("""
        SELECT COUNT(*), MIN(dias) FROM (
            SELECT cr.contato_id,
                   CAST(julianday('now') - julianday(
                       COALESCE(MAX(ci.data_interacao), cr.data_contato)
                   ) AS INTEGER) AS dias
            FROM contato_registro cr
            LEFT JOIN contato_interacao ci ON ci.contato_id=cr.contato_id AND ci.ativo=1
            WHERE cr.ativo=1 AND cr.tipo_topico='Negociação'
              AND cr.status NOT IN ('Concluído','Cancelado')
            GROUP BY cr.contato_id
            HAVING CAST(julianday('now') - julianday(
                       COALESCE(MAX(ci.data_interacao), cr.data_contato)
                   ) AS INTEGER) >= 15
        )""")
    if neg_paradas and neg_paradas[0][0]:
        qtd, min_dias = neg_paradas[0]
        alertas.append((
            "warn",
            f"🤝 **{qtd} negociação(ões) parada(s)** há mais de 15 dias sem interação "
            f"(a mais antiga há {min_dias} dias)",
            "contatos", "neg_parada"
        ))

    # 2. Clientes visitados mas nunca abordados sobre nenhum fornecedor
    sem_contato = query("""
        SELECT COUNT(*) FROM cliente c
        WHERE c.ativo=1 AND c.status IN ('Visitado','Ativo')
          AND c.cliente_id NOT IN (
              SELECT DISTINCT cliente_id FROM contato_registro
              WHERE ativo=1 AND cliente_id IS NOT NULL)""")
    if sem_contato and sem_contato[0][0]:
        qtd = sem_contato[0][0]
        alertas.append((
            "info",
            f"📋 **{qtd} cliente(s) visitado(s)/ativo(s)** sem nenhum contato registrado no app",
            "contatos", "sem_contato"
        ))

    # 3. Contatos com follow-up agendado para os próximos 2 dias
    prox_fups = query("""
        SELECT COUNT(*) FROM contato_registro
        WHERE ativo=1
          AND data_followup BETWEEN date('now','+1 day') AND date('now','+2 days')
          AND status NOT IN ('Concluído','Cancelado')""")
    if prox_fups and prox_fups[0][0]:
        qtd = prox_fups[0][0]
        alertas.append((
            "info",
            f"📅 **{qtd} follow-up(s)** agendado(s) para amanhã ou depois de amanhã",
            "contatos", "prox_fup"
        ))

    # 4. Pesquisas de preço sem finalizar há mais de 3 dias
    pesq_rascu = query("""
        SELECT COUNT(*) FROM pesquisa_preco
        WHERE status='rascunho'
          AND data_pesquisa <= date('now','-3 days')""")
    if pesq_rascu and pesq_rascu[0][0]:
        qtd = pesq_rascu[0][0]
        alertas.append((
            "warn",
            f"🔍 **{qtd} pesquisa(s) de preço** em rascunho há mais de 3 dias — finalizar ou descartar",
            "pesquisa", "pesq_rascu"
        ))

    return alertas


def _dashboard():
    import pandas as pd
    from datetime import date as _date, timedelta

    def brl(v):
        return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

    hoje     = _date.today()
    mes_ini  = hoje.strftime("%Y-%m-01")
    hoje_str = hoje.strftime("%d/%m/%Y")

    # ── Coleta todos os dados ─────────────────────────────────────────────
    def _q1(sql, p=()):
        r = query(sql, p); return r[0][0] if r else 0

    # Vendas
    qtd_abertos  = _q1("SELECT COUNT(*) FROM pedido WHERE status_pedido IN ('ABERTO','ENVIADO')")
    r = query("""SELECT COUNT(*), ROUND(COALESCE(SUM(
        (SELECT SUM(pi.quantidade*pi.preco_final*(1-COALESCE(p2.desconto_geral,0)/100.0))
         FROM pedido_item pi WHERE pi.pedido_id=p2.pedido_id
         AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO'))),0),2)
        FROM pedido p2 WHERE p2.status_pedido NOT IN ('CANCELADO','RECUSADO')
          AND p2.data_pedido >= date('now','start of month')""")
    qtd_mes, total_mes = (r[0][0], r[0][1]) if r else (0, 0.0)
    r2 = query("""SELECT ROUND(COALESCE(SUM(
        (SELECT SUM(pi.quantidade*pi.preco_final*(1-COALESCE(p2.desconto_geral,0)/100.0))
         FROM pedido_item pi WHERE pi.pedido_id=p2.pedido_id
         AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO'))
        * COALESCE(p2.comissao_percentual,COALESCE(com.percentual,0))/100.0),0),2)
        FROM pedido p2
        LEFT JOIN comissao com ON p2.fornecedor_id=com.fornecedor_id AND com.ativo=1
        WHERE p2.status_pedido='ENTREGUE'
          AND p2.data_pedido >= date('now','start of month')""")
    comissao_mes = r2[0][0] if r2 else 0.0
    qtd_entregas = _q1("SELECT COUNT(*) FROM pedido WHERE data_entrega BETWEEN date('now') AND date('now','+7 days') AND status_pedido NOT IN ('CANCELADO','RECUSADO','ENTREGUE','DEVOLVIDO')")
    qtd_sem_pedido = _q1("SELECT COUNT(*) FROM cliente c WHERE c.ativo=1 AND NOT EXISTS (SELECT 1 FROM pedido p WHERE p.cliente_id=c.cliente_id AND p.data_pedido >= date('now','-30 days') AND p.status_pedido NOT IN ('CANCELADO','RECUSADO'))")
    qtd_rupturas   = _q1("SELECT COUNT(*) FROM pesquisa_preco_item pi JOIN pesquisa_preco pp ON pi.pesquisa_id=pp.pesquisa_id WHERE pi.ruptura=1 AND pp.data_pesquisa >= date('now','-30 days')")

    # Atividade comercial — dados que JÁ existem no banco
    qtd_contatos_mes = _q1("""SELECT COUNT(*) FROM contato_registro
        WHERE ativo=1 AND data_contato >= date('now','start of month')""")
    qtd_negoc_abertas = _q1("""SELECT COUNT(*) FROM contato_registro
        WHERE ativo=1 AND tipo_topico='Negociação'
          AND status NOT IN ('Concluído','Cancelado')""")
    qtd_clientes_contatados = _q1("""SELECT COUNT(DISTINCT cliente_id)
        FROM contato_registro WHERE ativo=1
          AND data_contato >= date('now','-30 days')
          AND cliente_id IS NOT NULL""")
    qtd_pesquisas_mes = _q1("""SELECT COUNT(*) FROM pesquisa_preco
        WHERE data_pesquisa >= date('now','start of month')""")
    qtd_visitas_mes = _q1("""SELECT COUNT(*) FROM visita_cliente
        WHERE data_visita >= date('now','start of month')""")
    qtd_clientes_ativos = _q1("""SELECT COUNT(*) FROM cliente
        WHERE status NOT IN ('Encerrado','Cancelado')""")
    qtd_prospectos = _q1("SELECT COUNT(*) FROM cliente WHERE status='Prospecto'")

    # Follow-ups
    fups_venc = get_followups_vencidos()
    fups_hoje = get_followups_hoje()
    total_venc = len(fups_venc)
    total_hoje = len(fups_hoje)

    # ═════════════════════════════════════════════════════════════════════
    # BLOCO 1 — ALERTAS URGENTES (sempre no topo, só aparece se houver)
    # ═════════════════════════════════════════════════════════════════════
    st.divider()
    tem_alerta = total_venc or total_hoje or qtd_entregas

    if total_venc:
        st.error(f"🔴 **{total_venc} follow-up(s) vencido(s)** — ação necessária agora!")
        for row in fups_venc:
            cid_fw, entidade, assunto, data_fw, prioridade = row
            try:
                dias = (hoje - _date.fromisoformat(str(data_fw)[:10])).days
            except: dias = 0
            col_e, col_a, col_d, col_btn = st.columns([2.5, 3, 1.2, 1])
            col_e.write(f"**{entidade}**")
            col_a.caption(assunto[:55])
            col_d.caption(f"⏰ {dias}d")
            if col_btn.button("Abrir", key=f"dfv_{cid_fw}",
                              use_container_width=True, type="primary"):
                st.session_state["ct_aba"]           = "lista"
                st.session_state["ct_topico_aberto"] = cid_fw
                ir("contatos")

    if total_hoje:
        st.warning(f"📌 **{total_hoje} follow-up(s) para hoje**")
        for row in fups_hoje:
            cid_fh, entidade, assunto, prioridade = row
            col_e, col_a, col_btn = st.columns([2.5, 3.5, 1])
            col_e.write(f"**{entidade}**")
            col_a.caption(assunto[:55])
            if col_btn.button("Abrir", key=f"dfh_{cid_fh}",
                              use_container_width=True):
                st.session_state["ct_aba"]           = "lista"
                st.session_state["ct_topico_aberto"] = cid_fh
                ir("contatos")

    if qtd_entregas:
        st.warning(f"🚚 **{qtd_entregas} entrega(s) prevista(s) nos próximos 7 dias**")

    # ═════════════════════════════════════════════════════════════════════
    # BLOCO 2 — INDICADORES DE ATIVIDADE COMERCIAL
    # ═════════════════════════════════════════════════════════════════════
    st.caption(f"📅 Atividade comercial — {hoje_str}")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Contatos este mês",    qtd_contatos_mes,
                  help="Registros em Contatos & Negociações no mês atual")
        if st.button("Ver contatos", key="da_ct", use_container_width=True):
            ir("contatos")
    with col2:
        st.metric("Negociações abertas",  qtd_negoc_abertas,
                  help="Tópicos do tipo Negociação ainda não concluídos")
        if st.button("Ver negociações", key="da_neg", use_container_width=True):
            st.session_state["ct_aba"]  = "lista"
            st.session_state["fl_tipo"] = "Negociação"
            ir("contatos")
    with col3:
        st.metric("Clientes contatados",  qtd_clientes_contatados,
                  help="Clientes únicos com registro nos últimos 30 dias")
        st.caption(f"de {qtd_clientes_ativos} ativos")
    with col4:
        st.metric("Visitas este mês",     qtd_visitas_mes,
                  help="Visitas registradas no módulo de Visitas no mês atual")
        if st.button("Ver visitas", key="da_vis", use_container_width=True):
            ir("visitas")
    with col5:
        st.metric("Pesquisas de preço",   qtd_pesquisas_mes,
                  help="Pesquisas realizadas em PDVs no mês atual")
        if st.button("Ver pesquisas", key="da_pq", use_container_width=True):
            ir("pesquisa")

    # ─── Mini barra de progresso: clientes contatados ────────────────────
    if qtd_clientes_ativos > 0:
        pct = min(qtd_clientes_contatados / qtd_clientes_ativos, 1.0)
        st.progress(pct,
                    text=f"Cobertura de contato (30d): "
                         f"{min(qtd_clientes_contatados, qtd_clientes_ativos)}"
                         f"/{qtd_clientes_ativos} clientes "
                         f"({pct*100:.0f}%)")

    # ═════════════════════════════════════════════════════════════════════
    # BLOCO 3 — KPIs DE VENDAS
    # ═════════════════════════════════════════════════════════════════════
    st.divider()
    st.caption(f"💰 Vendas — {hoje_str}")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Pedidos em aberto", qtd_abertos)
        if qtd_abertos:
            if st.button("Ver pedidos", key="d_ab", use_container_width=True):
                ir("ver_pedidos")
    with col2:
        st.metric("Pedidos este mês",  qtd_mes)
        st.caption(brl(total_mes))
    with col3:
        st.metric("Comissão do mês",   brl(comissao_mes))
        if st.button("Detalhar", key="d_com", use_container_width=True):
            ir("comissoes")
    with col4:
        st.metric("Entregas em 7 dias", qtd_entregas)
        if qtd_entregas:
            if st.button("Ver", key="d_ent", use_container_width=True):
                ir("ver_pedidos")

    # ═════════════════════════════════════════════════════════════════════
    # BLOCO 4 — KPIs DE CAMPO
    # ═════════════════════════════════════════════════════════════════════
    st.divider()
    st.caption("🎯 Oportunidades e campo")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Follow-ups vencidos", total_venc,
                  delta=f"-{total_venc}" if total_venc else None,
                  delta_color="inverse")
        if st.button("📞 Ver e agir", key="d_fu", use_container_width=True):
            ir("contatos")
    with col2:
        st.metric("Follow-ups hoje",     total_hoje)
        if total_hoje:
            if st.button("📌 Ver hoje", key="d_fh", use_container_width=True):
                ir("contatos")
    with col3:
        st.metric("Sem pedido (30d)",    qtd_sem_pedido)
        if qtd_sem_pedido:
            if st.button("Ver oportunidades", key="d_sp", use_container_width=True):
                ir("relatorios")
    with col4:
        st.metric("Rupturas (30d)",      qtd_rupturas)
        if qtd_rupturas:
            if st.button("Ver pesquisas", key="d_ru", use_container_width=True):
                ir("pesquisa")

    # ─── Prospectos cadastrados ───────────────────────────────────────────
    if qtd_prospectos:
        st.info(f"🔵 **{qtd_prospectos} prospecto(s)** na carteira aguardando primeiro contato.")

    # ═════════════════════════════════════════════════════════════════════
    # BLOCO 5 — ALERTAS DE OPORTUNIDADE
    # ═════════════════════════════════════════════════════════════════════
    alertas = _coletar_alertas_oportunidade()
    if alertas:
        st.divider()
        st.caption("💡 Oportunidades detectadas")
        for alerta in alertas:
            tipo_a, msg_a, link_a, key_a = alerta
            col_msg, col_btn = st.columns([5, 1])
            with col_msg:
                if tipo_a == "warn":
                    st.warning(msg_a)
                else:
                    st.info(msg_a)
            with col_btn:
                if link_a and st.button("Ver", key=f"alerta_{key_a}",
                                        use_container_width=True):
                    if link_a == "contatos":
                        st.session_state["ct_aba"] = "lista"
                    ir(link_a)



    if qtd_abertos > 0:
        st.divider()
        st.markdown("**Pedidos aguardando confirmacao**")
        det_ped = query("""
            SELECT p.pedido_id, p.data_pedido, c.nome_fantasia,
                   f.nome_fantasia, p.status_pedido
            FROM pedido p
            JOIN cliente c ON p.cliente_id=c.cliente_id
            JOIN fornecedor f ON p.fornecedor_id=f.fornecedor_id
            WHERE p.status_pedido IN ('ABERTO','ENVIADO')
            ORDER BY p.data_pedido DESC LIMIT 10""")
        if det_ped:
            st.dataframe(pd.DataFrame(det_ped,
                columns=["#","Data","Cliente","Fornecedor","Status"]),
                use_container_width=True, hide_index=True)


pagina = st.session_state["pagina"]

_scroll_topo()

def _tela_busca_global():
    """Busca simultânea em clientes, produtos, contatos e pedidos."""
    from database import query
    st.header("🔍 Busca global")
    if st.button("⬅ Voltar"): ir("home")

    termo = st.text_input("",
                          placeholder="Digite nome de cliente, produto, assunto, código...",
                          key="bg_termo",
                          label_visibility="collapsed")

    if not termo or not termo.strip():
        st.caption("Digite ao menos 2 caracteres para buscar.")
        return

    t = termo.strip()
    if len(t) < 2:
        st.caption("Digite ao menos 2 caracteres.")
        return

    b = f"%{t}%"
    st.divider()
    encontrou = False

    # ── Clientes ─────────────────────────────────────────────────────────
    clientes = query("""
        SELECT cliente_id, nome_fantasia, status, cidade
        FROM cliente
        WHERE nome_fantasia LIKE ? OR razao_social LIKE ?
           OR cnpj LIKE ? OR cidade LIKE ?
        ORDER BY nome_fantasia LIMIT 10""", (b, b, b, b))
    if clientes:
        encontrou = True
        st.markdown("#### 👥 Clientes")
        for cid, nome, status, cidade in clientes:
            col1, col2, col3, col4 = st.columns([3, 1.5, 1.5, 1])
            col1.write(f"**{nome}**")
            col2.caption(status or "—")
            col3.caption(cidade or "—")
            if col4.button("Abrir", key=f"bg_cli_{cid}", use_container_width=True):
                ir("clientes")

    # ── Produtos ─────────────────────────────────────────────────────────
    produtos = query("""
        SELECT p.produto_id, p.descricao, p.codigo_produto,
               f.nome_fantasia, p.ativo
        FROM produto p
        LEFT JOIN fornecedor f ON p.fornecedor_id=f.fornecedor_id
        WHERE p.descricao LIKE ? OR p.descricao_curta LIKE ?
           OR p.codigo_produto LIKE ? OR p.ean LIKE ?
        ORDER BY p.descricao LIMIT 10""", (b, b, b, b))
    if produtos:
        encontrou = True
        st.markdown("#### 📦 Produtos")
        for pid, desc, cod, forn, ativo in produtos:
            col1, col2, col3, col4 = st.columns([3.5, 1.5, 2, 1])
            col1.write(f"**{desc}**" + ("" if ativo else " *(inativo)*"))
            col2.caption(cod or "—")
            col3.caption(forn or "—")
            if col4.button("Abrir", key=f"bg_prod_{pid}", use_container_width=True):
                ir("produtos")

    # ── Contatos & Negociações ────────────────────────────────────────────
    contatos = query("""
        SELECT cr.contato_id,
               cr.assunto, cr.status,
               COALESCE(cr.tipo_topico,'Contato'),
               COALESCE(c.nome_fantasia, f.nome_fantasia,'—') AS entidade
        FROM contato_registro cr
        LEFT JOIN cliente    c ON cr.cliente_id    = c.cliente_id
        LEFT JOIN fornecedor f ON cr.fornecedor_id = f.fornecedor_id
        WHERE cr.ativo=1
          AND (cr.assunto LIKE ? OR cr.descricao LIKE ?
               OR c.nome_fantasia LIKE ? OR f.nome_fantasia LIKE ?)
        ORDER BY cr.data_contato DESC LIMIT 10""", (b, b, b, b))
    if contatos:
        encontrou = True
        st.markdown("#### 📞 Contatos & Negociações")
        for cid, assunto, status, tipo, entidade in contatos:
            col1, col2, col3, col4 = st.columns([3, 1.5, 1.5, 1])
            col1.write(f"**{assunto[:55]}**")
            col2.caption(entidade[:25])
            col3.caption(f"{tipo} · {status}")
            if col4.button("Abrir", key=f"bg_ct_{cid}", use_container_width=True):
                st.session_state["ct_aba"]           = "lista"
                st.session_state["ct_topico_aberto"] = cid
                ir("contatos")

    # ── Pedidos ───────────────────────────────────────────────────────────
    pedidos = query("""
        SELECT p.pedido_id, p.data_pedido,
               c.nome_fantasia, f.nome_fantasia,
               p.status_pedido,
               p.nr_pedido_fornecedor
        FROM pedido p
        JOIN cliente    c ON p.cliente_id    = c.cliente_id
        JOIN fornecedor f ON p.fornecedor_id = f.fornecedor_id
        WHERE c.nome_fantasia LIKE ? OR p.nr_pedido_fornecedor LIKE ?
           OR f.nome_fantasia LIKE ?
        ORDER BY p.data_pedido DESC LIMIT 10""", (b, b, b))
    if pedidos:
        encontrou = True
        st.markdown("#### 🧾 Pedidos")
        for pid, data, cli, forn, status, num in pedidos:
            col1, col2, col3, col4, col5 = st.columns([2.5, 1.5, 1.5, 1.2, 1])
            col1.write(f"**{cli}**")
            col2.caption(forn[:20])
            col3.caption(data)
            col4.caption(status)
            if col5.button("Abrir", key=f"bg_ped_{pid}", use_container_width=True):
                ir("ver_pedidos")

    if not encontrou:
        st.info(f"Nenhum resultado encontrado para: {t}")


if pagina == "home":
    col_t, col_b, col_c = st.columns([5, 1, 1])
    with col_t: st.title(f"🌶 {_nome}")
    with col_b:
        st.write("")
        if st.button("🔍 Busca", use_container_width=True): ir("busca_global")
    with col_c:
        st.write("")
        if st.button("⚙️ Config.", use_container_width=True): ir("configuracao")
    _dashboard()
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Cadastros")
        if st.button("🏭 Fornecedores",     use_container_width=True): ir("fornecedores")
        if st.button("📦 Produtos",         use_container_width=True): ir("produtos")
        if st.button("💲 Tabelas de Preço", use_container_width=True): ir("tabelas_preco")
        if st.button("👥 Clientes",         use_container_width=True): ir("clientes")
    with col2:
        st.subheader("Comercial")
        if st.button("🧾 Novo Pedido",    use_container_width=True): ir("pedido")
        if st.button("📊 Ver Pedidos",    use_container_width=True): ir("ver_pedidos")
        if st.button("📈 Relatórios",     use_container_width=True): ir("relatorios")
        if st.button("💰 Comissões",      use_container_width=True): ir("comissoes")
        if st.button("📋 Visitas",        use_container_width=True): ir("visitas")
        if st.button("🎯 Mix / Oferta",   use_container_width=True): ir("mix_analise")
        if st.button("🔍 Pesquisa PDV",   use_container_width=True):
            st.session_state["pq_modo"] = "lista"; ir("pesquisa")
        if st.button("🏷️ Concorrentes",   use_container_width=True): ir("concorrentes")
        if st.button("📊 Inteligência Competitiva", use_container_width=True): ir("analise_competitiva")
        if st.button("📞 Contatos & Negociações",   use_container_width=True): ir("contatos")
        if st.button("🎯 Metas",                          use_container_width=True): ir("metas")


elif pagina == "configuracao":  tela_configuracao()
elif pagina == "fornecedores":  tela_fornecedores()
elif pagina == "produtos":      tela_produtos()
elif pagina == "tabelas_preco": tela_tabelas_preco()
elif pagina == "clientes":      tela_clientes()
elif pagina == "pedido":        tela_novo_pedido()
elif pagina == "ver_pedidos":   tela_ver_pedidos()
elif pagina == "relatorios":    tela_relatorios()
elif pagina == "comissoes":     tela_comissoes()
elif pagina == "visitas":       tela_visitas()
elif pagina == "mix_analise":   tela_mix_analise()
elif pagina == "pesquisa":      tela_pesquisa()
elif pagina == "concorrentes":        tela_concorrentes()
elif pagina == "analise_competitiva": tela_analise_competitiva()
elif pagina == "contatos":            tela_contatos()
elif pagina == "metas":               tela_metas()
elif pagina == "busca_global":        _tela_busca_global()