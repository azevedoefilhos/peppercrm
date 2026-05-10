from cache_helpers import cache_clientes, cache_fornecedores, cache_categorias, cache_produtos_fornecedor
# contatos.py — PepperCRM
# Módulo unificado: Contatos, Follow-ups & Negociações
# Modelo: Tópico (assunto) + Linha do tempo de interações

import streamlit as st
import pandas as pd
import io
from datetime import date, timedelta
from database import conectar, query

# ── Constantes ────────────────────────────────────────
VIAS = ["WhatsApp","E-mail","Telefone","Visita presencial",
        "Reunião","Videoconferência","Outro"]

TIPO_TOPICO = ["Contato","Negociação"]

STATUS_TOPICO = ["A contatar","Em andamento","Aguardando retorno",
                 "Proposta enviada","Em negociação","Concluído","Cancelado"]

PRIOR = ["Alta","Média","Baixa"]

VIA_ICONE = {
    "WhatsApp":"💬","E-mail":"✉️","Telefone":"📞",
    "Visita presencial":"🚶","Reunião":"🤝",
    "Videoconferência":"📹","Outro":"📌",
}
STATUS_ICONE = {
    "A contatar":"📋","Em andamento":"🔵","Aguardando retorno":"⏰",
    "Proposta enviada":"📤","Em negociação":"🤝",
    "Concluído":"🟢","Cancelado":"🔴",
}
TIPO_ICONE = {"Contato":"📞","Negociação":"🤝"}

def _ir(p):
    st.session_state["pagina"] = p
    st.session_state["_scroll_topo"] = True
    st.rerun()

def _brl(v):
    try: return f"R$ {float(v):,.2f}".replace(",","X").replace(".",",").replace("X",".")
    except: return "—"


# ═══════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════
def tela_contatos():
    st.header("📞 Contatos & Negociações")
    if st.button("⬅ Voltar"): _ir("home")

    ABAS = {
        "lista":   "📋 Registros",
        "novo":    "➕ Novo",
        "agenda":  "📅 Follow-ups",
        "entidade":"📊 Por cliente/forn.",
        "forn":    "🏭 Por fornecedor",
        "mensagens":"💬 Mensagens",
    }
    if "ct_aba" not in st.session_state:
        st.session_state["ct_aba"] = "lista"

    cols = st.columns(len(ABAS))
    for col, (k, v) in zip(cols, ABAS.items()):
        ativa = st.session_state["ct_aba"] == k
        if col.button(v, key=f"ctnav_{k}", use_container_width=True,
                      type="primary" if ativa else "secondary"):
            st.session_state["ct_aba"] = k
            st.session_state.pop("ct_topico_aberto", None)
            st.rerun()

    st.divider()

    msg = st.session_state.pop("ct_msg", None)
    if msg: st.success(msg)

    a = st.session_state["ct_aba"]
    if a == "lista":      _lista_topicos()
    elif a == "novo":     _form_novo_topico()
    elif a == "agenda":   _agenda()
    elif a == "entidade": _por_entidade()
    elif a == "forn":     _por_fornecedor()
    elif a == "mensagens":
        from catalogo import _tela_mensagens
        _tela_mensagens()


# ═══════════════════════════════════════════════════════
# 1. LISTA DE TÓPICOS
# ═══════════════════════════════════════════════════════
def _lista_topicos():
    # Filtros
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        fil_tipo = st.selectbox("Tipo", ["Todos"] + TIPO_TOPICO, key="fl_tipo")
    with col2:
        fil_status = st.selectbox("Status", ["Todos"] + STATUS_TOPICO, key="fl_status")
    with col3:
        fil_prior = st.selectbox("Prioridade", ["Todas"] + PRIOR, key="fl_prior")
    with col4:
        busca = st.text_input("🔍 Buscar", placeholder="Assunto ou cliente...", key="fl_busca")

    col_f, col_per, col_ord = st.columns([2, 1.5, 1.5])
    with col_f:
        forns = cache_fornecedores()
        forn_opts = [(0,"Todos os fornecedores")] + [(f[0],f[1]) for f in forns]
        fil_forn = st.selectbox("Fornecedor tratado", forn_opts,
                                format_func=lambda x: x[1], key="fl_forn")
    with col_per:
        fil_periodo = st.selectbox("Período", 
                                   ["Todos", "Hoje", "Esta semana", "Este mês", "Últimos 30 dias", "Últimos 90 dias"],
                                   key="fl_periodo")
    with col_ord:
        fil_ordem = st.selectbox("Ordenar por",
                                 ["Status/Prioridade", "Mais recentes", "Mais antigos", "Próx. followup"],
                                 key="fl_ordem")

    # Query
    where = ["cr.ativo=1"]
    params = []
    if fil_tipo != "Todos":
        where.append("COALESCE(cr.tipo_topico,'Contato')=?"); params.append(fil_tipo)
    if fil_status != "Todos":
        where.append("cr.status=?"); params.append(fil_status)
    if fil_prior != "Todas":
        where.append("cr.prioridade=?"); params.append(fil_prior)
    if busca.strip():
        b = f"%{busca.strip()}%"
        where.append("(cr.assunto LIKE ? OR c.nome_fantasia LIKE ?)")
        params.extend([b, b])
    if fil_forn[0]:
        where.append("""cr.contato_id IN (
            SELECT cxf.contato_id FROM contato_x_fornecedor cxf
            WHERE cxf.fornecedor_id=?)""")
        params.append(fil_forn[0])
    # Filtro de periodo: considera data do contato OU data da ultima interacao
    _ult_int = """(SELECT MAX(ci.data_interacao) FROM contato_interacao ci
                   WHERE ci.contato_id=cr.contato_id AND ci.ativo=1)"""
    if fil_periodo == "Hoje":
        where.append(f"(cr.data_contato::date = CURRENT_DATE OR ({_ult_int})::date = CURRENT_DATE)")
    elif fil_periodo == "Esta semana":
        where.append(f"(cr.data_contato::date >= CURRENT_DATE - INTERVAL '7 days' OR ({_ult_int})::date >= CURRENT_DATE - INTERVAL '7 days')")
    elif fil_periodo == "Este mês":
        where.append(f"(cr.data_contato::date >= DATE_TRUNC('month', CURRENT_DATE) OR ({_ult_int})::date >= DATE_TRUNC('month', CURRENT_DATE))")
    elif fil_periodo == "Últimos 30 dias":
        where.append(f"(cr.data_contato::date >= CURRENT_DATE - INTERVAL '30 days' OR ({_ult_int})::date >= CURRENT_DATE - INTERVAL '30 days')")
    elif fil_periodo == "Últimos 90 dias":
        where.append(f"(cr.data_contato::date >= CURRENT_DATE - INTERVAL '90 days' OR ({_ult_int})::date >= CURRENT_DATE - INTERVAL '90 days')")

    topicos = query(f"""
        SELECT cr.contato_id,
               COALESCE(cr.tipo_topico,'Contato') AS tipo,
               cr.assunto,
               COALESCE(c.nome_fantasia, f.nome_fantasia,'—') AS entidade,
               cr.tipo_entidade,
               cr.status, cr.prioridade,
               cr.data_contato,
               cr.data_followup,
               COALESCE(
                   (SELECT GROUP_CONCAT(fn.nome_fantasia,' / ')
                    FROM contato_x_fornecedor cxf
                    JOIN fornecedor fn ON cxf.fornecedor_id=fn.fornecedor_id
                    WHERE cxf.contato_id=cr.contato_id),'—') AS fornecedores,
               (SELECT COUNT(*) FROM contato_interacao ci
                WHERE ci.contato_id=cr.contato_id AND ci.ativo=1) AS n_int,
               (SELECT MAX(ci.data_interacao) FROM contato_interacao ci
                WHERE ci.contato_id=cr.contato_id AND ci.ativo=1) AS ultima_int
        FROM contato_registro cr
        LEFT JOIN cliente    c ON cr.cliente_id    = c.cliente_id
        LEFT JOIN fornecedor f ON cr.fornecedor_id = f.fornecedor_id
        WHERE {' AND '.join(where)}
        ORDER BY
            CASE WHEN ? = 'Mais recentes' THEN cr.data_contato END DESC,
            CASE WHEN ? = 'Mais antigos' THEN cr.data_contato END ASC,
            CASE WHEN ? = 'Próx. followup' THEN cr.data_followup END ASC NULLS LAST,
            CASE WHEN ? NOT IN ('Mais recentes','Mais antigos','Próx. followup') THEN
                CASE cr.status
                    WHEN 'A contatar' THEN 1 WHEN 'Em andamento' THEN 2
                    WHEN 'Em negociação' THEN 3 WHEN 'Aguardando retorno' THEN 4
                    WHEN 'Proposta enviada' THEN 5 WHEN 'Concluído' THEN 6 ELSE 7
                END
            END,
            CASE WHEN ? NOT IN ('Mais recentes','Mais antigos','Próx. followup') THEN
                CASE cr.prioridade WHEN 'Alta' THEN 1 WHEN 'Média' THEN 2 ELSE 3 END
            END,
            cr.data_contato DESC
    """, tuple(params) + (fil_ordem, fil_ordem, fil_ordem, fil_ordem, fil_ordem))

    if not topicos:
        st.info("Nenhum registro encontrado para os filtros selecionados.")
        return

    hoje = date.today().isoformat()
    st.caption(f"**{len(topicos)}** registro(s)")

    for row in topicos:
        (cid, tipo, assunto, entidade, tipo_ent,
         status, prioridade, data_c, followup,
         fornecedores, n_int, ultima_int) = row

        aberto = st.session_state.get("ct_topico_aberto") == cid
        vencido = followup and followup < hoje and status not in ("Concluído","Cancelado")

        with st.container(border=True):
            c1, c2, c3, c4, c5, c6 = st.columns([0.7, 3.0, 1.8, 1.2, 0.6, 0.5])

            with c1:
                novo_tipo_card = st.selectbox(
                    "Tipo", TIPO_TOPICO,
                    index=TIPO_TOPICO.index(tipo) if tipo in TIPO_TOPICO else 0,
                    key=f"ct_tipo_{cid}",
                    label_visibility="collapsed")
                novo_st_card = st.selectbox(
                    "Status", STATUS_TOPICO,
                    index=STATUS_TOPICO.index(status) if status in STATUS_TOPICO else 0,
                    key=f"ct_st_{cid}",
                    label_visibility="collapsed")
                if novo_tipo_card != tipo or novo_st_card != status:
                    conn = conectar()
                    conn.execute("""UPDATE contato_registro SET tipo_topico=?, status=?
                        WHERE contato_id=?""", (novo_tipo_card, novo_st_card, cid))
                    conn.commit(); conn.close()
                    st.session_state["ct_msg"] = (
                        f"✅ '{assunto[:35]}' → {novo_tipo_card} · {novo_st_card}")
                    st.rerun()

            with c2:
                st.markdown(f"**{'🔴 ' if vencido else ''}{assunto}**")
                ico_ent = "👤" if tipo_ent=="cliente" else "🏭"
                st.caption(f"{ico_ent} {entidade}")
                if fornecedores and fornecedores != "—":
                    pills = " ".join(
                        f'<span style="background:#e8f5e9;color:#2d6a4f;'
                        f'padding:1px 7px;border-radius:10px;font-size:11px">'
                        f'🏭 {fn}</span>'
                        for fn in fornecedores.split(" / "))
                    st.markdown(pills, unsafe_allow_html=True)

            with c3:
                pr_ico = "🔴" if prioridade=="Alta" else "🟡" if prioridade=="Média" else "🟢"
                st.caption(f"{pr_ico} {prioridade}")
                st.caption(f"📅 {followup or data_c}")
                st.caption(f"💬 {n_int} int.  |  {ultima_int or data_c}")

            with c4:
                novo_pr_card = st.selectbox(
                    "Prior.", PRIOR,
                    index=PRIOR.index(prioridade) if prioridade in PRIOR else 1,
                    key=f"ct_pr_{cid}",
                    label_visibility="collapsed")
                if novo_pr_card != prioridade:
                    conn = conectar()
                    conn.execute("UPDATE contato_registro SET prioridade=? WHERE contato_id=?",
                                 (novo_pr_card, cid))
                    conn.commit(); conn.close()
                    st.session_state["ct_msg"] = "✅ Prioridade atualizada."
                    st.rerun()

            with c5:
                label = "▲" if aberto else "▼"
                if st.button(label, key=f"tog_{cid}", use_container_width=True,
                             help="Ver histórico e interações"):
                    if aberto:
                        st.session_state.pop("ct_topico_aberto", None)
                    else:
                        st.session_state["ct_topico_aberto"] = cid
                    st.rerun()

            with c6:
                # Exclusão com confirmação inline
                if st.session_state.get(f"ct_del_confirm_{cid}"):
                    if st.button("✅", key=f"ct_del_ok_{cid}",
                                 use_container_width=True,
                                 help="Confirmar exclusão"):
                        conn = conectar()
                        conn.execute(
                            "UPDATE contato_interacao SET ativo=0 WHERE contato_id=?",
                            (cid,))
                        conn.execute(
                            "UPDATE contato_registro SET ativo=0 WHERE contato_id=?",
                            (cid,))
                        conn.commit(); conn.close()
                        st.session_state.pop(f"ct_del_confirm_{cid}", None)
                        st.session_state.pop("ct_topico_aberto", None)
                        st.session_state["ct_msg"] = "🗑️ Registro excluído."
                        st.rerun()
                else:
                    if st.button("🗑️", key=f"ct_del_{cid}",
                                 use_container_width=True,
                                 help="Excluir este registro"):
                        st.session_state[f"ct_del_confirm_{cid}"] = True
                        st.rerun()

            # Confirmação pendente — aviso visível
            if st.session_state.get(f"ct_del_confirm_{cid}"):
                st.warning(
                    f"⚠️ Excluir **{assunto[:50]}**? "
                    f"Clique ✅ para confirmar ou recarregue a página para cancelar.")

            if aberto:
                _painel_topico(cid, status, prioridade, tipo)


# ═══════════════════════════════════════════════════════
# 2. PAINEL DO TÓPICO — linha do tempo + nova interação
# ═══════════════════════════════════════════════════════
def _painel_topico(cid, status_atual, prioridade_atual, tipo_atual):
    """Painel completo: histórico editável + nova interação + edição do tópico."""
    st.divider()

    cr = query("""SELECT cr.*, c.nome_fantasia, f.nome_fantasia
        FROM contato_registro cr
        LEFT JOIN cliente c ON cr.cliente_id=c.cliente_id
        LEFT JOIN fornecedor f ON cr.fornecedor_id=f.fornecedor_id
        WHERE cr.contato_id=?""", (cid,))
    if not cr: return
    r      = cr[0]
    cli_id = r[4]

    todos_f   = cache_fornecedores()
    forns_vin = query("""SELECT fn.fornecedor_id, fn.nome_fantasia
        FROM contato_x_fornecedor cxf
        JOIN fornecedor fn ON cxf.fornecedor_id=fn.fornecedor_id
        WHERE cxf.contato_id=?""", (cid,))
    ids_vin = [f[0] for f in forns_vin]

    contatos_cli = []
    if cli_id:
        contatos_cli = query("""SELECT contato_cliente_id, nome_contato, departamento, whatsapp
            FROM contato_cliente WHERE cliente_id=? AND ativo=1 ORDER BY nome_contato""",
            (cli_id,))

    def _pd(v):
        try: return date.fromisoformat(str(v)[:10])
        except: return None

    # ════════════════════════════════════════════════════
    # SEÇÃO A — EDIÇÃO DO TÓPICO (sempre visível no topo)
    # ════════════════════════════════════════════════════
    with st.expander("✏️ Editar tópico — assunto, fornecedores, status, prioridade"):
        # Fornecedores — multiselect com hash para não resetar
        _kf       = f"cef_{cid}"
        _hash_key = f"cef_h_{cid}"
        if st.session_state.get(_hash_key) != str(sorted(ids_vin)):
            st.session_state[_kf]       = [(f[0],f[1]) for f in todos_f if f[0] in ids_vin]
            st.session_state[_hash_key] = str(sorted(ids_vin))
        st.multiselect("Fornecedores envolvidos na tratativa",
                       options=[(f[0],f[1]) for f in todos_f],
                       format_func=lambda x: x[1], key=_kf)

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            assunto_e  = st.text_input("Assunto", value=r[7] or "", key=f"eas_{cid}")
        with col_b:
            novo_tipo_e = st.selectbox("Tipo", TIPO_TOPICO,
                                       index=TIPO_TOPICO.index(tipo_atual)
                                       if tipo_atual in TIPO_TOPICO else 0,
                                       key=f"etp_{cid}")
            novo_st_e  = st.selectbox("Status", STATUS_TOPICO,
                                      index=STATUS_TOPICO.index(status_atual)
                                      if status_atual in STATUS_TOPICO else 0,
                                      key=f"est_{cid}")
        with col_c:
            novo_pr_e  = st.selectbox("Prioridade", PRIOR,
                                      index=PRIOR.index(prioridade_atual)
                                      if prioridade_atual in PRIOR else 1,
                                      key=f"epr_{cid}")
            nova_fup_e = st.date_input("Próximo contato",
                                       value=_pd(r[11]), key=f"efu_{cid}")
        obs_e = st.text_input("Observação", value=r[17] or "", key=f"eob_{cid}")

        col_s, col_d = st.columns(2)
        if col_s.button("💾 Salvar alterações do tópico", key=f"esv_{cid}",
                        use_container_width=True, type="primary"):
            _fs = st.session_state.get(_kf, [])
            conn = conectar()
            conn.execute("""UPDATE contato_registro SET
                assunto=?, tipo_topico=?, status=?, prioridade=?,
                data_followup=?, observacao=?
                WHERE contato_id=?""",
                (assunto_e.strip() or r[7], novo_tipo_e, novo_st_e, novo_pr_e,
                 nova_fup_e.isoformat() if nova_fup_e else None,
                 obs_e.strip() or None, cid))
            conn.execute("DELETE FROM contato_x_fornecedor WHERE contato_id=?", (cid,))
            for ft in _fs:
                fid = ft[0] if isinstance(ft,(list,tuple)) else ft
                conn.execute("INSERT OR IGNORE INTO contato_x_fornecedor "
                             "(contato_id, fornecedor_id) VALUES (?,?)", (cid, fid))
            conn.commit(); conn.close()
            st.session_state.pop(_kf, None); st.session_state.pop(_hash_key, None)
            st.session_state["ct_msg"] = "✅ Tópico atualizado."
            st.rerun()

        if col_d.button("🗑️ Encerrar / arquivar tópico", key=f"edel_{cid}",
                        use_container_width=True):
            conn = conectar()
            conn.execute("UPDATE contato_registro SET ativo=0 WHERE contato_id=?", (cid,))
            conn.commit(); conn.close()
            st.session_state.pop("ct_topico_aberto", None)
            st.session_state["ct_msg"] = "Tópico arquivado."
            st.rerun()

    # ════════════════════════════════════════════════════
    # SEÇÃO B — HISTÓRICO DE INTERAÇÕES com edição inline
    # ════════════════════════════════════════════════════
    ints = query("""SELECT ci.interacao_id, ci.data_interacao, ci.via_comunicacao,
               ci.contato_pessoa, ci.descricao, ci.resultado, ci.data_followup
        FROM contato_interacao ci
        WHERE ci.contato_id=? AND ci.ativo=1
        ORDER BY ci.data_interacao DESC""", (cid,))

    if ints:
        st.markdown(f"**📅 Linha do tempo — {len(ints)} interação(ões)**")
        for irow in ints:
            iid, data_i, via, pessoa, desc, result, fup = irow
            lbl = (f"{VIA_ICONE.get(via,'')} {data_i}"
                   + (f"  —  {pessoa}" if pessoa else "")
                   + (f"  |  {desc[:40]}…" if desc and len(desc)>3 else
                      f"  |  {desc}" if desc else ""))

            with st.expander(lbl, expanded=False):
                # Exibição
                if desc:
                    st.caption("**O que foi tratado:**")
                    st.code(desc, language=None)
                if result:
                    st.caption("**Resultado / próximo passo:**")
                    st.code(result, language=None)
                if fup:    st.caption(f"📅 Próximo contato agendado: {fup}")

                st.divider()
                st.caption("**Editar esta interação:**")

                col_ei1, col_ei2, col_ei3 = st.columns(3)
                with col_ei1:
                    ei_data = st.date_input("Data", value=_pd(data_i) or date.today(),
                                            key=f"ei_dt_{iid}")
                    ei_via  = st.selectbox("Via", VIAS,
                                           index=VIAS.index(via) if via in VIAS else 0,
                                           key=f"ei_via_{iid}")
                with col_ei2:
                    ei_pess = st.text_input("Pessoa", value=pessoa or "",
                                            key=f"ei_pe_{iid}")
                    ei_fup  = st.date_input("Próximo contato", value=_pd(fup),
                                            key=f"ei_fup_{iid}")
                with col_ei3:
                    st.write("")  # espaço
                ei_desc   = st.text_area("Descrição", value=desc or "",
                                         key=f"ei_desc_{iid}", height=70)
                ei_result = st.text_area("Resultado", value=result or "",
                                         key=f"ei_res_{iid}", height=55)

                col_ei_s, col_ei_d = st.columns(2)
                if col_ei_s.button("💾 Salvar", key=f"ei_save_{iid}",
                                   type="primary", use_container_width=True):
                    _ed  = st.session_state.get(f"ei_dt_{iid}", ei_data)
                    _ev  = st.session_state.get(f"ei_via_{iid}", ei_via)
                    _ep  = st.session_state.get(f"ei_pe_{iid}", ei_pess).strip()
                    _efu = st.session_state.get(f"ei_fup_{iid}", ei_fup)
                    _edc = st.session_state.get(f"ei_desc_{iid}", ei_desc).strip()
                    _ere = st.session_state.get(f"ei_res_{iid}", ei_result).strip()
                    conn = conectar()
                    conn.execute("""UPDATE contato_interacao SET
                        data_interacao=?, via_comunicacao=?, contato_pessoa=?,
                        descricao=?, resultado=?, data_followup=?
                        WHERE interacao_id=?""",
                        (_ed.isoformat() if _ed else data_i,
                         _ev, _ep or None, _edc or None, _ere or None,
                         _efu.isoformat() if _efu else None, iid))
                    conn.commit(); conn.close()
                    st.session_state["ct_msg"] = "✅ Interação atualizada."
                    st.rerun()

                if not st.session_state.get(f"conf_ei_del_{iid}"):
                    if col_ei_d.button("🗑️ Remover", key=f"ei_del_{iid}",
                                       use_container_width=True):
                        st.session_state[f"conf_ei_del_{iid}"] = True
                        st.rerun()
                else:
                    st.warning("⚠️ Remover esta interação?")
                    _i1, _i2 = st.columns(2)
                    with _i1:
                        if st.button("✅ Sim", key=f"conf_ei_ok_{iid}",
                                     type="primary", use_container_width=True):
                            conn = conectar()
                            conn.execute("UPDATE contato_interacao SET ativo=0 WHERE interacao_id=?", (iid,))
                            conn.commit(); conn.close()
                            st.session_state.pop(f"conf_ei_del_{iid}", None)
                            st.rerun()
                    with _i2:
                        if st.button("❌ Não", key=f"conf_ei_no_{iid}",
                                     use_container_width=True):
                            st.session_state.pop(f"conf_ei_del_{iid}", None)
                            st.rerun()
    else:
        st.info("Ainda sem interações. Registre a primeira abaixo.")

    st.divider()

    # ════════════════════════════════════════════════════
    # SEÇÃO C — NOVA INTERAÇÃO
    # ════════════════════════════════════════════════════
    st.markdown("**➕ Registrar nova interação**")

    _mk = f"ct_pm_{cid}"
    if _mk not in st.session_state: st.session_state[_mk] = "sel"

    col_m1, col_m2, col_m3 = st.columns(3)
    for btn_key, btn_lbl, modo in [
        (f"msel_{cid}", "👤 Contato existente", "sel"),
        (f"mlivre_{cid}", "✏️ Digitar nome", "livre"),
        (f"mcad_{cid}",  "➕ Cadastrar pessoa", "cad"),
    ]:
        ativa = st.session_state[_mk] == modo
        if [col_m1,col_m2,col_m3][["sel","livre","cad"].index(modo)].button(
                btn_lbl, key=btn_key, use_container_width=True,
                type="primary" if ativa else "secondary"):
            st.session_state[_mk] = modo; st.rerun()

    pessoa_nome = ""; ct_cli_id = None

    if st.session_state[_mk] == "sel":
        if contatos_cli:
            opts = [(None,"— não especificado —")] +                    [(c[0], f"{c[1]}" + (f" — {c[2]}" if c[2] else ""))
                    for c in contatos_cli]
            sel_c = st.selectbox("Pessoa", opts,
                                 format_func=lambda x: x[1], key=f"ctsel_{cid}")
            if sel_c and sel_c[0]:
                ct_cli_id = sel_c[0]
                ct_i = next((c for c in contatos_cli if c[0]==sel_c[0]), None)
                if ct_i:
                    pessoa_nome = ct_i[1]
                    if ct_i[3]:
                        num = "".join(filter(str.isdigit, ct_i[3]))
                        if not num.startswith("55"): num = "55" + num
                        st.caption(f"💬 [WhatsApp](https://wa.me/{num})")
        else:
            st.info("Nenhuma pessoa cadastrada — use **Digitar nome** ou **Cadastrar pessoa**.")
    elif st.session_state[_mk] == "livre":
        pessoa_nome = st.text_input("Nome", placeholder="Ex: Renato, Ed Carlos...",
                                    key=f"ctlivre_{cid}")
    else:
        col_a, col_b = st.columns(2)
        with col_a:
            st.text_input("Nome *", key=f"ncn_{cid}")
            st.text_input("Cargo / Depto.", key=f"ncc_{cid}")
        with col_b:
            st.text_input("WhatsApp", key=f"ncw_{cid}")
            st.text_input("Telefone", key=f"ncf_{cid}")
        st.text_input("E-mail", key=f"nce_{cid}")
        _prev = st.session_state.get(f"ncn_{cid}","").strip()
        if _prev: st.success(f"✅ **{_prev}** será cadastrado ao salvar.")
        pessoa_nome = _prev

    col_i1, col_i2, col_i3 = st.columns(3)
    with col_i1:
        data_i  = st.date_input("Data", value=date.today(), key=f"ni_dt_{cid}",
                                help="Pode ser data passada")
        via_i   = st.selectbox("Via", VIAS, key=f"ni_via_{cid}")
    with col_i2:
        fup_i   = st.date_input("Próximo contato", value=None, key=f"ni_fup_{cid}")
    with col_i3:
        novo_st = st.selectbox("Atualizar status",STATUS_TOPICO,
                               index=STATUS_TOPICO.index(status_atual)
                               if status_atual in STATUS_TOPICO else 0,
                               key=f"ni_st_{cid}")
        novo_tp = st.selectbox("Tipo",TIPO_TOPICO,
                               index=TIPO_TOPICO.index(tipo_atual)
                               if tipo_atual in TIPO_TOPICO else 0,
                               key=f"ni_tp_{cid}")

    desc_i   = st.text_area("O que foi tratado", key=f"ni_desc_{cid}", height=70)
    result_i = st.text_area("Resultado / próximo passo", key=f"ni_res_{cid}", height=55)

    if st.button("💾 Salvar interação", key=f"ni_save_{cid}",
                 type="primary", use_container_width=True):
        novo_ct_id = None
        if st.session_state.get(_mk) == "cad" and cli_id:
            _nc = st.session_state.get(f"ncn_{cid}","").strip()
            if _nc:
                conn = conectar(); cur = conn.cursor()
                cur.execute("""INSERT INTO contato_cliente
                    (cliente_id, nome_contato, departamento, fone, email, whatsapp, ativo)
                    VALUES (?,?,?,?,?,?,1)""",
                    (cli_id, _nc,
                     st.session_state.get(f"ncc_{cid}","").strip() or None,
                     st.session_state.get(f"ncf_{cid}","").strip() or None,
                     st.session_state.get(f"nce_{cid}","").strip() or None,
                     st.session_state.get(f"ncw_{cid}","").strip() or None))
                novo_ct_id = cur.lastrowid; pessoa_nome = _nc
                conn.commit(); conn.close()

        _dt  = st.session_state.get(f"ni_dt_{cid}", data_i)
        _via = st.session_state.get(f"ni_via_{cid}", via_i)
        _fup = st.session_state.get(f"ni_fup_{cid}", fup_i)
        _dc  = st.session_state.get(f"ni_desc_{cid}", desc_i).strip()
        _re  = st.session_state.get(f"ni_res_{cid}", result_i).strip()
        _nst = st.session_state.get(f"ni_st_{cid}", novo_st)
        _ntp = st.session_state.get(f"ni_tp_{cid}", novo_tp)

        conn = conectar()
        conn.execute("""INSERT INTO contato_interacao
            (contato_id, data_interacao, via_comunicacao,
             contato_pessoa, contato_cliente_id,
             descricao, resultado, data_followup, ativo)
            VALUES (?,?,?,?,?,?,?,?,1)""",
            (cid, _dt.isoformat() if hasattr(_dt,'isoformat') else str(_dt),
             _via, pessoa_nome or None, novo_ct_id or ct_cli_id,
             _dc or None, _re or None,
             _fup.isoformat() if _fup and hasattr(_fup,'isoformat') else None))
        _fup_val = _fup.isoformat() if _fup and hasattr(_fup,'isoformat') else None
        if _fup_val:
            conn.execute("UPDATE contato_registro SET status=?, tipo_topico=?, data_followup=? WHERE contato_id=?",
                (_nst, _ntp, _fup_val, cid))
        else:
            conn.execute("UPDATE contato_registro SET status=?, tipo_topico=? WHERE contato_id=?",
                (_nst, _ntp, cid))
        conn.commit(); conn.close()

        for k in [f"ncn_{cid}",f"ncc_{cid}",f"ncf_{cid}",f"ncw_{cid}",f"nce_{cid}"]:
            st.session_state.pop(k, None)
        st.session_state[_mk] = "sel"
        st.session_state.pop(f"exp_inter_{cid}", None)
        st.session_state["ct_msg"] = "✅ Interação registrada com sucesso!"
        st.rerun()


# ═══════════════════════════════════════════════════════
# 3. NOVO TÓPICO
# ═══════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════
# 3. NOVO TÓPICO — formulário em etapas claras
# ═══════════════════════════════════════════════════════
def _form_novo_topico():
    st.subheader("Novo registro")
    st.caption(
        "Preencha os dados do contato. "
        "A data pode ser passada — registre quando tiver tempo. "
        "**Pessoa contatada** é opcional."
    )

    msg = st.session_state.pop("ct_novo_msg", None)
    if msg: st.success(msg)
    err = st.session_state.pop("ct_novo_err", None)
    if err: st.error(err)

    clientes = query("SELECT cliente_id, nome_fantasia, status FROM cliente ORDER BY nome_fantasia")
    fornecs  = cache_fornecedores()

    # ── 1. Com quem ───────────────────────────────────────────────────────
    st.markdown("**1. Com quem foi o contato?**")
    col1, col2 = st.columns(2)
    with col1:
        tipo_ent = st.selectbox("Tipo", ["Cliente","Fornecedor"], key="nn_tipo")
    with col2:
        if tipo_ent == "Cliente":
            ent_sel = st.selectbox(
                "Cliente",
                clientes,
                format_func=lambda x: f"{x[1]}  ({x[2]})" if x[2] else x[1],
                key="nn_cli")
            cli_id = ent_sel[0] if ent_sel else None
            forn_ent_id = None
        else:
            ent_sel = st.selectbox("Fornecedor", fornecs,
                                   format_func=lambda x: x[1], key="nn_forn_ent")
            forn_ent_id = ent_sel[0] if ent_sel else None
            cli_id = None

    # ── 2. Assunto e fornecedores ─────────────────────────────────────────
    st.markdown("**2. Qual o assunto?**")
    assunto = st.text_input("Assunto *",
                            placeholder="Ex: Apresentação Specialli, Negociação vinagre MP Belmont...",
                            key="nn_assunto")
    _kfn = "nn_forns_sel"
    if _kfn not in st.session_state: st.session_state[_kfn] = []
    pre = [(f[0],f[1]) for f in fornecs if f[0]==forn_ent_id] if forn_ent_id else []
    if pre and not st.session_state[_kfn]:
        st.session_state[_kfn] = pre
    st.multiselect("Fornecedores tratados no assunto",
                   options=[(f[0],f[1]) for f in fornecs],
                   format_func=lambda x: x[1], key=_kfn,
                   help="Pode ser mais de um")

    # ── 3. Como e quando ──────────────────────────────────────────────────
    st.markdown("**3. Como e quando aconteceu?**")
    col3, col4, col5 = st.columns(3)
    with col3:
        data_c  = st.date_input("Data do contato *", value=date.today(), key="nn_data",
                                help="Pode ser uma data passada")
        via     = st.selectbox("Via", VIAS, key="nn_via")
    with col4:
        tipo_top = st.selectbox("Tipo", TIPO_TOPICO, key="nn_tipo_top")
        prior    = st.selectbox("Prioridade", PRIOR, index=1, key="nn_prior")
    with col5:
        status   = st.selectbox("Status", STATUS_TOPICO, key="nn_status")
        followup = st.date_input("Próximo contato", value=None, key="nn_fup")

    # ── 4. Pessoa contatada ───────────────────────────────────────────────
    st.markdown("**4. Quem foi a pessoa contatada?** *(opcional)*")
    contatos_cli = []
    if cli_id:
        contatos_cli = query("""SELECT contato_cliente_id, nome_contato, departamento
            FROM contato_cliente WHERE cliente_id=? AND ativo=1 ORDER BY nome_contato""",
            (cli_id,))

    _mk = "nn_pessoa_modo"
    if _mk not in st.session_state: st.session_state[_mk] = "sel"

    col_m1, col_m2, col_m3 = st.columns(3)
    if col_m1.button("👤 Já cadastrada", key="nn_modo_sel",
                     type="primary" if st.session_state[_mk]=="sel" else "secondary",
                     use_container_width=True):
        st.session_state[_mk] = "sel"; st.rerun()
    if col_m2.button("✏️ Digitar nome", key="nn_modo_livre",
                     type="primary" if st.session_state[_mk]=="livre" else "secondary",
                     use_container_width=True):
        st.session_state[_mk] = "livre"; st.rerun()
    if col_m3.button("➕ Cadastrar nova", key="nn_modo_cad",
                     type="primary" if st.session_state[_mk]=="cad" else "secondary",
                     use_container_width=True,
                     help="Cadastra a pessoa no cliente e registra o contato"):
        st.session_state[_mk] = "cad"; st.rerun()

    pessoa_nome    = ""
    ct_cli_id_novo = None

    if st.session_state[_mk] == "sel":
        if contatos_cli:
            opts = [(None,"— não especificado —")] +                    [(c[0], f"{c[1]}" + (f" — {c[2]}" if c[2] else ""))
                    for c in contatos_cli]
            sel_p = st.selectbox("Selecione", opts,
                                 format_func=lambda x: x[1], key="nn_psel")
            if sel_p and sel_p[0]:
                ct_cli_id_novo = sel_p[0]
                ct_i = next((c for c in contatos_cli if c[0]==sel_p[0]), None)
                if ct_i: pessoa_nome = ct_i[1]
        else:
            st.info("Nenhuma pessoa cadastrada ainda — use **Digitar nome** ou **Cadastrar nova**.")

    elif st.session_state[_mk] == "livre":
        pessoa_nome = st.text_input("Nome da pessoa",
                                    placeholder="Ex: Renato (comprador), Ed Carlos (gerente)...",
                                    key="nn_pessoa_livre")

    elif st.session_state[_mk] == "cad":
        st.caption(
            "Preencha os dados abaixo. A pessoa será cadastrada no cliente ao salvar. "
            "Você não precisa sair desta tela."
        )
        col_a, col_b = st.columns(2)
        with col_a:
            st.text_input("Nome *", key="nn_nc_nome", placeholder="Nome completo")
            st.text_input("Cargo / Departamento", key="nn_nc_cargo",
                          placeholder="Ex: Comprador, Gerente, Dono")
        with col_b:
            st.text_input("WhatsApp", key="nn_nc_wa", placeholder="11 9 9999-9999")
            st.text_input("Telefone", key="nn_nc_fone")
        st.text_input("E-mail", key="nn_nc_email")
        _nc_preview = st.session_state.get("nn_nc_nome","").strip()
        if _nc_preview:
            st.success(f"✅ **{_nc_preview}** será cadastrado ao salvar o registro.")
        else:
            st.caption("Preencha o nome acima para cadastrar.")
        pessoa_nome = _nc_preview

    # ── 5. O que foi tratado ──────────────────────────────────────────────
    st.markdown("**5. O que foi tratado?** *(pode preencher depois via edição)*")
    desc   = st.text_area("Descrição",
                          placeholder="Detalhes da conversa, pontos levantados...",
                          key="nn_desc", height=80)
    result = st.text_area("Resultado / próximo passo",
                          placeholder="O que ficou definido? Qual ação ficou pendente?",
                          key="nn_result", height=60)

    # ── Botões ────────────────────────────────────────────────────────────
    st.divider()
    col_s, col_l = st.columns([2,1])
    salvar = col_s.button("💾 Salvar registro", type="primary",
                          use_container_width=True, key="nn_salvar")
    limpar = col_l.button("🗑️ Limpar tudo", use_container_width=True, key="nn_limpar")

    if limpar:
        for k in ["nn_assunto","nn_desc","nn_result","nn_pessoa_livre",
                  _kfn, _mk, "nn_nc_nome","nn_nc_cargo",
                  "nn_nc_fone","nn_nc_wa","nn_nc_email"]:
            st.session_state.pop(k, None)
        st.rerun()

    if salvar:
        _assunto = st.session_state.get("nn_assunto","").strip()
        if not _assunto:
            st.session_state["ct_novo_err"] = "O campo Assunto é obrigatório."
            st.rerun()

        novo_ct_id   = None
        _pessoa_nome = pessoa_nome
        if st.session_state.get(_mk) == "cad" and cli_id:
            _nc = st.session_state.get("nn_nc_nome","").strip()
            if _nc:
                conn = conectar()
                cur  = conn.cursor()
                cur.execute("""INSERT INTO contato_cliente
                    (cliente_id, nome_contato, departamento, fone, email, whatsapp, ativo)
                    VALUES (?,?,?,?,?,?,1)""",
                    (cli_id, _nc,
                     st.session_state.get("nn_nc_cargo","").strip() or None,
                     st.session_state.get("nn_nc_fone","").strip() or None,
                     st.session_state.get("nn_nc_email","").strip() or None,
                     st.session_state.get("nn_nc_wa","").strip() or None))
                novo_ct_id   = cur.lastrowid
                _pessoa_nome = _nc
                conn.commit(); conn.close()

        _via      = st.session_state.get("nn_via", via)
        _data_c   = st.session_state.get("nn_data", data_c)
        _tipo_top = st.session_state.get("nn_tipo_top", tipo_top)
        _prior    = st.session_state.get("nn_prior", prior)
        _status   = st.session_state.get("nn_status", status)
        _followup = st.session_state.get("nn_fup", followup)
        _desc     = st.session_state.get("nn_desc","").strip()
        _result   = st.session_state.get("nn_result","").strip()
        _forns    = st.session_state.get(_kfn, [])

        def _iso(d):
            return d.isoformat() if d and hasattr(d,'isoformat') else None

        conn = conectar()
        conn.execute("""INSERT INTO contato_registro
            (data_contato, via_comunicacao, tipo_entidade, cliente_id, fornecedor_id,
             contato_pessoa, assunto, descricao, resultado,
             data_followup, status, prioridade, tipo_topico, ativo)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,1)""",
            (_iso(_data_c), _via, tipo_ent.lower(), cli_id, forn_ent_id,
             _pessoa_nome or None, _assunto, _desc or None, _result or None,
             _iso(_followup), _status, _prior, _tipo_top))
        novo_cid = conn.execute("SELECT lastval()").fetchone()[0]

        for ft in _forns:
            fid = ft[0] if isinstance(ft,(list,tuple)) else ft
            conn.execute("INSERT OR IGNORE INTO contato_x_fornecedor "
                         "(contato_id, fornecedor_id) VALUES (?,?)", (novo_cid, fid))

        conn.execute("""INSERT INTO contato_interacao
            (contato_id, data_interacao, via_comunicacao,
             contato_pessoa, contato_cliente_id,
             descricao, resultado, data_followup, ativo)
            VALUES (?,?,?,?,?,?,?,?,1)""",
            (novo_cid, _iso(_data_c), _via,
             _pessoa_nome or None, novo_ct_id or ct_cli_id_novo,
             _desc or None, _result or None, _iso(_followup)))
        conn.commit(); conn.close()

        for k in ["nn_assunto","nn_desc","nn_result","nn_pessoa_livre",
                  _kfn, _mk, "nn_nc_nome","nn_nc_cargo",
                  "nn_nc_fone","nn_nc_wa","nn_nc_email"]:
            st.session_state.pop(k, None)

        forns_nomes = ", ".join(
            f[1] if isinstance(f,(list,tuple)) else str(f) for f in _forns) or "—"
        st.session_state["ct_aba"]           = "lista"
        st.session_state["ct_topico_aberto"] = novo_cid
        st.session_state["ct_msg"] = (
            f"✅ **{_assunto}** registrado!  |  Fornecedores: {forns_nomes}")
        st.rerun()


# ═══════════════════════════════════════════════════════
# 4. AGENDA
# ═══════════════════════════════════════════════════════
def _agenda():
    st.subheader("📅 Agenda de follow-ups")
    hoje = date.today()
    semana = (hoje + timedelta(days=7)).isoformat()

    pendentes = query("""
        SELECT cr.contato_id,
               cr.data_followup,
               cr.via_comunicacao,
               COALESCE(c.nome_fantasia, f.nome_fantasia,'—') AS entidade,
               COALESCE(cr.contato_pessoa,'—') AS pessoa,
               cr.assunto, cr.status, cr.prioridade,
               COALESCE(cr.tipo_topico,'Contato') AS tipo,
               cr.cliente_id
        FROM contato_registro cr
        LEFT JOIN cliente    c ON cr.cliente_id    = c.cliente_id
        LEFT JOIN fornecedor f ON cr.fornecedor_id = f.fornecedor_id
        WHERE cr.ativo=1
          AND cr.data_followup IS NOT NULL
          AND cr.status NOT IN ('Concluído','Cancelado')
        ORDER BY cr.data_followup ASC
    """)

    if not pendentes:
        st.success("✅ Agenda limpa — nenhum follow-up pendente.")
        return

    venc   = [r for r in pendentes if r[1] < hoje.isoformat()]
    hoje_l = [r for r in pendentes if r[1] == hoje.isoformat()]
    prox   = [r for r in pendentes if hoje.isoformat() < r[1] <= semana]
    fut    = [r for r in pendentes if r[1] > semana]

    if venc:  st.error(f"🔴 {len(venc)} follow-up(s) vencido(s)")
    if hoje_l:st.warning(f"📌 {len(hoje_l)} follow-up(s) para hoje")

    def _bloco(titulo, lista):
        if not lista: return
        st.markdown(f"**{titulo}** ({len(lista)})")
        for r in lista:
            (cid, fup, via, entidade, pessoa,
             assunto, status, prior, tipo, cli_id) = r
            d = (date.fromisoformat(fup)-hoje).days
            lbl = (f"vencido há {abs(d)}d" if d<0 else "hoje" if d==0 else f"em {d}d")
            col1,col2,col3,col4 = st.columns([1.2,1.8,2.5,0.8])
            col1.caption(f"{fup} ({lbl})")
            col2.write(f"{TIPO_ICONE.get(tipo,'📞')} {entidade}")
            col3.caption(f"{VIA_ICONE.get(via,'')} {assunto[:55]}")
            if col4.button("📋 Abrir", key=f"ag_{cid}",
                           use_container_width=True):
                st.session_state["ct_aba"] = "lista"
                st.session_state["ct_topico_aberto"] = cid
                st.rerun()

    _bloco("🔴 Vencidos",        venc)
    _bloco("📌 Hoje",            hoje_l)
    _bloco("📅 Próximos 7 dias", prox)
    _bloco("🗓️ Mais adiante",   fut)


# ═══════════════════════════════════════════════════════
# 5. POR ENTIDADE
# ═══════════════════════════════════════════════════════
def _por_entidade():
    st.subheader("📊 Histórico por cliente / fornecedor")
    col1, col2 = st.columns(2)
    with col1:
        tipo_h = st.selectbox("Tipo", ["Cliente","Fornecedor"], key="he_tipo")
    with col2:
        if tipo_h == "Cliente":
            ents = query("""SELECT DISTINCT c.cliente_id, c.nome_fantasia
                FROM cliente c JOIN contato_registro cr ON cr.cliente_id=c.cliente_id
                WHERE cr.ativo=1 ORDER BY c.nome_fantasia""")
        else:
            ents = query("""SELECT DISTINCT f.fornecedor_id, f.nome_fantasia
                FROM fornecedor f JOIN contato_registro cr ON cr.fornecedor_id=f.fornecedor_id
                WHERE cr.ativo=1 ORDER BY f.nome_fantasia""")
        if not ents:
            st.info("Nenhum registro para este tipo ainda.")
            return
        ent_sel = st.selectbox("Selecione", ents,
                               format_func=lambda x: x[1], key="he_ent")

    if not ent_sel: return

    topicos = query(f"""
        SELECT cr.contato_id, cr.assunto, cr.status,
               COALESCE(cr.tipo_topico,'Contato'),
               cr.data_contato, cr.data_followup,
               (SELECT COUNT(*) FROM contato_interacao ci
                WHERE ci.contato_id=cr.contato_id AND ci.ativo=1)
        FROM contato_registro cr
        WHERE cr.{'cliente_id' if tipo_h=='Cliente' else 'fornecedor_id'}=?
          AND cr.ativo=1
        ORDER BY cr.data_contato DESC
    """, (ent_sel[0],))

    if not topicos:
        st.info(f"Nenhum registro para {ent_sel[1]}.")
        return

    total = len(topicos)
    conc  = sum(1 for r in topicos if r[2]=="Concluído")
    em_ab = total - conc

    c1,c2,c3 = st.columns(3)
    c1.metric("Total de tópicos", total)
    c2.metric("Concluídos",       conc)
    c3.metric("Em aberto",        em_ab)
    st.divider()

    for row in topicos:
        cid, assunto, status, tipo, data_c, followup, n_int = row
        aberto = st.session_state.get("ct_topico_aberto") == cid
        with st.container(border=True):
            c1,c2,c3,c4 = st.columns([3,1.5,1,0.8])
            c1.markdown(f"**{TIPO_ICONE.get(tipo,'📞')} {assunto}**")
            c1.caption(f"📅 {data_c}  |  💬 {n_int} interação(ões)")
            c2.caption(f"{STATUS_ICONE.get(status,'')} {status}")
            c3.caption(followup or "—")
            if c4.button("▼" if not aberto else "▲",
                         key=f"he_tog_{cid}", use_container_width=True):
                if aberto:
                    st.session_state.pop("ct_topico_aberto", None)
                else:
                    st.session_state["ct_topico_aberto"] = cid
                st.rerun()
            if aberto:
                _painel_topico(cid, status,
                               query("SELECT prioridade FROM contato_registro WHERE contato_id=?",
                                     (cid,))[0][0], tipo)


# ═══════════════════════════════════════════════════════
# 6. POR FORNECEDOR TRATADO
# ═══════════════════════════════════════════════════════
def _por_fornecedor():
    st.subheader("🏭 Por fornecedor tratado")
    st.caption("Tópicos onde o fornecedor foi parte da tratativa — independente de com quem o contato foi feito.")

    forns = query("""SELECT DISTINCT f.fornecedor_id, f.nome_fantasia
        FROM fornecedor f
        JOIN contato_x_fornecedor cxf ON f.fornecedor_id=cxf.fornecedor_id
        ORDER BY f.nome_fantasia""")

    if not forns:
        st.info("Nenhum tópico com fornecedor vinculado ainda.")
        return

    forn_sel = st.selectbox("Fornecedor", forns,
                            format_func=lambda x: x[1], key="pf_forn")
    if not forn_sel: return

    dados = query("""
        SELECT cr.contato_id, cr.assunto, cr.status,
               COALESCE(cr.tipo_topico,'Contato'),
               COALESCE(c.nome_fantasia, f2.nome_fantasia,'—') AS entidade,
               cr.tipo_entidade, cr.data_contato,
               (SELECT COUNT(*) FROM contato_interacao ci
                WHERE ci.contato_id=cr.contato_id AND ci.ativo=1)
        FROM contato_x_fornecedor cxf
        JOIN contato_registro cr ON cxf.contato_id=cr.contato_id
        LEFT JOIN cliente    c  ON cr.cliente_id    = c.cliente_id
        LEFT JOIN fornecedor f2 ON cr.fornecedor_id = f2.fornecedor_id
        WHERE cxf.fornecedor_id=? AND cr.ativo=1
        ORDER BY cr.data_contato DESC
    """, (forn_sel[0],))

    if not dados:
        st.info(f"Nenhum tópico registrado para {forn_sel[1]}.")
        return

    c1,c2,c3 = st.columns(3)
    c1.metric("Tópicos totais",  len(dados))
    c2.metric("Com clientes",    sum(1 for r in dados if r[5]=="cliente"))
    c3.metric("Diretos c/ forn.",sum(1 for r in dados if r[5]=="fornecedor"))
    st.divider()

    for row in dados:
        cid, assunto, status, tipo, entidade, tipo_ent, data_c, n_int = row
        ico = "👤" if tipo_ent=="cliente" else "🏭"
        aberto = st.session_state.get("ct_topico_aberto") == cid
        with st.container(border=True):
            col1,col2,col3,col4 = st.columns([3,1.5,1,0.8])
            col1.markdown(f"**{TIPO_ICONE.get(tipo,'📞')} {assunto}**")
            col1.caption(f"{ico} {entidade}  |  💬 {n_int} interação(ões)  |  📅 {data_c}")
            col2.caption(f"{STATUS_ICONE.get(status,'')} {status}")
            col3.caption(tipo)
            if col4.button("▼" if not aberto else "▲",
                           key=f"pf_tog_{cid}", use_container_width=True):
                if aberto:
                    st.session_state.pop("ct_topico_aberto", None)
                else:
                    st.session_state["ct_topico_aberto"] = cid
                st.rerun()
            if aberto:
                _painel_topico(cid, status,
                               query("SELECT prioridade FROM contato_registro WHERE contato_id=?",
                                     (cid,))[0][0], tipo)


# ═══════════════════════════════════════════════════════
# HELPERS PARA O DASHBOARD
# ═══════════════════════════════════════════════════════
def get_followups_vencidos():
    return query("""
        SELECT cr.contato_id,
               COALESCE(c.nome_fantasia, f.nome_fantasia,'—'),
               cr.assunto, cr.data_followup, cr.prioridade
        FROM contato_registro cr
        LEFT JOIN cliente    c ON cr.cliente_id    = c.cliente_id
        LEFT JOIN fornecedor f ON cr.fornecedor_id = f.fornecedor_id
        WHERE cr.ativo=1
          AND cr.data_followup < date('now')
          AND cr.status NOT IN ('Concluído','Cancelado')
        ORDER BY cr.data_followup ASC
    """) or []

def get_followups_hoje():
    return query("""
        SELECT cr.contato_id,
               COALESCE(c.nome_fantasia, f.nome_fantasia,'—'),
               cr.assunto, cr.prioridade
        FROM contato_registro cr
        LEFT JOIN cliente    c ON cr.cliente_id    = c.cliente_id
        LEFT JOIN fornecedor f ON cr.fornecedor_id = f.fornecedor_id
        WHERE cr.ativo=1
          AND cr.data_followup = date('now')
          AND cr.status NOT IN ('Concluído','Cancelado')
    """) or []

def get_negociacoes_urgentes():
    return query("""
        SELECT cr.contato_id,
               COALESCE(c.nome_fantasia,'—'),
               cr.assunto, cr.data_followup
        FROM contato_registro cr
        LEFT JOIN cliente c ON cr.cliente_id=c.cliente_id
        WHERE cr.ativo=1
          AND cr.tipo_topico='Negociação'
          AND cr.data_followup < date('now')
          AND cr.status NOT IN ('Concluído','Cancelado')
        ORDER BY cr.data_followup ASC
        LIMIT 5
    """) or []