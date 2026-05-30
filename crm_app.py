# crm_app.py — PepperCRM

# Carrega .env ANTES de qualquer import — garante DATABASE_URL disponível
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import streamlit as st
from database import query

@st.cache_data(ttl=300, show_spinner=False)
def _nome_empresa():
    from configuracao import get_nome_empresa
    return get_nome_empresa()

st.set_page_config(page_title="PepperCRM", layout="wide")

if "pagina"         not in st.session_state: st.session_state["pagina"]         = "home"
if "id_selecionado" not in st.session_state: st.session_state["id_selecionado"] = None
# estado do módulo de pesquisa
if "pq_modo"        not in st.session_state: st.session_state["pq_modo"]        = "lista"


# Mapa de reset: ao navegar para uma página, estas chaves de session_state
# são resetadas para o valor padrão — garante que a aba principal seja exibida.
# Chaves intencionalmente definidas pelo caller (ex: ct_aba, pq_modo) NÃO entram aqui.
_RESET_ABAS = {
    "fornecedores":        {"forn_aba": "lista"},
    "produtos":            {"prod_aba": "lista"},
    "tabelas_preco":       {"tab_preco_aba": "lista"},
    "clientes":            {"cli_aba": "lista"},
    "comissoes":           {"com_aba": "cfg"},
    "relatorios":          {"rel_aba": "cli"},
    "visitas":             {"vis_aba": "prom", "vis_modo": "lista"},
    "mix_analise":         {"mix_aba": "pdv"},
    "metas":               {"mt_nav_aba": "painel", "def_aba": "fat"},
    "analise_competitiva": {"ana_aba": "mc"},
    "concorrentes":        {"cc_aba": "marcas"},
    "ver_pedidos":         {"vp_modo": "lista"},
    "configuracao":        {"cfg_aba": "sis"},
    "despesas":            {"desp_aba": "nova"},
    "catalogo":            {"cat_aba": "catalogo"},
}


def ir(p):
    """Navega para a página p, reseta abas do destino e sinaliza scroll ao topo."""
    st.session_state["pagina"] = p
    st.session_state["_scroll_topo"] = True
    # Reset das abas do módulo destino (não interfere com chaves do caller)
    for chave, default in _RESET_ABAS.get(p, {}).items():
        st.session_state[chave] = default
    st.rerun()


def _scroll_topo():
    """Rola para o topo — âncora HTML + scrollIntoView (funciona no mobile)."""
    if st.session_state.pop("_scroll_topo", False):
        import streamlit.components.v1 as components
        # Injeta âncora invisível no topo do iframe e usa scrollIntoView,
        # que respeita o viewport do mobile sem depender de window.parent.
        components.html("""
<div id="__pepper_topo" style="position:absolute;top:0;left:0;height:1px;width:1px;"></div>
<script>
(function(){
    // Tenta scrollIntoView no próprio iframe (funciona no mobile/Safari)
    var anchor = document.getElementById('__pepper_topo');
    if (anchor) { anchor.scrollIntoView({behavior:'instant',block:'start'}); }
    // Fallback: tenta também via window.parent para desktop
    try {
        var sels = [
            'section[data-testid="stMain"]',
            'section.main',
            '.main .block-container'
        ];
        for (var i=0; i<sels.length; i++){
            var el = window.parent.document.querySelector(sels[i]);
            if (el){ el.scrollTop = 0; break; }
        }
        window.parent.scrollTo(0,0);
    } catch(e){}
})();
</script>
""", height=0, scrolling=False)


@st.cache_data(ttl=120, show_spinner=False)
def _dados_dashboard_cache():
    """
    Coleta TODOS os dados do dashboard em uma única função cacheada (TTL 120s).
    Compatível com SQLite (local) e PostgreSQL (Railway/Supabase).
    """
    from datetime import date as _date
    hoje = _date.today().isoformat()
    mes_ini = _date.today().strftime("%Y-%m-01")

    def q1(sql, p=()):
        r = query(sql, p)
        return r[0][0] if r else 0

    # ── Pedidos do mês ────────────────────────────────────────────────────
    r = query("""SELECT COUNT(*), ROUND(COALESCE(SUM(
        (SELECT SUM(pi.quantidade*pi.preco_final*(1-COALESCE(p2.desconto_geral,0)/100.0))
         FROM pedido_item pi WHERE pi.pedido_id=p2.pedido_id
         AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO'))),0),2)
        FROM pedido p2 WHERE p2.status_pedido NOT IN ('CANCELADO','RECUSADO')
          AND p2.data_pedido >= ?""", (mes_ini,))
    qtd_mes   = r[0][0] if r else 0
    total_mes = float(r[0][1]) if r and r[0][1] else 0.0

    r2 = query("""SELECT ROUND(COALESCE(SUM(
        (SELECT SUM(pi.quantidade*pi.preco_final*(1-COALESCE(p2.desconto_geral,0)/100.0))
         FROM pedido_item pi WHERE pi.pedido_id=p2.pedido_id
         AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO'))
        * COALESCE(p2.comissao_percentual,COALESCE(com.percentual,0))/100.0),0),2)
        FROM pedido p2
        LEFT JOIN comissao com ON p2.fornecedor_id=com.fornecedor_id AND com.ativo=1
        WHERE p2.status_pedido='ENTREGUE'
          AND p2.data_pedido >= ?""", (mes_ini,))

    # ── Follow-ups vencidos e de hoje (sintaxe compatível SQLite+PG) ──────
    fups_v = query("""
        SELECT cr.contato_id, COALESCE(cli.nome_fantasia,'—'), cr.assunto,
               cr.data_followup, cr.prioridade
        FROM contato_registro cr
        LEFT JOIN cliente cli ON cr.cliente_id=cli.cliente_id
        WHERE cr.ativo!=0 AND cr.data_followup IS NOT NULL
          AND cr.status NOT IN ('Concluído','Cancelado','Proposta enviada')
          AND cr.data_followup < ?
        ORDER BY cr.data_followup""", (hoje,))

    fups_h = query("""
        SELECT cr.contato_id, COALESCE(cli.nome_fantasia,'—'),
               cr.assunto, cr.data_followup
        FROM contato_registro cr
        LEFT JOIN cliente cli ON cr.cliente_id=cli.cliente_id
        WHERE cr.ativo!=0 AND cr.data_followup IS NOT NULL
          AND cr.status NOT IN ('Concluído','Cancelado','Proposta enviada')
          AND cr.data_followup = ?
        ORDER BY cr.data_followup""", (hoje,))

    # ── Pedidos em aberto (lista para exibição) ───────────────────────────
    det_ped = query("""
        SELECT p.pedido_id, p.data_pedido, c.nome_fantasia,
               f.nome_fantasia, p.status_pedido
        FROM pedido p
        JOIN cliente c ON p.cliente_id=c.cliente_id
        JOIN fornecedor f ON p.fornecedor_id=f.fornecedor_id
        WHERE p.status_pedido IN ('ABERTO','ENVIADO')
        ORDER BY p.data_pedido DESC LIMIT 10""")

    # ── Alertas de oportunidade ────────────────────────────────────────────
    alertas = []

    neg_paradas = query("""
        SELECT COUNT(*), MIN(dias) FROM (
            SELECT cr.contato_id,
                   CAST(julianday('now') - julianday(
                       COALESCE(MAX(ci.data_interacao), cr.data_contato)
                   ) AS INTEGER) AS dias
            FROM contato_registro cr
            LEFT JOIN contato_interacao ci ON ci.contato_id=cr.contato_id AND ci.ativo!=0
            WHERE cr.ativo!=0 AND cr.tipo_topico='Negociação'
              AND cr.status NOT IN ('Concluído','Cancelado')
            GROUP BY cr.contato_id
            HAVING CAST(julianday('now') - julianday(
                       COALESCE(MAX(ci.data_interacao), cr.data_contato)
                   ) AS INTEGER) >= 15
        )""")
    if neg_paradas and neg_paradas[0][0]:
        qtd, min_dias = neg_paradas[0]
        alertas.append(("warn",
            f"🤝 **{qtd} negociação(ões) parada(s)** há mais de 15 dias "
            f"(a mais antiga há {min_dias} dias)", "contatos", "neg_parada"))

    sem_contato = query("""
        SELECT COUNT(*) FROM cliente c
        WHERE c.ativo!=0 AND c.status IN ('Visitado','Ativo')
          AND c.cliente_id NOT IN (
              SELECT DISTINCT cliente_id FROM contato_registro
              WHERE ativo!=0 AND cliente_id IS NOT NULL)""")
    if sem_contato and sem_contato[0][0]:
        alertas.append(("info",
            f"📋 **{sem_contato[0][0]} cliente(s) visitado(s)/ativo(s)** "
            f"sem nenhum contato registrado", "contatos", "sem_contato"))

    from datetime import timedelta as _td
    amanha      = (_date.today() + _td(days=1)).isoformat()
    depois      = (_date.today() + _td(days=2)).isoformat()
    tres_dias   = (_date.today() - _td(days=3)).isoformat()
    trinta_dias = (_date.today() - _td(days=30)).isoformat()
    sete_dias   = (_date.today() + _td(days=7)).isoformat()

    prox_fups = query("""
        SELECT COUNT(*) FROM contato_registro
        WHERE ativo!=0
          AND data_followup BETWEEN ? AND ?
          AND status NOT IN ('Concluído','Cancelado')""", (amanha, depois))
    if prox_fups and prox_fups[0][0]:
        alertas.append(("info",
            f"📅 **{prox_fups[0][0]} follow-up(s)** agendado(s) para "
            f"amanhã ou depois de amanhã", "contatos", "prox_fup"))

    pesq_rascu = query("""
        SELECT COUNT(*) FROM pesquisa_preco
        WHERE status='rascunho'
          AND data_pesquisa <= ?""", (tres_dias,))
    if pesq_rascu and pesq_rascu[0][0]:
        alertas.append(("warn",
            f"🔍 **{pesq_rascu[0][0]} pesquisa(s)** em rascunho há mais de 3 dias",
            "pesquisa", "pesq_rascu"))

    return {
        "qtd_abertos":           q1("SELECT COUNT(*) FROM pedido WHERE status_pedido IN ('ABERTO','ENVIADO')"),
        "qtd_mes":               qtd_mes,
        "total_mes":             total_mes,
        "comissao_mes":          float(r2[0][0]) if r2 and r2[0][0] else 0.0,
        "qtd_entregas":          q1("SELECT COUNT(*) FROM pedido WHERE data_entrega BETWEEN ? AND ? AND status_pedido NOT IN ('CANCELADO','RECUSADO','ENTREGUE','DEVOLVIDO')", (hoje, sete_dias)),
        "qtd_sem_pedido":        q1("SELECT COUNT(*) FROM cliente c WHERE c.ativo!=0 AND NOT EXISTS (SELECT 1 FROM pedido p WHERE p.cliente_id=c.cliente_id AND p.data_pedido >= ? AND p.status_pedido NOT IN ('CANCELADO','RECUSADO'))", (trinta_dias,)),
        "qtd_rupturas":          q1("SELECT COUNT(*) FROM pesquisa_preco_item pi JOIN pesquisa_preco pp ON pi.pesquisa_id=pp.pesquisa_id WHERE pi.ruptura=1 AND pp.data_pesquisa >= ?", (trinta_dias,)),
        "qtd_contatos_mes":      q1("SELECT COUNT(*) FROM contato_registro cr WHERE ativo!=0 AND cr.data_contato >= ?", (mes_ini,)),
        "qtd_negoc_abertas":     q1("SELECT COUNT(*) FROM contato_registro WHERE ativo!=0 AND tipo_topico='Negociação' AND status NOT IN ('Concluído','Cancelado')"),
        "qtd_clientes_contatados": q1("SELECT COUNT(DISTINCT cliente_id) FROM contato_registro WHERE ativo!=0 AND data_contato >= ? AND cliente_id IS NOT NULL", (trinta_dias,)),
        "qtd_pesquisas_mes":     q1("SELECT COUNT(*) FROM pesquisa_preco WHERE data_pesquisa >= ?", (mes_ini,)),
        "qtd_visitas_mes":       q1("SELECT COUNT(*) FROM visita_cliente WHERE data_visita >= ?", (mes_ini,)),
        "qtd_clientes_ativos":   q1("SELECT COUNT(*) FROM cliente WHERE status NOT IN ('Encerrado','Cancelado')"),
        "qtd_prospectos":        q1("SELECT COUNT(*) FROM cliente WHERE status='Prospecto'"),
        "fups_venc":             list(fups_v),
        "fups_hoje":             list(fups_h),
        "det_ped":               list(det_ped) if det_ped else [],
        "alertas":               alertas,
    }


def _dashboard():
    import pandas as pd
    from datetime import date as _date

    def brl(v):
        return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

    hoje     = _date.today()
    hoje_str = hoje.strftime("%d/%m/%Y")

    # ⚡ Tudo vem do cache único — zero queries extras nesta função
    _d                   = _dados_dashboard_cache()
    qtd_abertos          = _d["qtd_abertos"]
    qtd_mes              = _d["qtd_mes"]
    total_mes            = _d["total_mes"]
    comissao_mes         = _d["comissao_mes"]
    qtd_entregas         = _d["qtd_entregas"]
    qtd_sem_pedido       = _d["qtd_sem_pedido"]
    qtd_rupturas         = _d["qtd_rupturas"]
    qtd_contatos_mes     = _d["qtd_contatos_mes"]
    qtd_negoc_abertas    = _d["qtd_negoc_abertas"]
    qtd_clientes_contatados = _d["qtd_clientes_contatados"]
    qtd_pesquisas_mes    = _d["qtd_pesquisas_mes"]
    qtd_visitas_mes      = _d["qtd_visitas_mes"]
    qtd_clientes_ativos  = _d["qtd_clientes_ativos"]
    qtd_prospectos       = _d["qtd_prospectos"]
    fups_venc            = _d["fups_venc"]
    fups_hoje            = _d["fups_hoje"]
    det_ped              = _d["det_ped"]
    alertas              = _d["alertas"]
    total_venc           = len(fups_venc)
    total_hoje           = len(fups_hoje)

    # ═════════════════════════════════════════════════════════════════════
    # BLOCO 1 — ALERTAS URGENTES (sempre no topo, só aparece se houver)
    # ═════════════════════════════════════════════════════════════════════
    st.divider()
    tem_alerta = total_venc or total_hoje or qtd_entregas

    if total_venc:
        st.error(f"🔴 **{total_venc} follow-up(s) vencido(s)** — ação necessária agora!")
        with st.expander("👁️ Ver lista", expanded=False):
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
                                  width="stretch", type="primary"):
                    st.session_state["ct_aba"]           = "lista"
                    st.session_state["ct_topico_aberto"] = cid_fw
                    ir("contatos")

    if total_hoje:
        st.warning(f"📌 **{total_hoje} follow-up(s) para hoje**")
        with st.expander("👁️ Ver lista", expanded=False):
            for row in fups_hoje:
                cid_fh, entidade, assunto, prioridade = row
                col_e, col_a, col_btn = st.columns([2.5, 3.5, 1])
                col_e.write(f"**{entidade}**")
                col_a.caption(assunto[:55])
                if col_btn.button("Abrir", key=f"dfh_{cid_fh}",
                                  width="stretch"):
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
        if st.button("Ver contatos", key="da_ct", width="stretch"):
            ir("contatos")
    with col2:
        st.metric("Negociações abertas",  qtd_negoc_abertas,
                  help="Tópicos do tipo Negociação ainda não concluídos")
        if st.button("Ver negociações", key="da_neg", width="stretch"):
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
        if st.button("Ver visitas", key="da_vis", width="stretch"):
            ir("visitas")
    with col5:
        st.metric("Pesquisas de preço",   qtd_pesquisas_mes,
                  help="Pesquisas realizadas em PDVs no mês atual")
        if st.button("Ver pesquisas", key="da_pq", width="stretch"):
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
            if st.button("Ver pedidos", key="d_ab", width="stretch"):
                ir("ver_pedidos")
    with col2:
        st.metric("Pedidos este mês",  qtd_mes)
        st.caption(brl(total_mes))
    with col3:
        st.metric("Comissão do mês",   brl(comissao_mes))
        if st.button("Detalhar", key="d_com", width="stretch"):
            ir("comissoes")
    with col4:
        st.metric("Entregas em 7 dias", qtd_entregas)
        if qtd_entregas:
            if st.button("Ver", key="d_ent", width="stretch"):
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
        if st.button("📞 Ver e agir", key="d_fu", width="stretch"):
            ir("contatos")
    with col2:
        st.metric("Follow-ups hoje",     total_hoje)
        if total_hoje:
            if st.button("📌 Ver hoje", key="d_fh", width="stretch"):
                ir("contatos")
    with col3:
        st.metric("Sem pedido (30d)",    qtd_sem_pedido)
        if qtd_sem_pedido:
            if st.button("Ver oportunidades", key="d_sp", width="stretch"):
                ir("relatorios")
    with col4:
        st.metric("Rupturas (30d)",      qtd_rupturas)
        if qtd_rupturas:
            if st.button("Ver pesquisas", key="d_ru", width="stretch"):
                ir("pesquisa")

    # ─── Prospectos cadastrados ───────────────────────────────────────────
    if qtd_prospectos:
        st.info(f"🔵 **{qtd_prospectos} prospecto(s)** na carteira aguardando primeiro contato.")

    # ═════════════════════════════════════════════════════════════════════
    # BLOCO 5 — ALERTAS DE OPORTUNIDADE
    # ═════════════════════════════════════════════════════════════════════
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
                                        width="stretch"):
                    if link_a == "contatos":
                        st.session_state["ct_aba"] = "lista"
                    ir(link_a)



    if qtd_abertos > 0:
        st.divider()
        st.markdown("**Pedidos aguardando confirmacao**")
        if det_ped:
            st.dataframe(pd.DataFrame(det_ped,
                columns=["#","Data","Cliente","Fornecedor","Status"]),
                width="stretch", hide_index=True)


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
            if col4.button("Abrir", key=f"bg_cli_{cid}", width="stretch"):
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
            if col4.button("Abrir", key=f"bg_prod_{pid}", width="stretch"):
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
        WHERE cr.ativo!=0
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
            if col4.button("Abrir", key=f"bg_ct_{cid}", width="stretch"):
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
            if col5.button("Abrir", key=f"bg_ped_{pid}", width="stretch"):
                ir("ver_pedidos")

    if not encontrou:
        st.info(f"Nenhum resultado encontrado para: {t}")


if pagina == "home":
    col_t, col_b, col_c = st.columns([5, 1, 1])
    with col_t: st.title(f"{_nome_empresa()}")
    with col_b:
        st.write("")
        if st.button("🔍 Busca", width="stretch"): ir("busca_global")
    with col_c:
        st.write("")
        if st.button("⚙️ Config.", width="stretch"): ir("configuracao")
    _dashboard()
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Cadastros")
        if st.button("🏭 Fornecedores",     width="stretch"): ir("fornecedores")
        if st.button("📦 Produtos",         width="stretch"): ir("produtos")
        if st.button("💲 Tabelas de Preço", width="stretch"): ir("tabelas_preco")
        if st.button("👥 Clientes",         width="stretch"): ir("clientes")
        if st.button("📒 Catálogo",         width="stretch"): ir("catalogo")
    with col2:
        st.subheader("Comercial")
        if st.button("🧾 Novo Pedido",    width="stretch"): ir("pedido")
        if st.button("📊 Ver Pedidos",    width="stretch"): ir("ver_pedidos")
        if st.button("📈 Relatórios",     width="stretch"): ir("relatorios")
        if st.button("💰 Comissões",      width="stretch"): ir("comissoes")
        if st.button("📋 Visitas",        width="stretch"): ir("visitas")
        if st.button("🎯 Mix / Oferta",   width="stretch"): ir("mix_analise")
        if st.button("🔍 Pesquisa PDV",   width="stretch"):
            st.session_state["pq_modo"] = "lista"; ir("pesquisa")
        if st.button("🏷️ Concorrentes",   width="stretch"): ir("concorrentes")
        if st.button("📊 Inteligência Competitiva", width="stretch"): ir("analise_competitiva")
        if st.button("📞 Contatos & Negociações",   width="stretch"): ir("contatos")
        if st.button("🎯 Metas",                    width="stretch"): ir("metas")
        if st.button("💸 Despesas",                 width="stretch"): ir("despesas")


elif pagina == "configuracao":  from configuracao import tela_configuracao; tela_configuracao()
elif pagina == "fornecedores":  from cadastros import tela_fornecedores; tela_fornecedores()
elif pagina == "produtos":      from cadastros import tela_produtos; tela_produtos()
elif pagina == "tabelas_preco": from cadastros import tela_tabelas_preco; tela_tabelas_preco()
elif pagina == "clientes":      from cadastros import tela_clientes; tela_clientes()
elif pagina == "pedido":        from pedido import tela_novo_pedido; tela_novo_pedido()
elif pagina == "ver_pedidos":   from ver_pedidos import tela_ver_pedidos; tela_ver_pedidos()
elif pagina == "relatorios":    from relatorios import tela_relatorios; tela_relatorios()
elif pagina == "comissoes":     from comissoes import tela_comissoes; tela_comissoes()
elif pagina == "visitas":       from visitas import tela_visitas; tela_visitas()
elif pagina == "mix_analise":   from mix_analise import tela_mix_analise; tela_mix_analise()
elif pagina == "pesquisa":      from pesquisa import tela_pesquisa; tela_pesquisa()
elif pagina == "concorrentes":        from concorrentes import tela_concorrentes; tela_concorrentes()
elif pagina == "analise_competitiva": from analise_competitiva import tela_analise_competitiva; tela_analise_competitiva()
elif pagina == "contatos":            from contatos import tela_contatos; tela_contatos()
elif pagina == "metas":               from metas import tela_metas; tela_metas()
elif pagina == "catalogo":            from catalogo import tela_catalogo; tela_catalogo()
elif pagina == "despesas":            from despesas import tela_despesas; tela_despesas()
elif pagina == "busca_global":        _tela_busca_global()