from cache_helpers import cache_clientes, cache_categorias, cache_produtos_fornecedor
from database import query, conectar, _cache_fornecedores as _db_cache_fornecedores

def cache_fornecedores():
    """Wrapper que converte _DictRow para list serializável pelo st.cache_data."""
    rows = _db_cache_fornecedores()
    return [(r[0], r[1]) if not hasattr(r, 'keys') else (r['fornecedor_id'], r['nome_fantasia'])
            for r in rows]
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

    # Scroll para o topo quando sinalizado (ex: após salvar interação)
    if st.session_state.pop("_scroll_topo", False):
        st.components.v1.html(
            "<script>window.parent.document.querySelector('section.main').scrollTo(0,0);</script>",
            height=0)

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
    where = ["cr.ativo!=0"]
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
    # Filtro de periodo — datas calculadas em Python (compativel SQLite + PostgreSQL)
    _ult_int = """(SELECT MAX(ci.data_interacao) FROM contato_interacao ci
                   WHERE ci.contato_id=cr.contato_id AND ci.ativo!=0)"""
    if fil_periodo == "Hoje":
        where.append(f"(cr.data_contato = '2026-05-13' OR {_ult_int} = '2026-05-13')")
    elif fil_periodo == "Esta semana":
        where.append(f"(cr.data_contato >= '2026-05-06' OR {_ult_int} >= '2026-05-06')")
    elif fil_periodo == "Este mês":
        where.append(f"(cr.data_contato >= '2026-05-01' OR {_ult_int} >= '2026-05-01')")
    elif fil_periodo == "Últimos 30 dias":
        where.append(f"(cr.data_contato >= '2026-04-13' OR {_ult_int} >= '2026-04-13')")
    elif fil_periodo == "Últimos 90 dias":
        where.append(f"(cr.data_contato >= '2026-02-12' OR {_ult_int} >= '2026-02-12')")

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
                WHERE ci.contato_id=cr.contato_id AND ci.ativo!=0) AS n_int,
               (SELECT MAX(ci.data_interacao) FROM contato_interacao ci
                WHERE ci.contato_id=cr.contato_id AND ci.ativo!=0) AS ultima_int
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

    # ── Exportação PDF consolidado ────────────────────────────────────────
    with st.expander("📄 Exportar relatório PDF consolidado", expanded=False):
        col_modo, col_per2 = st.columns([2, 2])
        with col_modo:
            modo_int = st.radio(
                "Interações a incluir",
                ["Historico completo de cada topico",
                 "Apenas interacoes do periodo filtrado"],
                key="pdf_con_modo",
                help="Completo: todo o histórico do tópico. "
                     "Período: só as interações que caem no filtro de data.")
        with col_per2:
            # Datas do período para filtrar interações (só relevante no modo período)
            _usar_datas = "periodo" in modo_int.lower() or "periodo" in modo_int
            data_ini_pdf = st.date_input(
                "De", value=date.today() - timedelta(days=30),
                key="pdf_con_ini",
                disabled=("completo" in modo_int.lower()))
            data_fim_pdf = st.date_input(
                "Ate", value=date.today(),
                key="pdf_con_fim",
                disabled=("completo" in modo_int.lower()))

        # Monta descrição dos filtros aplicados para capa do PDF
        _filtros_desc = {
            "Periodo (topicos)": fil_periodo if fil_periodo != "Todos" else "Todos",
            "Fornecedor":        fil_forn[1] if fil_forn[0] else "Todos",
            "Tipo":              fil_tipo if fil_tipo != "Todos" else "Todos",
            "Status":            fil_status if fil_status != "Todos" else "Todos",
            "Prioridade":        fil_prior if fil_prior != "Todas" else "Todas",
            "Busca":             busca.strip() if busca.strip() else "—",
            "Historico":         ("Completo" if "completo" in modo_int.lower()
                                  else f"Periodo: {data_ini_pdf} a {data_fim_pdf}"),
            "Total de topicos":  str(len(topicos)),
        }
        _modo_key = ("completo" if "completo" in modo_int.lower() else "periodo")
        _ids = [row[0] for row in topicos]
        _pdf_con_key = f"pdf_con_cache_{hash(str(_ids)+_modo_key)}"

        if _pdf_con_key not in st.session_state:
            with st.spinner("Preparando PDF..."):
                _pdf_bytes = _gerar_pdf_consolidado(
                    _ids, _filtros_desc, _modo_key,
                    data_ini=data_ini_pdf.isoformat() if _modo_key=="periodo" else None,
                    data_fim=data_fim_pdf.isoformat() if _modo_key=="periodo" else None)
            st.session_state[_pdf_con_key] = _pdf_bytes

        _hoje_fn = date.today().strftime("%Y%m%d")
        _forn_fn = (fil_forn[1].replace(" ","_")[:15] if fil_forn[0] else "geral")
        st.download_button(
            label="⬇️ Baixar PDF",
            data=st.session_state[_pdf_con_key],
            file_name=f"contatos_{_forn_fn}_{_hoje_fn}.pdf",
            mime="application/pdf",
            key="pdf_con_dl",
            use_container_width=True,
            type="primary")

    for row in topicos:
        (cid, tipo, assunto, entidade, tipo_ent,
         status, prioridade, data_c, followup,
         fornecedores, n_int, ultima_int) = row

        aberto = st.session_state.get("ct_topico_aberto") == cid
        vencido = followup and followup < hoje and status not in ("Concluído","Cancelado")

        # Busca fornecedores do tópico com status individual
        _forns_topico = query("""
            SELECT cft.cft_id, cft.fornecedor_id, f.nome_fantasia,
                   cft.status, cft.tipo_topico, cft.prioridade, cft.data_followup
            FROM contato_fornecedor_topico cft
            JOIN fornecedor f ON f.fornecedor_id=cft.fornecedor_id
            WHERE cft.contato_id=? AND cft.ativo!=0
            ORDER BY f.nome_fantasia
        """, (cid,))

        # Fallback: se ainda não migrou, usa contato_x_fornecedor
        if not _forns_topico:
            _forns_topico_raw = query("""
                SELECT cxf.fornecedor_id, f.nome_fantasia
                FROM contato_x_fornecedor cxf
                JOIN fornecedor f ON f.fornecedor_id=cxf.fornecedor_id
                WHERE cxf.contato_id=?""", (cid,))
            _forns_topico = [(None, r[0], r[1], status, tipo, prioridade, followup)
                             for r in _forns_topico_raw]

        with st.container(border=True):
            c1, c2, c3, c4, c5 = st.columns([3.0, 4.8, 1.6, 0.35, 0.35])

            _edit_key = f"ct_edit_{cid}"
            _editando = st.session_state.get(_edit_key, False)

            with c1:
                if not _editando:
                    # Mostra status/tipo por fornecedor
                    for _ft in _forns_topico:
                        _cft_id, _fid, _fnome, _fst, _ftp, _fpr, _ffup = _ft
                        _tipo_ico = "📞" if _ftp == "Contato" else "🤝"
                        _pr_cor = "#e53935" if _fpr=="Alta" else "#fb8c00" if _fpr=="Média" else "#43a047"
                        st.markdown(
                            f"<div style='font-size:12px;line-height:1.7;padding:2px 0;"
                            f"border-left:3px solid {_pr_cor};padding-left:6px;margin-bottom:4px'>"
                            f"<b>{_fnome}</b><br/>"
                            f"{_tipo_ico} {_ftp or 'Contato'} · "
                            f"{STATUS_ICONE.get(_fst,'')} {_fst or 'A contatar'}"
                            f"</div>",
                            unsafe_allow_html=True)
                    if st.button("✏️", key=f"ct_edtbtn_{cid}",
                                 help="Editar fornecedores / status / prioridade"):
                        st.session_state[_edit_key] = True
                        st.rerun()
                else:
                    # Modo edição por fornecedor
                    for _ft in _forns_topico:
                        _cft_id, _fid, _fnome, _fst, _ftp, _fpr, _ffup = _ft
                        st.caption(f"**{_fnome}**")
                        _novo_tp = st.selectbox(f"Tipo", TIPO_TOPICO,
                            index=TIPO_TOPICO.index(_ftp) if _ftp in TIPO_TOPICO else 0,
                            key=f"ct_tipo_{cid}_{_fid}", label_visibility="collapsed")
                        _novo_st = st.selectbox(f"Status", STATUS_TOPICO,
                            index=STATUS_TOPICO.index(_fst) if _fst in STATUS_TOPICO else 0,
                            key=f"ct_st_{cid}_{_fid}", label_visibility="collapsed")
                        _novo_pr = st.selectbox(f"Prior.", PRIOR,
                            index=PRIOR.index(_fpr) if _fpr in PRIOR else 1,
                            key=f"ct_pr_{cid}_{_fid}", label_visibility="collapsed")
                        # Salva mudanças imediatamente ao detectar alteração
                        if _novo_tp != _ftp or _novo_st != _fst or _novo_pr != _fpr:
                            conn = conectar()
                            if _cft_id:
                                conn.execute("""UPDATE contato_fornecedor_topico
                                    SET tipo_topico=?, status=?, prioridade=?
                                    WHERE cft_id=?""",
                                    (_novo_tp, _novo_st, _novo_pr, _cft_id))
                            conn.commit(); conn.close()

                    col_sv, col_cx = st.columns(2)
                    if col_sv.button("✅ Salvar", key=f"ct_sv_{cid}",
                                     use_container_width=True):
                        # Atualiza status global do tópico com o pior status entre fornecedores
                        _status_ord = {s: i for i, s in enumerate(STATUS_TOPICO)}
                        _pior_status = min(
                            [_ft[3] or "A contatar" for _ft in _forns_topico],
                            key=lambda s: _status_ord.get(s, 99))
                        conn = conectar()
                        conn.execute("UPDATE contato_registro SET status=? WHERE contato_id=?",
                                     (_pior_status, cid))
                        conn.commit(); conn.close()
                        st.session_state.pop(_edit_key, None)
                        st.session_state["ct_msg"] = f"✅ '{assunto[:30]}' atualizado."
                        st.rerun()
                    if col_cx.button("✖️", key=f"ct_cx_{cid}",
                                     use_container_width=True):
                        st.session_state.pop(_edit_key, None)
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
                pr_cor = "#e53935" if prioridade=="Alta" else "#fb8c00" if prioridade=="Média" else "#43a047"
                _data_fmt = lambda d: (d[8:10]+"/"+d[5:7]+"/"+d[:4]) if d and len(d)>=10 else d or "—"
                _fup_str  = _data_fmt(followup) if followup else "—"
                _ult_str  = _data_fmt(ultima_int or data_c)
                st.markdown(
                    f"<div style='font-size:13px;line-height:1.9;color:#444;padding-left:6px'>"
                    f"<span style='color:{pr_cor};font-size:16px;font-weight:900'>●</span> "
                    f"{prioridade}<br/>"
                    f"<span style='font-size:12px'>📅 {_fup_str}<br/>"
                    f"💬 {n_int}x · {_ult_str}</span>"
                    f"</div>",
                    unsafe_allow_html=True)

            with c4:
                label = "▲" if aberto else "▼"
                if st.button(label, key=f"tog_{cid}", use_container_width=True,
                             help="Ver histórico e interações"):
                    if aberto:
                        st.session_state.pop("ct_topico_aberto", None)
                    else:
                        st.session_state["ct_topico_aberto"] = cid
                    st.rerun()

            with c5:
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
    """Delega para o painel completo que já existe mais abaixo no módulo."""
    _painel_topico_completo(cid, status_atual, prioridade_atual, tipo_atual)


def _gerar_pdf_topico(cid, fornecedor_id=None):
    """
    Gera PDF estruturado com o histórico de um tópico de contato.
    fornecedor_id: se informado, filtra interações daquele fornecedor.
    Retorna bytes do PDF prontos para st.download_button.
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table, TableStyle, HRFlowable)
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    import io as _io

    # ── Busca dados ───────────────────────────────────────
    cr = query("""
        SELECT cr.assunto, cr.tipo_topico, cr.status, cr.prioridade,
               cr.data_contato, cr.data_followup, cr.observacao,
               COALESCE(c.nome_fantasia, f.nome_fantasia, '—') AS entidade,
               cr.tipo_entidade
        FROM contato_registro cr
        LEFT JOIN cliente    c ON cr.cliente_id    = c.cliente_id
        LEFT JOIN fornecedor f ON cr.fornecedor_id = f.fornecedor_id
        WHERE cr.contato_id=?""", (cid,))
    if not cr:
        return None
    r = cr[0]
    assunto, tipo, status, prioridade, data_c, followup, obs, entidade, tipo_ent = r

    forns = query("""
        SELECT fn.nome_fantasia FROM contato_x_fornecedor cxf
        JOIN fornecedor fn ON cxf.fornecedor_id=fn.fornecedor_id
        WHERE cxf.contato_id=?""", (cid,))
    forns_str = " / ".join(f[0] for f in forns) if forns else "—"

    # Busca interações filtradas por fornecedor se informado
    if fornecedor_id:
        ints = query("""
            SELECT ci.data_interacao, ci.via_comunicacao, ci.contato_pessoa,
                   ci.descricao, ci.resultado, ci.data_followup, ci.ativo
            FROM contato_interacao ci
            WHERE ci.contato_id=?
              AND (ci.fornecedor_id=? OR ci.fornecedor_id IS NULL)
            ORDER BY ci.data_interacao ASC""", (cid, fornecedor_id))
    else:
        ints = query("""
            SELECT ci.data_interacao, ci.via_comunicacao, ci.contato_pessoa,
                   ci.descricao, ci.resultado, ci.data_followup, ci.ativo
            FROM contato_interacao ci
            WHERE ci.contato_id=?
            ORDER BY ci.data_interacao ASC""", (cid,))

    # Filtra inativos em Python — compatível SQLite e PostgreSQL
    ints = [r for r in ints if r['ativo'] not in (0, False, '0')] if ints else []

    # ── Estilos ───────────────────────────────────────────
    buf  = _io.BytesIO()
    doc  = SimpleDocTemplate(buf, pagesize=A4,
                             leftMargin=2*cm, rightMargin=2*cm,
                             topMargin=2*cm, bottomMargin=2*cm)
    estilos = getSampleStyleSheet()

    VERDE   = colors.HexColor("#2E7D32")
    VERDE_L = colors.HexColor("#E8F5E9")
    CINZA   = colors.HexColor("#F5F5F5")
    TEXTO   = colors.HexColor("#212121")

    s_titulo = ParagraphStyle("titulo", parent=estilos["Title"],
                               fontSize=16, textColor=VERDE,
                               spaceAfter=4, leading=20)
    s_sub    = ParagraphStyle("sub", parent=estilos["Normal"],
                               fontSize=10, textColor=colors.HexColor("#555555"),
                               spaceAfter=2)
    s_label  = ParagraphStyle("label", parent=estilos["Normal"],
                               fontSize=8, textColor=colors.HexColor("#777777"),
                               spaceBefore=0, spaceAfter=1)
    s_valor  = ParagraphStyle("valor", parent=estilos["Normal"],
                               fontSize=10, textColor=TEXTO,
                               spaceBefore=0, spaceAfter=6)
    s_inter_titulo = ParagraphStyle("inter_t", parent=estilos["Normal"],
                                    fontSize=10, textColor=VERDE,
                                    fontName="Helvetica-Bold", spaceAfter=3)
    s_inter_texto  = ParagraphStyle("inter_tx", parent=estilos["Normal"],
                                    fontSize=9, textColor=TEXTO,
                                    spaceAfter=3, leading=13)
    s_rodape = ParagraphStyle("rodape", parent=estilos["Normal"],
                               fontSize=7, textColor=colors.HexColor("#999999"),
                               alignment=TA_CENTER)

    VIA_LABEL = {"WhatsApp":"WhatsApp","E-mail":"E-mail",
                 "Telefone":"Telefone","Visita presencial":"Visita presencial",
                 "Reuniao":"Reuniao","Videoconferencia":"Videoconferencia",
                 "Outro":"Outro"}

    def _fmt_data(d):
        """Converte AAAA-MM-DD para DD/MM/AAAA."""
        if not d: return "—"
        try: return f"{str(d)[8:10]}/{str(d)[5:7]}/{str(d)[:4]}"
        except: return str(d)

    from datetime import date as _date
    hoje_str = _date.today().strftime("%d/%m/%Y")

    elementos = []

    # ── Cabeçalho ─────────────────────────────────────────
    elementos.append(Paragraph("PepperCRM — Histórico de Contato", s_titulo))
    elementos.append(Paragraph(
        f"Gerado em {hoje_str}  |  Tópico #{cid}", s_sub))
    elementos.append(HRFlowable(width="100%", thickness=1.5,
                                color=VERDE, spaceAfter=10))

    # ── Ficha do tópico ───────────────────────────────────
    ico_ent = "Cliente" if tipo_ent == "cliente" else "Fornecedor"
    ficha = [
        ["Assunto",    assunto or "—",
         "Tipo",       tipo or "Contato"],
        [ico_ent,      entidade,
         "Status",     status or "—"],
        ["Prioridade", prioridade or "—",
         "Data inicio", _fmt_data(data_c)],
        ["Prox. contato", _fmt_data(followup),
         "Fornecedores tratados", forns_str],
    ]
    if obs:
        ficha.append(["Observacao", obs, "", ""])

    t_ficha = Table(
        [[Paragraph(f"<b>{cel}</b>" if i % 2 == 0 else cel,
                    s_label if i % 2 == 0 else s_valor)
          for i, cel in enumerate(linha)]
         for linha in ficha],
        colWidths=[3.2*cm, 7.5*cm, 3.2*cm, 3.5*cm])
    t_ficha.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), CINZA),
        ("ROWBACKGROUND", (0,0), (-1,-1), [CINZA, colors.white]),
        ("BOX",      (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ("INNERGRID",(0,0), (-1,-1), 0.3, colors.HexColor("#DDDDDD")),
        ("VALIGN",   (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
    ]))
    elementos.append(t_ficha)
    elementos.append(Spacer(1, 0.5*cm))

    # ── Linha do tempo ────────────────────────────────────
    elementos.append(HRFlowable(width="100%", thickness=1,
                                color=VERDE_L, spaceAfter=6))
    elementos.append(Paragraph(
        f"<b>Linha do tempo — {len(ints)} interação(ões)</b>", s_inter_titulo))
    elementos.append(Spacer(1, 0.2*cm))

    if not ints:
        elementos.append(Paragraph("Nenhuma interação registrada.", s_inter_texto))
    else:
        for idx, irow in enumerate(ints, 1):
            data_i, via, pessoa, desc, result, fup_i = irow[:6] if not hasattr(irow, 'keys') else (irow['data_interacao'], irow['via_comunicacao'], irow['contato_pessoa'], irow['descricao'], irow['resultado'], irow['data_followup'])
            via_lbl = VIA_LABEL.get(via, via or "—")
            cabecalho = f"<b>#{idx} — {_fmt_data(data_i)}  |  {via_lbl}"
            if pessoa:
                cabecalho += f"  |  {pessoa}"
            cabecalho += "</b>"

            dados_int = [[
                Paragraph(cabecalho, s_inter_titulo),
            ]]
            linhas_int = [dados_int[0]]

            if desc:
                linhas_int.append([
                    Paragraph(f"<b>O que foi tratado:</b><br/>{desc}", s_inter_texto)
                ])
            if result:
                linhas_int.append([
                    Paragraph(f"<b>Resultado / proximo passo:</b><br/>{result}", s_inter_texto)
                ])
            if fup_i:
                linhas_int.append([
                    Paragraph(f"Proximo contato agendado: <b>{_fmt_data(fup_i)}</b>", s_inter_texto)
                ])

            t_int = Table(linhas_int, colWidths=[17.1*cm])
            bg = VERDE_L if idx % 2 == 0 else colors.white
            t_int.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,-1), bg),
                ("BOX",      (0,0), (-1,-1), 0.5, colors.HexColor("#C8E6C9")),
                ("TOPPADDING",   (0,0), (-1,-1), 6),
                ("BOTTOMPADDING",(0,0), (-1,-1), 6),
                ("LEFTPADDING",  (0,0), (-1,-1), 8),
                ("RIGHTPADDING", (0,0), (-1,-1), 8),
            ]))
            elementos.append(t_int)
            elementos.append(Spacer(1, 0.2*cm))

    # ── Rodapé ────────────────────────────────────────────
    elementos.append(Spacer(1, 0.5*cm))
    elementos.append(HRFlowable(width="100%", thickness=0.5,
                                color=colors.HexColor("#CCCCCC"), spaceAfter=4))
    elementos.append(Paragraph(
        f"PepperCRM — Azevedo e Filhos Representação Comercial  |  "
        f"Documento gerado em {hoje_str}  |  Confidencial",
        s_rodape))

    doc.build(elementos)
    buf.seek(0)
    return buf.read()


def _gerar_pdf_consolidado(topicos_ids, filtros_desc, modo_interacoes,
                           data_ini=None, data_fim=None):
    """
    Gera PDF consolidado com múltiplos tópicos.
    modo_interacoes: 'periodo' = só interações do período
                     'completo' = histórico completo de cada tópico
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table, TableStyle, HRFlowable, PageBreak)
    from reportlab.lib.enums import TA_CENTER
    import io as _io
    from datetime import date as _date

    buf = _io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    VERDE   = colors.HexColor("#2E7D32")
    VERDE_L = colors.HexColor("#E8F5E9")
    CINZA   = colors.HexColor("#F5F5F5")
    TEXTO   = colors.HexColor("#212121")
    LARANJA = colors.HexColor("#E65100")

    estilos = getSampleStyleSheet()
    s_capa_titulo = ParagraphStyle("ct", parent=estilos["Title"],
                                   fontSize=20, textColor=VERDE,
                                   spaceAfter=6, leading=24)
    s_capa_sub  = ParagraphStyle("cs", parent=estilos["Normal"],
                                 fontSize=11, textColor=colors.HexColor("#555"),
                                 spaceAfter=4)
    s_topico_h  = ParagraphStyle("th", parent=estilos["Normal"],
                                 fontSize=12, textColor=VERDE,
                                 fontName="Helvetica-Bold", spaceAfter=4,
                                 spaceBefore=6)
    s_label     = ParagraphStyle("lb", parent=estilos["Normal"],
                                 fontSize=8, textColor=colors.HexColor("#777"),
                                 spaceAfter=1)
    s_valor     = ParagraphStyle("vl", parent=estilos["Normal"],
                                 fontSize=10, textColor=TEXTO,
                                 spaceAfter=4)
    s_inter_t   = ParagraphStyle("it", parent=estilos["Normal"],
                                 fontSize=10, textColor=VERDE,
                                 fontName="Helvetica-Bold", spaceAfter=3)
    s_inter_tx  = ParagraphStyle("itx", parent=estilos["Normal"],
                                 fontSize=9, textColor=TEXTO,
                                 spaceAfter=3, leading=13)
    s_total_h   = ParagraphStyle("toh", parent=estilos["Normal"],
                                 fontSize=11, textColor=LARANJA,
                                 fontName="Helvetica-Bold", spaceAfter=4,
                                 spaceBefore=8)
    s_rodape    = ParagraphStyle("rp", parent=estilos["Normal"],
                                 fontSize=7, textColor=colors.HexColor("#999"),
                                 alignment=TA_CENTER)

    VIA_LABEL = {"WhatsApp":"WhatsApp","E-mail":"E-mail","Telefone":"Telefone",
                 "Visita presencial":"Visita presencial","Reuniao":"Reuniao",
                 "Reunião":"Reuniao","Videoconferencia":"Videoconferencia",
                 "Videoconferência":"Videoconferencia","Outro":"Outro"}

    def _fd(d):
        if not d: return "—"
        try: return f"{str(d)[8:10]}/{str(d)[5:7]}/{str(d)[:4]}"
        except: return str(d)

    hoje_str = _date.today().strftime("%d/%m/%Y")
    elementos = []

    # ── CAPA ─────────────────────────────────────────────
    elementos.append(Spacer(1, 1*cm))
    elementos.append(Paragraph("PepperCRM", s_capa_titulo))
    elementos.append(Paragraph("Relatorio de Contatos e Negociacoes", s_capa_sub))
    elementos.append(HRFlowable(width="100%", thickness=2, color=VERDE, spaceAfter=12))

    # Filtros aplicados
    filtros_rows = [[Paragraph(f"<b>{k}</b>", s_label),
                     Paragraph(v, s_valor)]
                    for k, v in filtros_desc.items()]
    t_filtros = Table(filtros_rows, colWidths=[4*cm, 13.1*cm])
    t_filtros.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), CINZA),
        ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#CCC")),
        ("INNERGRID", (0,0), (-1,-1), 0.3, colors.HexColor("#DDD")),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    elementos.append(t_filtros)
    elementos.append(Spacer(1, 0.5*cm))

    # Totais gerais (calculados depois — placeholder, preenchido abaixo)
    total_topicos   = len(topicos_ids)
    total_interacoes = 0
    contagem_via    = {}
    contagem_forn   = {}

    # ── TÓPICOS ───────────────────────────────────────────
    elementos.append(PageBreak())

    for idx_t, cid in enumerate(topicos_ids, 1):
        cr = query("""
            SELECT cr.assunto, cr.tipo_topico, cr.status, cr.prioridade,
                   cr.data_contato, cr.data_followup, cr.observacao,
                   COALESCE(c.nome_fantasia, f.nome_fantasia, '—') AS entidade,
                   cr.tipo_entidade
            FROM contato_registro cr
            LEFT JOIN cliente    c ON cr.cliente_id    = c.cliente_id
            LEFT JOIN fornecedor f ON cr.fornecedor_id = f.fornecedor_id
            WHERE cr.contato_id=?""", (cid,))
        if not cr: continue
        assunto, tipo, status, prioridade, data_c, followup, obs, entidade, tipo_ent = cr[0]

        forns = query("""SELECT fn.nome_fantasia FROM contato_x_fornecedor cxf
            JOIN fornecedor fn ON cxf.fornecedor_id=fn.fornecedor_id
            WHERE cxf.contato_id=?""", (cid,))
        forns_str = " / ".join(f[0] for f in forns) if forns else "—"
        for f in forns:
            contagem_forn[f[0]] = contagem_forn.get(f[0], 0) + 1

        # Busca interações conforme modo
        if modo_interacoes == "periodo" and data_ini and data_fim:
            ints = query("""
                SELECT ci.data_interacao, ci.via_comunicacao, ci.contato_pessoa,
                       ci.descricao, ci.resultado, ci.data_followup, ci.ativo
                FROM contato_interacao ci
                WHERE ci.contato_id=?
                  AND ci.data_interacao >= ? AND ci.data_interacao <= ?
                ORDER BY ci.data_interacao ASC""", (cid, data_ini, data_fim))
        else:
            ints = query("""
                SELECT ci.data_interacao, ci.via_comunicacao, ci.contato_pessoa,
                       ci.descricao, ci.resultado, ci.data_followup, ci.ativo
                FROM contato_interacao ci
                WHERE ci.contato_id=?
                ORDER BY ci.data_interacao ASC""", (cid,))

        # Filtra inativos em Python
        ints = [r for r in ints if r['ativo'] not in (0, False, '0')] if ints else []

        total_interacoes += len(ints)
        for irow in ints:
            via = irow[1] or "Outro"
            contagem_via[via] = contagem_via.get(via, 0) + 1

        # Cabeçalho do tópico + ficha resumida agrupados para nunca ficarem órfãos
        from reportlab.platypus import KeepTogether as _KT

        _bloco_cabecalho = []
        _bloco_cabecalho.append(HRFlowable(width="100%", thickness=1,
                                           color=VERDE_L, spaceAfter=4))
        _bloco_cabecalho.append(Paragraph(
            f"#{idx_t}  {assunto or '—'}", s_topico_h))

        # Ficha resumida
        ico_ent = "Cliente" if tipo_ent == "cliente" else "Fornecedor"
        ficha = [
            ["Tipo", tipo or "Contato", "Status", status or "—"],
            [ico_ent, entidade, "Prioridade", prioridade or "—"],
            ["Data inicio", _fd(data_c), "Prox. contato", _fd(followup)],
            ["Fornecedores", forns_str, "Interacoes", str(len(ints))],
        ]
        if obs:
            ficha.append(["Observacao", obs, "", ""])
        t_f = Table(
            [[Paragraph(f"<b>{c}</b>" if i%2==0 else c,
                        s_label if i%2==0 else s_valor)
              for i,c in enumerate(linha)]
             for linha in ficha],
            colWidths=[3*cm, 6.5*cm, 3*cm, 4.6*cm])
        t_f.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), CINZA),
            ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#CCC")),
            ("INNERGRID", (0,0), (-1,-1), 0.3, colors.HexColor("#DDD")),
            ("TOPPADDING", (0,0), (-1,-1), 4),
            ("BOTTOMPADDING", (0,0), (-1,-1), 4),
            ("LEFTPADDING", (0,0), (-1,-1), 6),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
        ]))
        _bloco_cabecalho.append(t_f)
        _bloco_cabecalho.append(Spacer(1, 0.3*cm))

        # Label "Histórico" fica junto ao cabeçalho para não ficar solto
        modo_lbl = "do periodo" if modo_interacoes == "periodo" else "completo"
        _bloco_cabecalho.append(Paragraph(
            f"<b>Historico {modo_lbl} — {len(ints)} interacao(oes)</b>", s_inter_t))

        elementos.append(_KT(_bloco_cabecalho))

        if not ints:
            elementos.append(Paragraph(
                "Nenhuma interacao no periodo selecionado.", s_inter_tx))
        else:
            for idx_i, irow in enumerate(ints, 1):
                data_i, via, pessoa, desc, result, fup_i = irow[:6] if not hasattr(irow, 'keys') else (irow['data_interacao'], irow['via_comunicacao'], irow['contato_pessoa'], irow['descricao'], irow['resultado'], irow['data_followup'])
                via_lbl = VIA_LABEL.get(via, via or "—")
                cab = f"<b>#{idx_i} — {_fd(data_i)}  |  {via_lbl}"
                if pessoa: cab += f"  |  {pessoa}"
                cab += "</b>"
                linhas = [[Paragraph(cab, s_inter_t)]]
                if desc:
                    linhas.append([Paragraph(
                        f"<b>O que foi tratado:</b><br/>{desc}", s_inter_tx)])
                if result:
                    linhas.append([Paragraph(
                        f"<b>Resultado / proximo passo:</b><br/>{result}", s_inter_tx)])
                if fup_i:
                    linhas.append([Paragraph(
                        f"Proximo contato: <b>{_fd(fup_i)}</b>", s_inter_tx)])
                t_i = Table(linhas, colWidths=[17.1*cm])
                bg = VERDE_L if idx_i % 2 == 0 else colors.white
                t_i.setStyle(TableStyle([
                    ("BACKGROUND", (0,0), (-1,-1), bg),
                    ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#C8E6C9")),
                    ("TOPPADDING", (0,0), (-1,-1), 5),
                    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
                    ("LEFTPADDING", (0,0), (-1,-1), 8),
                    ("RIGHTPADDING", (0,0), (-1,-1), 8),
                ]))
                elementos.append(t_i)
                elementos.append(Spacer(1, 0.15*cm))

        elementos.append(Spacer(1, 0.4*cm))

    # ── TOTALIZADOR ───────────────────────────────────────
    elementos.append(PageBreak())
    elementos.append(Paragraph("Resumo Geral", s_total_h))
    elementos.append(HRFlowable(width="100%", thickness=1.5,
                                color=LARANJA, spaceAfter=8))

    resumo = [
        ["Topicos incluidos", str(total_topicos)],
        ["Total de interacoes", str(total_interacoes)],
    ]
    t_res = Table(resumo, colWidths=[8*cm, 9.1*cm])
    t_res.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), CINZA),
        ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#CCC")),
        ("INNERGRID", (0,0), (-1,-1), 0.3, colors.HexColor("#DDD")),
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]))
    elementos.append(t_res)
    elementos.append(Spacer(1, 0.4*cm))

    if contagem_via:
        elementos.append(Paragraph("<b>Interacoes por via:</b>", s_inter_t))
        rows_via = [[Paragraph(f"<b>{via}</b>", s_label),
                     Paragraph(str(qtd), s_valor)]
                    for via, qtd in sorted(contagem_via.items(),
                                          key=lambda x: -x[1])]
        t_via = Table(rows_via, colWidths=[8*cm, 9.1*cm])
        t_via.setStyle(TableStyle([
            ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#CCC")),
            ("INNERGRID", (0,0), (-1,-1), 0.3, colors.HexColor("#DDD")),
            ("TOPPADDING", (0,0), (-1,-1), 4),
            ("BOTTOMPADDING", (0,0), (-1,-1), 4),
            ("LEFTPADDING", (0,0), (-1,-1), 8),
        ]))
        elementos.append(t_via)
        elementos.append(Spacer(1, 0.4*cm))

    if contagem_forn:
        elementos.append(Paragraph("<b>Topicos por fornecedor:</b>", s_inter_t))
        rows_forn = [[Paragraph(f"<b>{fn}</b>", s_label),
                      Paragraph(str(qtd), s_valor)]
                     for fn, qtd in sorted(contagem_forn.items(),
                                           key=lambda x: -x[1])]
        t_forn = Table(rows_forn, colWidths=[8*cm, 9.1*cm])
        t_forn.setStyle(TableStyle([
            ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#CCC")),
            ("INNERGRID", (0,0), (-1,-1), 0.3, colors.HexColor("#DDD")),
            ("TOPPADDING", (0,0), (-1,-1), 4),
            ("BOTTOMPADDING", (0,0), (-1,-1), 4),
            ("LEFTPADDING", (0,0), (-1,-1), 8),
        ]))
        elementos.append(t_forn)

    # ── Rodapé ────────────────────────────────────────────
    elementos.append(Spacer(1, 0.8*cm))
    elementos.append(HRFlowable(width="100%", thickness=0.5,
                                color=colors.HexColor("#CCC"), spaceAfter=4))
    elementos.append(Paragraph(
        f"PepperCRM — Azevedo e Filhos Representacao Comercial  |  "
        f"Gerado em {hoje_str}  |  Confidencial", s_rodape))

    doc.build(elementos)
    buf.seek(0)
    return buf.read()


def _painel_topico_completo(cid, status_atual, prioridade_atual, tipo_atual):
    """Painel completo com separação por fornecedor."""
    st.divider()

    _msg_inline = st.session_state.pop(f"ct_msg_inline_{cid}", None)
    if _msg_inline:
        st.success(_msg_inline)

    # ── Fornecedores do tópico ────────────────────────────────────────────
    # Tenta contato_fornecedor_topico primeiro, fallback para contato_x_fornecedor
    _forns_pan = []
    try:
        _forns_pan = query("""
            SELECT cft.cft_id, cft.fornecedor_id, f.nome_fantasia,
                   cft.status, cft.tipo_topico, cft.prioridade, cft.data_followup
            FROM contato_fornecedor_topico cft
            JOIN fornecedor f ON f.fornecedor_id=cft.fornecedor_id
            WHERE cft.contato_id=? AND cft.ativo!=0
            ORDER BY f.nome_fantasia
        """, (cid,))
    except Exception:
        pass

    if not _forns_pan:
        try:
            _raw = query("""SELECT cxf.fornecedor_id, f.nome_fantasia
                FROM contato_x_fornecedor cxf
                JOIN fornecedor f ON f.fornecedor_id=cxf.fornecedor_id
                WHERE cxf.contato_id=?""", (cid,))
            _forns_pan = [(None, r[0], r[1], status_atual,
                           tipo_atual, prioridade_atual, None) for r in _raw]
        except Exception:
            pass

    _forn_opts = [(ft[1], ft[2]) for ft in _forns_pan] if _forns_pan else []

    # Seletor de fornecedor + botão PDF
    col_fsel, col_pdf = st.columns([3, 2])
    with col_fsel:
        if len(_forn_opts) > 1:
            _fsel_idx = st.selectbox(
                "📋 Ver interações de:",
                range(len(_forn_opts)),
                format_func=lambda i: _forn_opts[i][1],
                key=f"forn_sel_painel_{cid}")
        else:
            _fsel_idx = 0
        _forn_id_ativo   = _forn_opts[_fsel_idx][0] if _forn_opts else None
        _forn_nome_ativo = _forn_opts[_fsel_idx][1] if _forn_opts else "Geral"

    # PDF por fornecedor
    _pdf_key      = f"pdf_cache_v2_{cid}_{_forn_id_ativo}"
    _pdf_nome_key = f"pdf_nome_v2_{cid}_{_forn_id_ativo}"
    if _pdf_key not in st.session_state:
        with st.spinner("Preparando PDF..."):
            _pdf_bytes = _gerar_pdf_topico(cid, _forn_id_ativo)
        if _pdf_bytes:
            _ass  = query("SELECT assunto FROM contato_registro WHERE contato_id=?", (cid,))
            _nome = (_ass[0][0] or f"topico_{cid}") if _ass else f"topico_{cid}"
            _nome = "".join(c for c in _nome if c.isalnum() or c in " _-")[:40].strip()
            st.session_state[_pdf_key]      = _pdf_bytes
            st.session_state[_pdf_nome_key] = _nome
    with col_pdf:
        if _pdf_key in st.session_state:
            st.download_button(
                label=f"📄 PDF — {_forn_nome_ativo}",
                data=st.session_state[_pdf_key],
                file_name=f"historico_{st.session_state.get(_pdf_nome_key,cid)}_{_forn_nome_ativo[:10]}.pdf",
                mime="application/pdf",
                key=f"pdf_dl_{cid}_{_forn_id_ativo}",
                use_container_width=True)
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
            st.session_state[f"ct_msg_inline_{cid}"] = "✅ Tópico atualizado."
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

    # Busca todas as interações do tópico (sem filtro ativo para máxima compatibilidade)
    try:
        ints = query("""SELECT ci.interacao_id, ci.data_interacao, ci.via_comunicacao,
                   ci.contato_pessoa, ci.descricao, ci.resultado, ci.data_followup
            FROM contato_interacao ci
            WHERE ci.contato_id=?
            ORDER BY ci.data_interacao DESC""", (cid,))
        # Filtra em Python para máxima compatibilidade SQLite/PostgreSQL
        ints = [r for r in ints if r['ativo'] not in (0, False, '0')] if ints and hasattr(ints[0], 'keys') and 'ativo' in ints[0].keys() else ints
    except Exception as _ex:
        st.warning(f"Erro ao buscar interações: {_ex}")
        ints = []

    if ints:
        st.markdown(f"**📅 Histórico — {len(ints)} interação(ões)**")
        for irow in ints:
            # Acesso defensivo — suporta DictRow e tuple
            def _g(r, k, i): 
                try: return r[k]
                except: 
                    try: return r[i]
                    except: return None
            iid    = _g(irow, 'interacao_id', 0)
            data_i = _g(irow, 'data_interacao', 1)
            via    = _g(irow, 'via_comunicacao', 2)
            pessoa = _g(irow, 'contato_pessoa', 3)
            desc   = _g(irow, 'descricao', 4)
            result = _g(irow, 'resultado', 5)
            fup    = _g(irow, 'data_followup', 6)
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
                    st.session_state[f"ct_msg_inline_{cid}"] = "✅ Interação atualizada."
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
        st.info("Ainda sem interações registradas. Registre a primeira abaixo.")

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
        _fup_val = _fup.isoformat() if _fup and hasattr(_fup,'isoformat') else None

        conn = conectar()
        # Grava interação com fornecedor_id do fornecedor selecionado no painel
        conn.execute("""INSERT INTO contato_interacao
            (contato_id, fornecedor_id, data_interacao, via_comunicacao,
             contato_pessoa, contato_cliente_id,
             descricao, resultado, data_followup, ativo)
            VALUES (?,?,?,?,?,?,?,?,?,1)""",
            (cid, _forn_id_ativo,
             _dt.isoformat() if hasattr(_dt,'isoformat') else str(_dt),
             _via, pessoa_nome or None, novo_ct_id or ct_cli_id,
             _dc or None, _re or None, _fup_val))

        # Atualiza status/tipo/followup no contato_fornecedor_topico deste fornecedor
        _cft_row = query("""SELECT cft_id FROM contato_fornecedor_topico
            WHERE contato_id=? AND fornecedor_id=?""", (cid, _forn_id_ativo))
        if _cft_row:
            conn.execute("""UPDATE contato_fornecedor_topico
                SET status=?, tipo_topico=?, data_followup=?
                WHERE cft_id=?""",
                (_nst, _ntp, _fup_val, _cft_row[0][0]))
        # Atualiza status global do tópico (pior status entre fornecedores)
        if _fup_val:
            conn.execute("""UPDATE contato_registro
                SET status=?, tipo_topico=?, data_followup=? WHERE contato_id=?""",
                (_nst, _ntp, _fup_val, cid))
        else:
            conn.execute("""UPDATE contato_registro
                SET status=?, tipo_topico=? WHERE contato_id=?""",
                (_nst, _ntp, cid))
        conn.commit(); conn.close()

        for k in [f"ncn_{cid}",f"ncc_{cid}",f"ncf_{cid}",f"ncw_{cid}",f"nce_{cid}"]:
            st.session_state.pop(k, None)
        st.session_state[_mk] = "sel"
        st.session_state.pop(f"exp_inter_{cid}", None)
        # Invalida cache do PDF deste fornecedor
        st.session_state.pop(f"pdf_cache_{cid}_{_forn_id_ativo}", None)
        st.session_state.pop(f"pdf_nome_{cid}_{_forn_id_ativo}", None)
        st.session_state.pop("ct_topico_aberto", None)
        st.session_state["ct_msg"] = "✅ Interação registrada com sucesso!"
        st.session_state["_scroll_topo"] = True
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

    from database import _cache_todos_clientes
    clientes = [(r[0],r[1],None) for r in _cache_todos_clientes()]
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
                WHERE ci.contato_id=cr.contato_id AND ci.ativo!=0)
        FROM contato_registro cr
        WHERE cr.{'cliente_id' if tipo_h=='Cliente' else 'fornecedor_id'}=?
          AND cr.ativo!=0
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
                WHERE ci.contato_id=cr.contato_id AND ci.ativo!=0)
        FROM contato_x_fornecedor cxf
        JOIN contato_registro cr ON cxf.contato_id=cr.contato_id
        LEFT JOIN cliente    c  ON cr.cliente_id    = c.cliente_id
        LEFT JOIN fornecedor f2 ON cr.fornecedor_id = f2.fornecedor_id
        WHERE cxf.fornecedor_id=? AND cr.ativo!=0
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
          AND cr.data_followup < '2026-05-13'
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
          AND cr.data_followup = '2026-05-13'
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
          AND cr.data_followup < '2026-05-13'
          AND cr.status NOT IN ('Concluído','Cancelado')
        ORDER BY cr.data_followup ASC
        LIMIT 5
    """) or []