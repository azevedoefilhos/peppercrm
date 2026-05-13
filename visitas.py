# visitas.py -- PepperCRM
# Registro de visitas a clientes/PDVs com geolocalizacao e integracao com pesquisa de precos

import streamlit as st
import pandas as pd
import io
from datetime import date, datetime
from database import conectar, query


def _ir(p):
    st.session_state["pagina"] = p
    st.rerun()

def _brl(v):
    if v is None: return "—"
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

STATUS_FOLLOWUP = ["Pendente","Concluido","Cancelado"]
TIPOS_VISITA    = ["Prospeccao","Rotina","Cobranca","Entrega","Reuniao","Outro"]


def tela_visitas():
    st.header("Visitas a Clientes")

    modo = st.session_state.get("vis_modo", "lista")

    if modo == "lista":
        if st.button("Voltar ao menu"):
            _ir("home")
        _lista_visitas()

    elif modo == "nova":
        if st.button("Cancelar"):
            st.session_state["vis_modo"] = "lista"
            st.rerun()
        _form_nova_visita()

    elif modo == "roteiro":
        if st.button("Voltar a lista de visitas"):
            st.session_state["vis_modo"] = "lista"; st.rerun()
        _tela_roteiro()

    elif modo == "promotores":
        if st.button("Voltar a lista de visitas"):
            st.session_state["vis_modo"] = "lista"; st.rerun()
        _tela_promotores()

    elif modo == "detalhe":
        col1, col2 = st.columns([2,1])
        with col1:
            if st.button("Lista de visitas"):
                st.session_state["vis_modo"] = "lista"
                st.session_state.pop("vis_id", None)
                st.rerun()
        with col2:
            if st.button("Voltar ao menu", use_container_width=True):
                _ir("home")
        _tela_detalhe(st.session_state.get("vis_id"))

    else:
        st.session_state["vis_modo"] = "lista"
        st.rerun()


# ==============================================================
# LISTA DE VISITAS
# ==============================================================

def _lista_visitas():
    from database import _cache_clientes
    from datetime import date as _date, timedelta as _td

    col1, col2, col3, col4 = st.columns([2,1,1,1])
    with col2:
        if st.button("Nova visita", type="primary", use_container_width=True):
            st.session_state["vis_modo"] = "nova"
            st.rerun()
    with col3:
        if st.button("Roteiro", use_container_width=True):
            st.session_state["vis_modo"] = "roteiro"
            st.rerun()
    with col4:
        if st.button("Promotores", use_container_width=True):
            st.session_state["vis_modo"] = "promotores"
            st.rerun()

    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        clientes = [(None,"Todos os clientes")] + [(r[0],r[1]) for r in _cache_clientes()]
        fil_cli = st.selectbox("Cliente", clientes, format_func=lambda x: x[1], key="vis_fil_cli")
    with col2:
        fil_per = st.selectbox("Periodo", ["30 dias","60 dias","90 dias","Ano atual","Todos"],
                               key="vis_fil_per")
    with col3:
        fil_tipo = st.selectbox("Tipo de visita", ["Todos"] + TIPOS_VISITA, key="vis_fil_tipo")

    col4, col5, col6 = st.columns(3)
    with col4:
        fil_followup = st.selectbox("Follow-up", ["Todos","Pendente","Concluido","Cancelado"],
                                    key="vis_fil_fw")
    with col5:
        TIPOS_PDV_VIS = ["Todos","Supermercado","Hipermercado","Atacadista","Mini Mercado",
                         "Mercearia","Emporio","Sacolao","Hortifruti","Acougue","Casa de Carnes",
                         "Peixaria","Padaria","Confeitaria","Delicatessen","Hamburgueria",
                         "Restaurante","Lanchonete","Bar / Boteco","Clube / Associacao","Outro"]
        fil_tipo_pdv = st.selectbox("Tipo de PDV", TIPOS_PDV_VIS, key="vis_fil_tipo_pdv")
    with col6:
        fil_com_pesq = st.selectbox("Com pesquisa", ["Todos","Com pesquisa","Sem pesquisa"],
                                    key="vis_fil_pesq")

    hoje    = _date.today()
    ano_ini = hoje.strftime("%Y-01-01")
    where, params = ["1=1"], []
    if fil_cli[0]:
        where.append("v.cliente_id=?"); params.append(fil_cli[0])
    if fil_tipo != "Todos":
        where.append("v.local=?"); params.append(fil_tipo)
    if fil_followup != "Todos":
        where.append("v.proxima_acao IS NOT NULL")
    if fil_tipo_pdv != "Todos":
        where.append("pdv.tipo_pdv=?"); params.append(fil_tipo_pdv)
    if fil_com_pesq == "Com pesquisa":
        where.append("v.pesquisa_preco_id IS NOT NULL")
    elif fil_com_pesq == "Sem pesquisa":
        where.append("v.pesquisa_preco_id IS NULL")
    dias_map = {"30 dias":30,"60 dias":60,"90 dias":90}
    if fil_per in dias_map:
        where.append("v.data_visita >= ?")
        params.append((hoje - _td(days=dias_map[fil_per])).isoformat())
    elif fil_per == "Ano atual":
        where.append("v.data_visita >= ?"); params.append(ano_ini)

    visitas = query(f"""
        SELECT v.visita_id, v.data_visita,
               c.nome_fantasia,
               COALESCE(pdv.nome_loja,'Matriz') AS pdv,
               COALESCE(v.local,'—') AS tipo,
               v.contato, v.resumo,
               v.proxima_acao, v.data_followup,
               CASE WHEN v.latitude IS NOT NULL THEN 1 ELSE 0 END AS tem_gps,
               CASE WHEN v.pesquisa_preco_id IS NOT NULL THEN 1 ELSE 0 END AS tem_pesquisa,
               CASE WHEN v.pedido_id IS NOT NULL THEN 1 ELSE 0 END AS tem_pedido
        FROM visita_cliente v
        JOIN cliente c ON v.cliente_id=c.cliente_id
        LEFT JOIN pdv  ON v.pdv_id=pdv.pdv_id
        WHERE {' AND '.join(where)}
        ORDER BY v.data_visita DESC, v.visita_id DESC
    """, tuple(params))

    if not visitas:
        st.info("Nenhuma visita encontrada. Registre a primeira visita!")
        return

    # Metricas rapidas
    col1, col2, col3 = st.columns(3)
    col1.metric("Visitas no periodo", len(visitas))
    com_pesquisa = sum(1 for v in visitas if v[10])
    col2.metric("Com pesquisa de preco", com_pesquisa)
    followups = sum(1 for v in visitas if v[7])
    col3.metric("Com follow-up pendente", followups)

    st.divider()

    # Exportar
    col_exp, _ = st.columns([1,3])
    with col_exp:
        df_exp = pd.DataFrame([(
            v[1], v[2], v[3], v[4], v[5] or "—", v[6] or "—",
            v[7] or "—", v[8] or "—",
            "Sim" if v[9] else "Nao",
            "Sim" if v[10] else "Nao",
        ) for v in visitas],
        columns=["Data","Cliente","PDV","Tipo","Contato","Resumo",
                 "Prox.acao","Data followup","GPS","Pesquisa"])
        buf = io.BytesIO()
        df_exp.to_excel(buf, index=False, sheet_name="Visitas")
        buf.seek(0)
        st.download_button("Exportar Excel", data=buf, file_name="visitas.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)

    # Cabecalho da lista
    hc = st.columns([1.0, 2.5, 1.8, 1.2, 0.5, 0.5, 0.5, 0.8])
    for col, txt in zip(hc, ["Data","Cliente / PDV","Tipo / Contato","Follow-up","GPS","Pesq.","Ped.",""]):
        col.markdown(f"<small><b>{txt}</b></small>", unsafe_allow_html=True)

    for v in visitas:
        vid, data, cli, pdv, tipo, contato, resumo, prox, fw_data, gps, pesq, ped = v
        c = st.columns([1.0, 2.5, 1.8, 1.2, 0.5, 0.5, 0.5, 0.8])
        c[0].caption(data[:10] if data else "—")
        c[1].write(f"{cli} / {pdv}")
        c[2].caption(f"{tipo}  {('| ' + contato) if contato else ''}")
        c[3].caption(f"{prox[:20] + '...' if prox and len(prox)>20 else prox or '—'}")
        c[4].caption("📍" if gps else "—")
        c[5].caption("🔍" if pesq else "—")
        c[6].caption("📦" if ped else "—")
        with c[7]:
            if st.button("Ver", key=f"vis_ver_{vid}", use_container_width=True):
                st.session_state["vis_id"]  = vid
                st.session_state["vis_modo"] = "detalhe"
                st.rerun()


# ==============================================================
# NOVA VISITA
# ==============================================================

def _form_nova_visita():
    st.subheader("Registrar nova visita")

    # Geolocalizacao — entrada manual das coordenadas
    # (instrucao para pegar do Google Maps no celular)
    st.markdown("**Localizacao / Prova de presenca no PDV**")

    with st.expander("Como registrar minha localizacao no celular", expanded=False):
        st.markdown("""
**Opcao 1 — Google Maps (recomendado):**
1. Abra o Google Maps no celular
2. Pressione e segure no ponto exato do PDV ate aparecer o pin vermelho
3. Toque no endereco que aparece na parte de baixo
4. Role ate ver as coordenadas (ex: -23.9876, -46.3456)
5. Copie e cole nos campos abaixo

**Opcao 2 — WhatsApp:**
Envie sua localizacao atual pelo WhatsApp para si mesmo,
abra no computador e copie as coordenadas da URL do mapa.

**Opcao 3 — URL do navegador:**
No celular, abra maps.google.com, navegue ate o PDV,
as coordenadas aparecem na URL apos o simbolo @
        """)

    col_geo1, col_geo2 = st.columns(2)
    with col_geo1:
        lat_manual = st.number_input("Latitude",
                                     value=0.0, format="%.6f", key="vis_lat",
                                     help="Ex: -23.987654  (negativo para Sul)")
        lng_manual = st.number_input("Longitude",
                                     value=0.0, format="%.6f", key="vis_lng",
                                     help="Ex: -46.345678  (negativo para Oeste)")
    with col_geo2:
        endereco_gps = st.text_input("Endereco / referencia do local", key="vis_end_gps",
                                     placeholder="Ex: Av. Brasil 1200, Jardim Real, Praia Grande SP")
        if lat_manual != 0.0 and lng_manual != 0.0:
            maps_url = f"https://www.google.com/maps?q={lat_manual},{lng_manual}"
            st.markdown(f"Preview: [Ver no Google Maps]({maps_url})")
            st.caption(f"Lat: {lat_manual:.5f} | Lng: {lng_manual:.5f}")
        else:
            st.caption("Preencha latitude e longitude para ver o link de verificacao")

    st.divider()

    # Dados da visita
    col1, col2 = st.columns(2)
    with col1:
        clientes = query("SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo=1 ORDER BY nome_fantasia")
        if not clientes:
            st.warning("Nenhum cliente cadastrado."); return
        cli_sel  = st.selectbox("Cliente *", clientes, format_func=lambda x: x[1], key="vis_cli")
        cli_id   = cli_sel[0]

        pdvs = query("""SELECT pdv_id, nome_loja, cidade FROM pdv
            WHERE cliente_id=? AND ativo=1 ORDER BY nome_loja""", (cli_id,))
        pdv_opts = [(None,"— Visita na matriz/sem PDV")] + [(p[0],f"{p[1]} ({p[2] or ''})") for p in pdvs]
        pdv_sel  = st.selectbox("PDV", pdv_opts, format_func=lambda x: x[1], key="vis_pdv")
        pdv_id   = pdv_sel[0]

        data_vis = st.date_input("Data da visita *", value=date.today(), key="vis_data")
        tipo_vis = st.selectbox("Tipo de visita", TIPOS_VISITA, key="vis_tipo")
        duracao  = st.number_input("Duracao (minutos)", min_value=0, value=30, step=15,
                                   key="vis_dur")

    with col2:
        contato  = st.text_input("Contato (nome/cargo)", key="vis_contato",
                                 placeholder="Ex: Joao Silva — Gerente")
        resumo   = st.text_area("Resumo da visita *", height=100, key="vis_resumo",
                                placeholder="O que foi discutido, produtos apresentados...")
        prods    = st.text_input("Produtos tratados", key="vis_prods",
                                 placeholder="Ex: Vinagre Maca 500ml, Vinagre Arroz 750ml")
        prox_acao = st.text_input("Proxima acao / follow-up", key="vis_prox",
                                  placeholder="Ex: Enviar tabela de precos atualizada")
        fw_data  = st.date_input("Data do follow-up", value=None, key="vis_fw_data")

    st.divider()

    # Vinculo com pesquisa de precos
    st.markdown("**Vincular pesquisa de precos realizada nesta visita**")
    pesquisas_disp = query("""
        SELECT pp.pesquisa_id, pp.data_pesquisa, f.nome_fantasia, pp.status
        FROM pesquisa_preco pp
        JOIN fornecedor f ON pp.fornecedor_id=f.fornecedor_id
        WHERE (pp.cliente_id=? OR pp.pdv_id=?)
          AND pp.data_pesquisa LIKE ?
        ORDER BY pp.pesquisa_id DESC
    """, (cli_id, pdv_id or 0, f"{data_vis}%"))

    pesq_opts = [(None,"— Sem pesquisa vinculada")] + [
        (p[0], f"#{p[0]} {p[1][:10]} | {p[2]} | {p[3]}") for p in pesquisas_disp]
    pesq_sel = st.selectbox("Pesquisa de precos do dia",
                            pesq_opts, format_func=lambda x: x[1],
                            key="vis_pesq_id")
    pesq_id = pesq_sel[0]

    # Vinculo com pedido
    pedidos_disp = query("""
        SELECT p.pedido_id, p.data_pedido, f.nome_fantasia, p.status_pedido
        FROM pedido p
        JOIN fornecedor f ON p.fornecedor_id=f.fornecedor_id
        WHERE p.cliente_id=? AND p.data_pedido LIKE ?
        ORDER BY p.pedido_id DESC
    """, (cli_id, f"{data_vis}%"))

    ped_opts = [(None,"— Sem pedido vinculado")] + [
        (p[0], f"#{p[0]} {p[1][:10]} | {p[2]} | {p[3]}") for p in pedidos_disp]
    ped_sel = st.selectbox("Pedido realizado nesta visita",
                           ped_opts, format_func=lambda x: x[1],
                           key="vis_ped_id")
    ped_id = ped_sel[0]

    obs = st.text_area("Observacoes adicionais", height=60, key="vis_obs")

    st.divider()
    if st.button("Registrar visita", type="primary", use_container_width=True):
        if not resumo.strip():
            st.error("O resumo da visita e obrigatorio."); return

        lat  = float(lat_manual) if lat_manual and lat_manual != 0.0 else None
        lng  = float(lng_manual) if lng_manual and lng_manual != 0.0 else None

        conn = conectar()
        conn.execute("""
            INSERT INTO visita_cliente
            (cliente_id, pdv_id, local, data_visita, contato, resumo,
             produtos_tratados, pedido_id, pesquisa_preco_id,
             proxima_acao, data_followup, observacao,
             latitude, longitude, endereco_gps, duracao_minutos)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (cli_id, pdv_id, tipo_vis, str(data_vis), contato or None,
              resumo.strip(), prods or None, ped_id, pesq_id,
              prox_acao or None,
              str(fw_data) if fw_data else None,
              obs or None, lat, lng,
              endereco_gps or None, duracao or None))
        conn.commit(); conn.close()
        st.success("Visita registrada com sucesso!")
        st.session_state["vis_modo"] = "lista"
        st.rerun()


# ==============================================================
# DETALHE DA VISITA
# ==============================================================

def _tela_detalhe(vis_id):
    if not vis_id:
        st.info("Selecione uma visita."); return

    v = query("""
        SELECT v.visita_id, v.data_visita, c.nome_fantasia,
               COALESCE(pdv.nome_loja,'Matriz') AS pdv,
               COALESCE(pdv.cidade, c.cidade,'') AS cidade,
               COALESCE(v.local,'—') AS tipo, v.contato,
               v.resumo, v.produtos_tratados,
               v.proxima_acao, v.data_followup, v.observacao,
               v.latitude, v.longitude, v.endereco_gps,
               v.duracao_minutos, v.pesquisa_preco_id, v.pedido_id
        FROM visita_cliente v
        JOIN cliente c ON v.cliente_id=c.cliente_id
        LEFT JOIN pdv  ON v.pdv_id=pdv.pdv_id
        WHERE v.visita_id=?
    """, (vis_id,))

    if not v: st.error("Visita nao encontrada."); return
    (vid, data, cli, pdv, cidade, tipo, contato,
     resumo, prods, prox, fw_data, obs,
     lat, lng, end_gps, duracao, pesq_id, ped_id) = v[0]

    # Cabecalho
    st.subheader(f"Visita #{vid}")
    col1, col2 = st.columns([3,1])
    with col1:
        st.markdown(f"**{cli}**  |  {pdv}  —  {cidade}")
        st.caption(
            f"Data: {data[:10] if data else '—'}  "
            f"| Tipo: {tipo}  "
            f"| Duracao: {duracao or '—'} min  "
            f"| Contato: {contato or '—'}"
        )
    with col2:
        # GPS badge
        if lat and lng:
            maps_url = f"https://www.google.com/maps?q={lat},{lng}"
            st.markdown(f"[Ver no Google Maps]({maps_url})")
            st.caption(f"Lat: {lat:.5f}\nLng: {lng:.5f}")
        else:
            st.caption("Sem GPS registrado")

    st.divider()

    # Conteudo
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Resumo da visita**")
        st.write(resumo or "—")
        if prods:
            st.markdown("**Produtos tratados**")
            st.caption(prods)
        if obs:
            st.markdown("**Observacoes**")
            st.caption(obs)
    with col2:
        if prox or fw_data:
            st.markdown("**Follow-up**")
            st.info(f"**Proxima acao:** {prox or '—'}\n\n**Data:** {fw_data[:10] if fw_data else '—'}")
        if end_gps:
            st.markdown("**Local registrado**")
            st.caption(end_gps)

    st.divider()

    # Vinculos
    col1, col2 = st.columns(2)
    with col1:
        if pesq_id:
            pq = query("""SELECT pp.data_pesquisa, f.nome_fantasia, pp.status
                FROM pesquisa_preco pp JOIN fornecedor f ON pp.fornecedor_id=f.fornecedor_id
                WHERE pp.pesquisa_id=?""", (pesq_id,))
            if pq:
                st.markdown("**Pesquisa de precos vinculada**")
                st.success(f"#{pesq_id} — {pq[0][0][:10]} | {pq[0][1]} | {pq[0][2]}")
                if st.button("Abrir pesquisa", key=f"abrir_pesq_{vid}"):
                    st.session_state["pq_id"]   = pesq_id
                    st.session_state["pq_modo"] = "detalhe"
                    _ir("pesquisa")
    with col2:
        if ped_id:
            ped = query("""SELECT p.data_pedido, f.nome_fantasia, p.status_pedido
                FROM pedido p JOIN fornecedor f ON p.fornecedor_id=f.fornecedor_id
                WHERE p.pedido_id=?""", (ped_id,))
            if ped:
                st.markdown("**Pedido vinculado**")
                st.success(f"#{ped_id} — {ped[0][0][:10]} | {ped[0][1]} | {ped[0][2]}")
                if st.button("Abrir pedido", key=f"abrir_ped_{vid}"):
                    st.session_state["pedido_ativo_id"] = ped_id
                    st.session_state["vp_modo"] = "detalhe"
                    _ir("ver_pedidos")

    st.divider()

    # Edicao rapida de follow-up
    with st.expander("Editar follow-up / observacoes"):
        with st.form(f"edit_vis_{vid}"):
            novo_prox  = st.text_input("Proxima acao", value=prox or "")
            novo_fw    = st.date_input("Data follow-up",
                                       value=date.fromisoformat(fw_data[:10]) if fw_data else None)
            novo_obs   = st.text_area("Observacoes", value=obs or "")
            if st.form_submit_button("Salvar", type="primary"):
                conn = conectar()
                conn.execute("""UPDATE visita_cliente SET
                    proxima_acao=?, data_followup=?, observacao=?
                    WHERE visita_id=?""",
                    (novo_prox or None,
                     str(novo_fw) if novo_fw else None,
                     novo_obs or None, vid))
                conn.commit(); conn.close()
                st.success("Atualizado!"); st.rerun()

    # Excluir visita
    with st.expander("Excluir visita"):
        st.warning("Esta acao nao pode ser desfeita.")
        if st.button("Confirmar exclusao", type="primary", key=f"del_vis_{vid}"):
            conn = conectar()
            conn.execute("DELETE FROM visita_cliente WHERE visita_id=?", (vid,))
            conn.commit(); conn.close()
            st.session_state["vis_modo"] = "lista"
            st.session_state.pop("vis_id", None)
            st.success("Visita excluida."); st.rerun()


# ==============================================================
# ROTEIRO DE VISITAS
# ==============================================================

def _tela_roteiro():
    st.header("Roteiro de Visitas")
    st.caption("Organize os PDVs por dia da semana e planeje a ordem otimizada de visitas.")

    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        dias = ["Todos","Segunda","Terca","Quarta","Quinta","Sexta","Sabado","Flexivel"]
        fil_dia  = st.selectbox("Dia da semana", dias, key="rot_dia")
    with col2:
        freqs = ["Todas","Semanal","Quinzenal","Mensal","Bimestral","Sob demanda"]
        fil_freq = st.selectbox("Frequencia", freqs, key="rot_freq")
    with col3:
        clientes = [(None,"Todos os clientes")] + [
            (r[0],r[1]) for r in query(
                "SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo=1 ORDER BY nome_fantasia")]
        fil_cli  = st.selectbox("Cliente", clientes, format_func=lambda x: x[1], key="rot_cli")

    where, params = ["p.ativo=1"], []
    if fil_dia != "Todos":
        where.append("p.dia_visita=?"); params.append(fil_dia)
    if fil_freq != "Todas":
        where.append("p.frequencia_visita=?"); params.append(fil_freq)
    if fil_cli[0]:
        where.append("p.cliente_id=?"); params.append(fil_cli[0])

    pdvs = query(f"""
        SELECT p.pdv_id, c.nome_fantasia, p.nome_loja,
               COALESCE(p.tipo_pdv,'—')        AS tipo,
               COALESCE(p.dia_visita,'—')       AS dia,
               COALESCE(p.frequencia_visita,'—') AS freq,
               COALESCE(p.endereco,'')          AS end,
               COALESCE(p.bairro,'')            AS bairro,
               COALESCE(p.cidade,'')            AS cidade,
               p.gerente,
               p.horario_recebimento,
               COALESCE(p.ordem_roteiro, 999)   AS ordem,
               p.latitude, p.longitude
        FROM pdv p
        JOIN cliente c ON p.cliente_id=c.cliente_id
        WHERE {' AND '.join(where)}
        ORDER BY p.ordem_roteiro NULLS LAST, p.dia_visita, c.nome_fantasia, p.nome_loja
    """, tuple(params))

    if not pdvs:
        st.info("Nenhum PDV encontrado para os filtros selecionados.")
        st.caption("Dica: cadastre o dia de visita nos PDVs em Clientes -> PDVs -> Editar.")
        return

    # Metricas
    col1, col2, col3 = st.columns(3)
    col1.metric("PDVs no roteiro", len(pdvs))
    com_coord = sum(1 for p in pdvs if p[12] and p[13])
    col2.metric("Com localizacao GPS", com_coord)
    dias_unicos = len(set(p[4] for p in pdvs if p[4] != "—"))
    col3.metric("Dias de cobertura", dias_unicos)

    st.divider()

    # Agrupado por dia
    if fil_dia == "Todos":
        ordem_dias = ["Segunda","Terca","Quarta","Quinta","Sexta","Sabado","Flexivel","—"]
        dias_presentes = sorted(set(p[4] for p in pdvs),
                                key=lambda d: ordem_dias.index(d) if d in ordem_dias else 99)
    else:
        dias_presentes = [fil_dia]

    for dia in dias_presentes:
        pdvs_dia = [p for p in pdvs if p[4] == dia]
        if not pdvs_dia: continue

        with st.expander(f"📅 {dia}  —  {len(pdvs_dia)} PDV(s)", expanded=True):
            # Cabecalho
            hc = st.columns([0.5, 2.0, 2.5, 1.5, 1.5, 2.0, 1.5, 0.8])
            for col, txt in zip(hc, ["#","Cliente — PDV","Endereco / Bairro","Tipo","Freq.",
                                      "Gerente","Horario","Mapa"]):
                col.markdown(f"<small><b>{txt}</b></small>", unsafe_allow_html=True)

            for i, p in enumerate(pdvs_dia, 1):
                (pdv_id, cli, pdv_nome, tipo, dia_v, freq, end, bairro,
                 cidade, gerente, horario, ordem, lat, lng) = p
                c = st.columns([0.5, 2.0, 2.5, 1.5, 1.5, 2.0, 1.5, 0.8])
                c[0].caption(str(i))
                c[1].write(f"{cli} — {pdv_nome}")
                loc = " | ".join(filter(None, [end, bairro, cidade]))
                c[2].caption(loc or "—")
                c[3].caption(tipo)
                c[4].caption(freq)
                c[5].caption(gerente or "—")
                c[6].caption(horario or "—")
                with c[7]:
                    if lat and lng:
                        maps_url = f"https://www.google.com/maps?q={lat},{lng}"
                        st.markdown(f"[📍]({maps_url})")
                    else:
                        st.caption("—")

            # Editor de ordem
            with st.expander(f"Editar ordem de visita — {dia}"):
                st.caption("Defina a ordem numerica em que os PDVs serao visitados neste dia.")
                for p in pdvs_dia:
                    (pdv_id, cli, pdv_nome, tipo, dia_v, freq, end, bairro,
                     cidade, gerente, horario, ordem_at, lat, lng) = p
                    col_n, col_s = st.columns([3,1])
                    col_n.caption(f"{cli} — {pdv_nome}")
                    with col_s:
                        nova_ordem = st.number_input(
                            "Ordem", min_value=1, max_value=999,
                            value=int(ordem_at) if ordem_at and ordem_at < 999 else i,
                            key=f"ord_{pdv_id}", label_visibility="collapsed")
                if st.button(f"Salvar ordem — {dia}", key=f"salvar_ord_{dia}",
                             type="primary"):
                    conn = conectar()
                    for p in pdvs_dia:
                        pdv_id = p[0]
                        key    = f"ord_{pdv_id}"
                        val    = st.session_state.get(key, 999)
                        conn.execute("UPDATE pdv SET ordem_roteiro=? WHERE pdv_id=?",
                                     (val, pdv_id))
                    conn.commit(); conn.close()
                    st.success(f"Ordem do {dia} salva!")
                    st.rerun()

    # Link Google Maps com todos os PDVs com coordenadas
    st.divider()
    pdvs_com_gps = [(p[1], p[2], p[12], p[13]) for p in pdvs if p[12] and p[13]]
    if pdvs_com_gps:
        st.markdown("**Abrir roteiro no Google Maps**")
        st.caption(f"{len(pdvs_com_gps)} PDV(s) com coordenadas GPS cadastradas.")

        if len(pdvs_com_gps) <= 10:
            waypoints = "/".join(f"{p[2]},{p[3]}" for p in pdvs_com_gps[1:-1])
            origem  = f"{pdvs_com_gps[0][2]},{pdvs_com_gps[0][3]}"
            destino = f"{pdvs_com_gps[-1][2]},{pdvs_com_gps[-1][3]}"
            if waypoints:
                maps_roteiro = (f"https://www.google.com/maps/dir/{origem}/"
                                f"{waypoints.replace('/','/') }/{destino}")
            else:
                maps_roteiro = f"https://www.google.com/maps/dir/{origem}/{destino}"
            st.link_button("Abrir roteiro no Google Maps", maps_roteiro,
                           use_container_width=False)
            st.caption("Abre o Google Maps com todos os PDVs como paradas do roteiro.")
        else:
            st.caption("Para roteiros com mais de 10 PDVs, use os links individuais 📍 na tabela acima.")
    else:
        st.caption("Cadastre as coordenadas GPS nos PDVs para habilitar o roteiro no Google Maps.")
        st.caption("Como cadastrar: Clientes → PDVs → Editar → informe Latitude e Longitude "
                   "(obtenha no Google Maps pressionando o ponto por alguns segundos).")


# ==============================================================
# PROMOTORES E ATENDIMENTO (att_promotor / att_vendedor)
# ==============================================================

DIAS_SEMANA  = ["Seg","Ter","Qua","Qui","Sex","Sab"]
FREQ_PROM    = ["Diaria","Semanal","Quinzenal"]
FREQ_VEND    = ["Semanal","Quinzenal","Mensal","Bimestral","Sob demanda"]


def _tela_promotores():
    st.header("Promotores e Atendimento")
    st.caption("Cadastre promotores e defina quais PDVs cada um atende, com dias e frequencia.")

    ABAS_VIS = {"prom":"Promotores","att":"Atendimento Promotor",
                "vend":"Atendimento Vendedor","rot":"Roteiro Promotor"}
    if "vis_aba" not in st.session_state: st.session_state["vis_aba"] = "prom"
    cols = st.columns(4)
    for col,(k,v) in zip(cols, ABAS_VIS.items()):
        ativa = st.session_state["vis_aba"] == k
        if col.button(v, key=f"visnav_{k}", use_container_width=True,
                      type="primary" if ativa else "secondary"):
            st.session_state["vis_aba"] = k; st.rerun()
    st.divider()
    a = st.session_state["vis_aba"]
    if a=="prom":   _tela_cadastro_promotores()
    elif a=="att":  _tela_att_promotor()
    elif a=="vend": _tela_att_vendedor()
    elif a=="rot":  _tela_roteiro_promotor()


# ── Cadastro de Promotores ────────────────────────────

def _tela_cadastro_promotores():
    st.subheader("Promotores cadastrados")

    proms = query("""SELECT promotor_id, nome, fone, cidade, estado, ativo
        FROM promotor ORDER BY nome""")

    if proms:
        df = pd.DataFrame(proms,
                          columns=["ID","Nome","Fone","Cidade","UF","Ativo"])
        df["Ativo"] = df["Ativo"].map({1:"Sim",0:"Nao"})
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Edicao rapida
        prom_sel = st.selectbox("Editar promotor", [(None,"— selecione")] +
                                [(p[0], p[1]) for p in proms],
                                format_func=lambda x: x[1], key="prom_edit_sel")
        if prom_sel[0]:
            _form_editar_promotor(prom_sel[0])
    else:
        st.info("Nenhum promotor cadastrado ainda.")

    st.divider()
    st.subheader("Novo promotor")
    with st.form("novo_promotor", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome_p  = st.text_input("Nome completo *")
            fone_p  = st.text_input("Fone / WhatsApp")
            email_p = st.text_input("E-mail")
            cpf_p   = st.text_input("CPF")
        with col2:
            cidade_p  = st.text_input("Cidade")
            estado_p  = st.selectbox("UF", _ufs_vis(), key="prom_uf")
            bairro_p  = st.text_input("Bairro / regiao de atuacao")
            veiculo_p = st.text_input("Veiculo (opcional)", placeholder="Ex: Moto, Carro, A pe")
        obs_p  = st.text_input("Observacao")
        salvar = st.form_submit_button("Salvar promotor", type="primary")

    if salvar:
        if not nome_p.strip():
            st.error("Nome e obrigatorio."); return
        conn = conectar()
        conn.execute("""INSERT INTO promotor
            (nome, fone, email, cpf, cidade, estado, bairro, veiculo, observacao, ativo)
            VALUES (?,?,?,?,?,?,?,?,?,1)""",
            (nome_p.strip(), fone_p or None, email_p or None, cpf_p or None,
             cidade_p or None, estado_p, bairro_p or None,
             veiculo_p or None, obs_p or None))
        conn.commit(); conn.close()
        st.success(f"Promotor '{nome_p}' cadastrado!")
        st.rerun()


def _form_editar_promotor(prom_id):
    p = query("SELECT * FROM promotor WHERE promotor_id=?", (prom_id,))
    if not p: return
    p = p[0]
    with st.form(f"edit_prom_{prom_id}"):
        col1, col2 = st.columns(2)
        with col1:
            nome_p    = st.text_input("Nome",    p[1] or "")
            fone_p    = st.text_input("Fone",    p[2] or "")
            email_p   = st.text_input("E-mail",  p[3] or "")
            cpf_p     = st.text_input("CPF",     p[4] or "")
        with col2:
            cidade_p  = st.text_input("Cidade",  p[7] or "")
            ufs       = _ufs_vis()
            idx_uf    = ufs.index(p[8]) if p[8] in ufs else 0
            estado_p  = st.selectbox("UF", ufs, index=idx_uf, key=f"prom_uf_e_{prom_id}")
            bairro_p  = st.text_input("Bairro",  p[9] or "")
            veiculo_p = st.text_input("Veiculo", p[6] or "")
        obs_p   = st.text_input("Observacao", p[11] or "")
        ativo_p = st.checkbox("Ativo", value=bool(p[12]))
        salvar  = st.form_submit_button("Salvar alteracoes", type="primary")
    if salvar:
        conn = conectar()
        conn.execute("""UPDATE promotor SET nome=?, fone=?, email=?, cpf=?,
            veiculo=?, cidade=?, estado=?, bairro=?, observacao=?, ativo=?
            WHERE promotor_id=?""",
            (nome_p, fone_p or None, email_p or None, cpf_p or None,
             veiculo_p or None, cidade_p or None, estado_p,
             bairro_p or None, obs_p or None, int(ativo_p), prom_id))
        conn.commit(); conn.close()
        st.success("Promotor atualizado!"); st.rerun()


def _ufs_vis():
    return ["AC","AL","AM","AP","BA","CE","DF","ES","GO","MA","MG","MS","MT",
            "PA","PB","PE","PI","PR","RJ","RN","RO","RR","RS","SC","SE","SP","TO"]


# ── Atendimento Promotor ──────────────────────────────

def _tela_att_promotor():
    st.subheader("Atendimento de Promotores por PDV")
    st.caption("Defina quais PDVs cada promotor atende, com dias da semana e frequencia.")

    proms = query("SELECT promotor_id, nome FROM promotor WHERE ativo=1 ORDER BY nome")
    if not proms:
        st.info("Cadastre um promotor primeiro."); return

    prom_sel = st.selectbox("Promotor", proms, format_func=lambda x: x[1],
                            key="att_prom_sel")
    prom_id  = prom_sel[0]

    # PDVs ja atendidos por este promotor
    atts = query("""
        SELECT ap.att_promotor_id, c.nome_fantasia,
               COALESCE(pdv.nome_loja,'Matriz') AS loja,
               COALESCE(pdv.cidade,'')           AS cidade,
               COALESCE(pdv.setor,'—')           AS setor,
               COALESCE(pdv.tipo_pdv,'—')        AS tipo,
               ap.dias_visita, ap.frequencia,
               ap.hora_inicio, ap.hora_fim,
               ap.ativo, ap.pdv_id
        FROM att_promotor ap
        JOIN pdv     ON ap.pdv_id=pdv.pdv_id
        JOIN cliente c ON pdv.cliente_id=c.cliente_id
        WHERE ap.promotor_id=?
        ORDER BY c.nome_fantasia, loja
    """, (prom_id,))

    if atts:
        st.caption(f"{len(atts)} PDV(s) atendido(s) por {prom_sel[1]}")
        hc = st.columns([2.0, 2.0, 1.2, 1.2, 1.5, 1.5, 0.7, 1.0])
        for col, txt in zip(hc, ["Cliente","PDV","Setor","Tipo","Dias","Freq.","Ativo",""]):
            col.markdown(f"<small><b>{txt}</b></small>", unsafe_allow_html=True)

        for att in atts:
            (att_id, cli, loja, cidade, setor, tipo,
             dias, freq, h_ini, h_fim, ativo, pdv_id) = att
            c = st.columns([2.0, 2.0, 1.2, 1.2, 1.5, 1.5, 0.7, 1.0])
            c[0].write(cli)
            c[1].caption(loja)
            c[2].caption(setor)
            c[3].caption(tipo)
            c[4].caption(dias or "—")
            c[5].caption(freq or "—")
            c[6].caption("✅" if ativo else "❌")
            with c[7]:
                if st.button("✏️", key=f"ed_att_p_{att_id}", use_container_width=True):
                    st.session_state["att_prom_editar"] = att_id
                    st.rerun()

            # Form de edicao inline
            if st.session_state.get("att_prom_editar") == att_id:
                with st.form(f"edit_att_p_{att_id}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        dias_sel = st.multiselect("Dias de visita", DIAS_SEMANA,
                                                  default=[d.strip() for d in (dias or "").split(",") if d.strip()],
                                                  key=f"dias_p_{att_id}")
                        freq_e   = st.selectbox("Frequencia", FREQ_PROM,
                                                index=FREQ_PROM.index(freq) if freq in FREQ_PROM else 1,
                                                key=f"freq_p_{att_id}")
                    with col2:
                        h_ini_e  = st.text_input("Hora inicio", value=h_ini or "",
                                                 placeholder="Ex: 08:00", key=f"hini_p_{att_id}")
                        h_fim_e  = st.text_input("Hora fim", value=h_fim or "",
                                                 placeholder="Ex: 17:00", key=f"hfim_p_{att_id}")
                        ativo_e  = st.checkbox("Ativo", value=bool(ativo), key=f"ativ_p_{att_id}")
                    col_s, col_c = st.columns(2)
                    with col_s: salvar_e   = st.form_submit_button("Salvar", type="primary")
                    with col_c: cancelar_e = st.form_submit_button("Cancelar")
                if salvar_e:
                    conn = conectar()
                    conn.execute("""UPDATE att_promotor SET dias_visita=?, frequencia=?,
                        hora_inicio=?, hora_fim=?, ativo=?
                        WHERE att_promotor_id=?""",
                        (",".join(dias_sel), freq_e,
                         h_ini_e or None, h_fim_e or None, int(ativo_e), att_id))
                    conn.commit(); conn.close()
                    st.session_state.pop("att_prom_editar", None)
                    st.success("Atendimento atualizado!"); st.rerun()
                if cancelar_e:
                    st.session_state.pop("att_prom_editar", None); st.rerun()
    else:
        st.info(f"{prom_sel[1]} ainda nao tem PDVs vinculados.")

    # Adicionar PDV ao promotor
    st.divider()
    with st.expander("Adicionar PDV ao roteiro do promotor"):
        ids_ja  = {a[11] for a in atts} if atts else set()
        clientes = query("SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo=1 ORDER BY nome_fantasia")
        if not clientes:
            st.caption("Nenhum cliente cadastrado."); return

        cli_add = st.selectbox("Cliente", clientes, format_func=lambda x: x[1], key="att_p_cli")
        pdvs_add = query("""SELECT pdv_id, nome_loja, cidade, setor
            FROM pdv WHERE cliente_id=? AND ativo=1 AND pdv_id NOT IN ({})
            ORDER BY nome_loja""".format(",".join("?" * len(ids_ja)) if ids_ja else "0"),
            (cli_add[0], *ids_ja) if ids_ja else (cli_add[0],))

        if not pdvs_add:
            st.caption("Todos os PDVs deste cliente ja estao no roteiro deste promotor.")
        else:
            with st.form(f"add_att_p_{prom_id}", clear_on_submit=True):
                pdv_add  = st.selectbox("PDV", pdvs_add,
                                        format_func=lambda x: f"{x[1]} ({x[2] or ''}) — Setor: {x[3] or '—'}")
                dias_add = st.multiselect("Dias de visita", DIAS_SEMANA)
                col1, col2 = st.columns(2)
                with col1:
                    freq_add   = st.selectbox("Frequencia", FREQ_PROM)
                    h_ini_add  = st.text_input("Hora inicio", placeholder="08:00")
                with col2:
                    h_fim_add  = st.text_input("Hora fim", placeholder="17:00")
                if st.form_submit_button("Adicionar", type="primary"):
                    conn = conectar()
                    conn.execute("""INSERT OR REPLACE INTO att_promotor
                        (promotor_id, pdv_id, dias_visita, frequencia,
                         hora_inicio, hora_fim, ativo)
                        VALUES (?,?,?,?,?,?,1)""",
                        (prom_id, pdv_add[0], ",".join(dias_add) or None,
                         freq_add, h_ini_add or None, h_fim_add or None))
                    conn.commit(); conn.close()
                    st.success(f"'{pdv_add[1]}' adicionado ao roteiro!"); st.rerun()


# ── Atendimento Vendedor ──────────────────────────────

def _tela_att_vendedor():
    st.subheader("Atendimento de Vendedor por PDV")
    st.caption("Defina quais PDVs o vendedor visita e com qual frequencia.")

    vends = query("SELECT vendedor_id, nome FROM vendedor WHERE ativo=1 ORDER BY nome")
    if not vends:
        st.info("Nenhum vendedor cadastrado. Va em Configuracoes > Vendedores."); return

    vend_sel = st.selectbox("Vendedor", vends, format_func=lambda x: x[1],
                            key="att_vend_sel")
    vend_id  = vend_sel[0]

    atts_v = query("""
        SELECT av.att_vendedor_id, c.nome_fantasia,
               COALESCE(pdv.nome_loja,'Matriz') AS loja,
               COALESCE(pdv.cidade,'')           AS cidade,
               COALESCE(pdv.setor,'—')           AS setor,
               av.dias_visita, av.frequencia, av.ativo, av.pdv_id
        FROM att_vendedor av
        JOIN pdv     ON av.pdv_id=pdv.pdv_id
        JOIN cliente c ON pdv.cliente_id=c.cliente_id
        WHERE av.vendedor_id=?
        ORDER BY c.nome_fantasia, loja
    """, (vend_id,))

    if atts_v:
        st.caption(f"{len(atts_v)} PDV(s) na carteira de {vend_sel[1]}")
        for av in atts_v:
            (av_id, cli, loja, cidade, setor, dias, freq, ativo, pdv_id) = av
            c = st.columns([2.5, 2.0, 1.2, 1.5, 1.5, 0.7, 1.0])
            c[0].write(cli)
            c[1].caption(loja)
            c[2].caption(setor)
            c[3].caption(dias or "Flexivel")
            c[4].caption(freq or "—")
            c[5].caption("✅" if ativo else "❌")
            with c[6]:
                if st.button("🗑️", key=f"del_av_{av_id}", use_container_width=True,
                             help="Remover PDV da carteira"):
                    conn = conectar()
                    conn.execute("DELETE FROM att_vendedor WHERE att_vendedor_id=?", (av_id,))
                    conn.commit(); conn.close(); st.rerun()
    else:
        st.info(f"{vend_sel[1]} ainda nao tem PDVs na carteira.")

    # Adicionar PDV
    st.divider()
    with st.expander("Adicionar PDV a carteira do vendedor"):
        ids_ja_v = {a[8] for a in atts_v} if atts_v else set()
        clientes = query("SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo=1 ORDER BY nome_fantasia")
        if clientes:
            cli_add_v = st.selectbox("Cliente", clientes, format_func=lambda x: x[1], key="att_v_cli")
            pdvs_add_v = query("""SELECT pdv_id, nome_loja, cidade, setor
                FROM pdv WHERE cliente_id=? AND ativo=1 AND pdv_id NOT IN ({})
                ORDER BY nome_loja""".format(",".join("?" * len(ids_ja_v)) if ids_ja_v else "0"),
                (cli_add_v[0], *ids_ja_v) if ids_ja_v else (cli_add_v[0],))
            if not pdvs_add_v:
                st.caption("Todos os PDVs deste cliente ja estao na carteira deste vendedor.")
            else:
                with st.form(f"add_av_{vend_id}", clear_on_submit=True):
                    pdv_add_v  = st.selectbox("PDV", pdvs_add_v,
                                              format_func=lambda x: f"{x[1]} — Setor: {x[3] or '—'}")
                    dias_add_v = st.multiselect("Dias preferidos (opcional)", DIAS_SEMANA)
                    freq_add_v = st.selectbox("Frequencia", FREQ_VEND, index=2)
                    obs_add_v  = st.text_input("Observacao")
                    if st.form_submit_button("Adicionar", type="primary"):
                        conn = conectar()
                        conn.execute("""INSERT OR REPLACE INTO att_vendedor
                            (vendedor_id, pdv_id, dias_visita, frequencia, observacao, ativo)
                            VALUES (?,?,?,?,?,1)""",
                            (vend_id, pdv_add_v[0],
                             ",".join(dias_add_v) or None, freq_add_v,
                             obs_add_v or None))
                        conn.commit(); conn.close()
                        st.success(f"'{pdv_add_v[1]}' adicionado!"); st.rerun()


# ── Roteiro por Promotor ──────────────────────────────

def _tela_roteiro_promotor():
    st.subheader("Roteiro por Promotor")
    st.caption("Visualize o roteiro semanal de cada promotor organizado por dia.")

    proms = query("SELECT promotor_id, nome FROM promotor WHERE ativo=1 ORDER BY nome")
    if not proms:
        st.info("Nenhum promotor cadastrado."); return

    prom_sel = st.selectbox("Promotor", proms, format_func=lambda x: x[1],
                            key="rot_prom_view")

    col1, col2 = st.columns(2)
    with col1:
        fil_setor = st.text_input("Filtrar por setor", key="rot_prom_setor",
                                  placeholder="Ex: Setor Centro")

    atts = query("""
        SELECT ap.dias_visita, ap.frequencia,
               ap.hora_inicio, ap.hora_fim,
               c.nome_fantasia, COALESCE(pdv.nome_loja,'Matriz') AS loja,
               COALESCE(pdv.cidade,'')    AS cidade,
               COALESCE(pdv.setor,'—')   AS setor,
               COALESCE(pdv.tipo_pdv,'—') AS tipo,
               pdv.gerente, pdv.horario_recebimento,
               pdv.latitude, pdv.longitude
        FROM att_promotor ap
        JOIN pdv     ON ap.pdv_id=pdv.pdv_id
        JOIN cliente c ON pdv.cliente_id=c.cliente_id
        WHERE ap.promotor_id=? AND ap.ativo=1
        ORDER BY ap.dias_visita, c.nome_fantasia
    """, (prom_sel[0],))

    if fil_setor.strip():
        atts = [a for a in atts if fil_setor.strip().lower() in (a[7] or "").lower()]

    if not atts:
        st.info(f"Nenhum PDV no roteiro de {prom_sel[1]}.")
        return

    metricas_col = st.columns(3)
    metricas_col[0].metric("PDVs no roteiro", len(atts))
    com_gps = sum(1 for a in atts if a[11] and a[12])
    metricas_col[1].metric("Com GPS", com_gps)
    setores = len(set(a[7] for a in atts if a[7] and a[7] != "—"))
    metricas_col[2].metric("Setores", setores)

    st.divider()

    # Agrupa por dia
    for dia in DIAS_SEMANA:
        pdvs_dia = [a for a in atts if dia in (a[0] or "").split(",")]
        if not pdvs_dia: continue

        with st.expander(f"📅 {dia}  —  {len(pdvs_dia)} PDV(s)", expanded=True):
            hc = st.columns([2.0, 1.8, 1.0, 1.2, 1.5, 1.5, 1.5, 0.7])
            for col, txt in zip(hc, ["Cliente / PDV","Setor","Tipo",
                                      "Gerente","Horario PDV","Entrada","Saida","Mapa"]):
                col.markdown(f"<small><b>{txt}</b></small>", unsafe_allow_html=True)

            for i, a in enumerate(pdvs_dia, 1):
                (dias, freq, h_ini, h_fim, cli, loja, cidade,
                 setor, tipo, gerente, horario, lat, lng) = a
                c = st.columns([2.0, 1.8, 1.0, 1.2, 1.5, 1.5, 1.5, 0.7])
                c[0].write(f"{cli} / {loja}")
                c[1].caption(setor)
                c[2].caption(tipo)
                c[3].caption(gerente or "—")
                c[4].caption(horario or "—")
                c[5].caption(h_ini or "—")
                c[6].caption(h_fim or "—")
                with c[7]:
                    if lat and lng:
                        st.markdown(f"[📍](https://www.google.com/maps?q={lat},{lng})")
                    else:
                        st.caption("—")

        # Link Google Maps do dia
        pdvs_gps = [(a[11], a[12]) for a in pdvs_dia if a[11] and a[12]]
        if len(pdvs_gps) >= 2:
            wps  = "/".join(f"{p[0]},{p[1]}" for p in pdvs_gps[1:-1])
            orig = f"{pdvs_gps[0][0]},{pdvs_gps[0][1]}"
            dest = f"{pdvs_gps[-1][0]},{pdvs_gps[-1][1]}"
            url  = f"https://www.google.com/maps/dir/{orig}/{wps}/{dest}" if wps \
                   else f"https://www.google.com/maps/dir/{orig}/{dest}"
            st.link_button(f"Abrir rota de {dia} no Google Maps ({len(pdvs_gps)} pontos)",
                           url)