# catalogo.py — PepperCRM
# Catálogo digital PDF por fornecedor + WhatsApp com biblioteca de mensagens

import streamlit as st
import io, os
from datetime import date, datetime
from database import conectar, query

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
def tela_catalogo():
    st.header("📄 Catálogo PDF")
    if st.button("⬅ Voltar"): _ir("home")
    st.divider()
    msg = st.session_state.pop("cat_msg", None)
    if msg: st.success(msg)
    _tela_catalogo()


# ═══════════════════════════════════════════════════════
# 1. CATÁLOGO PDF
# ═══════════════════════════════════════════════════════
def _tela_catalogo():
    st.subheader("Gerar catálogo de produtos")

    forns = query("SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia")
    if not forns:
        st.info("Nenhum fornecedor cadastrado.")
        return

    col1, col2 = st.columns(2)
    with col1:
        forn_sel = st.selectbox("Fornecedor", forns,
                                format_func=lambda x: x[1], key="cat_forn")
    with col2:
        # Tabela de preços disponíveis
        tabelas = query("""SELECT tabela_preco_id, nome_tabela, tipo_tabela
            FROM tabela_preco
            WHERE fornecedor_id=? AND ativo=1 ORDER BY nome_tabela""",
            (forn_sel[0],))
        tab_opts = [(None, "— sem tabela de preços —")] + \
                   [(t[0], f"{t[1]} ({t[2]})") for t in tabelas]
        tab_sel = st.selectbox("Incluir tabela de preços",
                               tab_opts, format_func=lambda x: x[1],
                               key="cat_tab")

    st.markdown("**Ordenação e agrupamento dos produtos:**")
    col3, col4, col5 = st.columns(3)
    with col3:
        agrupar = st.selectbox("Agrupar por",
                               ["Categoria", "Linha", "Sub-categoria", "Grupo", "Sem agrupamento"],
                               key="cat_grupo")
    with col4:
        ordenar = st.selectbox("Ordenar por",
                               ["Descrição", "Código", "Categoria → Descrição",
                                "Linha → Descrição", "Grupo → Descrição"],
                               key="cat_ordem")
    with col5:
        incluir_inativos = st.checkbox("Incluir inativos", value=False, key="cat_inat")

    st.markdown("**Informações a exibir:**")
    col6, col7, col8 = st.columns(3)
    with col6:
        show_cod   = st.checkbox("Código do produto", value=True, key="cat_scod")
        show_peso  = st.checkbox("Peso / volume", value=True, key="cat_speso")
        show_ean   = st.checkbox("EAN-13", value=False, key="cat_sean")
    with col7:
        show_uncx  = st.checkbox("Unidades por caixa", value=True, key="cat_suncx")
        show_val   = st.checkbox("Validade (dias)", value=True, key="cat_sval")
        show_ncm   = st.checkbox("NCM / CEST", value=False, key="cat_sncm")
    with col8:
        show_preco = st.checkbox("Tabela de preços", value=bool(tab_sel[0]), key="cat_spreco")
        show_obs   = st.checkbox("Observação", value=False, key="cat_sobs")

    # Dados do representante para rodapé
    rep = query("""SELECT nome_fantasia, razao_social, fone, whatsapp, email
        FROM representante WHERE ativo=1 LIMIT 1""")
    vend = query("""SELECT nome, fone, whatsapp, email
        FROM vendedor WHERE ativo=1 ORDER BY vendedor_id LIMIT 1""")

    st.markdown("**Rodapé — dados de contato:**")
    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        rod_empresa = st.text_input("Empresa representante",
                                    value=rep[0][0] if rep else "",
                                    key="cat_rnome")
    with col_r2:
        rod_vendedor = st.text_input("Vendedor / Representante",
                                     value=vend[0][0] if vend else "",
                                     key="cat_rvend")
    with col_r3:
        rod_fone = st.text_input("WhatsApp / Fone",
                                  value=(vend[0][2] or vend[0][1]) if vend else
                                        (rep[0][3] or rep[0][2]) if rep else "",
                                  key="cat_rfone")
    rod_email = st.text_input("E-mail",
                               value=vend[0][3] if vend else rep[0][4] if rep else "",
                               key="cat_remail")

    st.divider()
    col_btn, col_prev = st.columns([1, 2])
    gerar = col_btn.button("📄 Gerar catálogo PDF", type="primary",
                            width="stretch", key="cat_gerar")

    if gerar:
        with st.spinner("Gerando catálogo..."):
            buf = _gerar_pdf_catalogo(
                forn_id=forn_sel[0],
                forn_nome=forn_sel[1],
                tab_id=tab_sel[0] if tab_sel else None,
                agrupar=agrupar,
                ordenar=ordenar,
                incluir_inativos=incluir_inativos,
                show={
                    "cod": show_cod, "peso": show_peso, "ean": show_ean,
                    "uncx": show_uncx, "val": show_val, "ncm": show_ncm,
                    "preco": show_preco and bool(tab_sel[0]), "obs": show_obs
                },
                rodape={
                    "empresa": rod_empresa, "vendedor": rod_vendedor,
                    "fone": rod_fone, "email": rod_email
                }
            )
        nome_arq = (f"catalogo_{forn_sel[1].replace(' ','_')[:20]}"
                    f"_{date.today().strftime('%Y%m%d')}.pdf")
        st.download_button(
            f"⬇️ Baixar catálogo — {forn_sel[1]}",
            data=buf, file_name=nome_arq, mime="application/pdf",
            width="stretch"
        )
        st.success("Catálogo gerado! Clique acima para baixar.")


def _gerar_pdf_catalogo(forn_id, forn_nome, tab_id, agrupar, ordenar,
                         incluir_inativos, show, rodape):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units    import cm
    from reportlab.lib          import colors
    from reportlab.platypus     import (SimpleDocTemplate, Table, TableStyle,
                                        Paragraph, Spacer, HRFlowable,
                                        KeepTogether, PageBreak)
    from reportlab.lib.styles   import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums    import TA_CENTER, TA_LEFT, TA_RIGHT

    # Cores
    VERDE   = colors.HexColor("#2d6a4f")
    VERDE_C = colors.HexColor("#e8f5e9")
    CINZA   = colors.HexColor("#555555")
    CINZA_L = colors.HexColor("#f8f9fa")
    BRANCO  = colors.white

    sty = getSampleStyleSheet()
    s_title = ParagraphStyle("cat_title", parent=sty["Normal"],
                              fontSize=18, fontName="Helvetica-Bold",
                              textColor=VERDE, spaceAfter=2)
    s_sub   = ParagraphStyle("cat_sub", parent=sty["Normal"],
                              fontSize=10, textColor=CINZA, spaceAfter=6)
    s_grp   = ParagraphStyle("cat_grp", parent=sty["Normal"],
                              fontSize=11, fontName="Helvetica-Bold",
                              textColor=BRANCO, spaceAfter=0)
    s_prod  = ParagraphStyle("cat_prod", parent=sty["Normal"],
                              fontSize=8, leading=10)
    s_prod_b= ParagraphStyle("cat_prod_b", parent=sty["Normal"],
                              fontSize=8, fontName="Helvetica-Bold", leading=10)
    s_hdr   = ParagraphStyle("cat_hdr", parent=sty["Normal"],
                              fontSize=7, fontName="Helvetica-Bold",
                              textColor=BRANCO)
    s_rod   = ParagraphStyle("cat_rod", parent=sty["Normal"],
                              fontSize=7, textColor=CINZA, alignment=TA_CENTER)

    # Largura útil real da página (A4 = 21cm, 2x margem 0.8cm = 19.4cm)
    MARGEM     = 0.8 * cm
    LARGURA    = A4[0] - 2 * MARGEM          # ~19.4 cm

    # Pesos relativos de cada coluna (produto recebe o restante)
    # Definimos as colunas opcionais com largura fixa em proporção da A4
    # e a coluna Produto absorve o espaço restante
    FIXAS = []   # (label, largura_fixa)
    if show["cod"]:   FIXAS.append(("Código",        2.0*cm))
    if show["uncx"]:  FIXAS.append(("Un/Cx",         1.4*cm))
    if show["peso"]:  FIXAS.append(("Peso/Vol.+UM",  2.2*cm))
    if show["val"]:   FIXAS.append(("Val.(d)",        1.4*cm))
    if show["ean"]:   FIXAS.append(("EAN-13",         2.8*cm))
    if show["ncm"]:   FIXAS.append(("NCM",            2.0*cm))
    if show["preco"]: FIXAS.append(("Preço Cx",       2.2*cm))
    if show["obs"]:   FIXAS.append(("Obs.",            2.8*cm))

    soma_fixas   = sum(w for _, w in FIXAS)
    w_produto    = LARGURA - soma_fixas          # coluna Produto = tudo que sobra
    w_produto    = max(w_produto, 4.0*cm)        # mínimo de 4 cm

    col_labels = ["Produto"] + [lbl for lbl, _ in FIXAS]
    col_widths = [w_produto] + [w for _, w in FIXAS]

    # Busca produtos
    order_map = {
        "Descrição":             "p.descricao",
        "Código":                "p.codigo_produto",
        "Categoria → Descrição": "cat.nome_categoria, p.descricao",
        "Linha → Descrição":     "l.nome_linha, p.descricao",
        "Grupo → Descrição":     "p.grupo, p.descricao",
    }
    order_sql = order_map.get(ordenar, "p.descricao")
    ativo_fil = "" if incluir_inativos else "AND p.ativo=1"

    produtos = query(f"""
        SELECT p.produto_id, p.descricao, p.descricao_curta,
               p.codigo_produto, p.unidade_medida, p.unidades_caixa,
               p.peso, p.peso_caixa, p.validade_dias,
               p.ean, p.ncm, p.cest,
               COALESCE(p.sub_categoria,''), COALESCE(p.grupo,''),
               COALESCE(cat.nome_categoria,'Sem categoria'),
               COALESCE(l.nome_linha,'Sem linha'),
               p.observacao, p.ativo
        FROM produto p
        LEFT JOIN categoria cat ON p.categoria_id=cat.categoria_id
        LEFT JOIN linha l       ON p.linha_id=l.linha_id
        WHERE p.fornecedor_id=? {ativo_fil}
        ORDER BY {order_sql}
    """, (forn_id,))

    if not produtos:
        buf = io.BytesIO()
        buf.write(b"%PDF-1.4\n")  # PDF mínimo
        buf.seek(0)
        return buf

    # Busca preços se solicitado
    precos = {}
    if show["preco"] and tab_id:
        px = query("""SELECT tpi.produto_id, tpi.preco_caixa, tpi.preco_kg
            FROM tabela_preco_item tpi WHERE tpi.tabela_preco_id=?""", (tab_id,))
        precos = {r[0]: (r[1], r[2]) for r in px}

    # Agrupamento duplo: Categoria → Linha (padrão) ou simples
    from itertools import groupby

    if agrupar == "Categoria":
        # Agrupa por Categoria, sub-agrupa por Linha
        cat_grupos = {}
        for p in produtos:
            cat  = p[14] or "Sem categoria"
            linha = p[15] or "Sem linha"
            cat_grupos.setdefault(cat, {}).setdefault(linha, []).append(p)
        # Converte para lista ordenada: {(cat, linha): [prods]}
        grupos = {}
        for cat in sorted(cat_grupos.keys()):
            for linha in sorted(cat_grupos[cat].keys()):
                grupos[(cat, linha)] = cat_grupos[cat][linha]
        modo_duplo = True
    else:
        grupo_map = {
            "Linha":          15,
            "Sub-categoria":  12,
            "Grupo":          13,
            "Sem agrupamento": None,
        }
        grp_idx = grupo_map.get(agrupar)
        if grp_idx is not None:
            grupos = {}
            for p in produtos:
                chave = p[grp_idx] or "Sem classificação"
                grupos.setdefault(chave, []).append(p)
        else:
            grupos = {"": produtos}
        modo_duplo = False

    # Monta documento
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=0.8*cm, rightMargin=0.8*cm,
                            topMargin=1.5*cm, bottomMargin=1.8*cm)

    # Rodapé em todas as páginas
    rod_txt = []
    if rodape["empresa"]:   rod_txt.append(rodape["empresa"])
    if rodape["vendedor"]:  rod_txt.append(rodape["vendedor"])
    if rodape["fone"]:      rod_txt.append(f"WhatsApp: {rodape['fone']}")
    if rodape["email"]:     rod_txt.append(rodape["email"])
    rod_str = "   |   ".join(rod_txt)

    def _rodape(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(CINZA)
        canvas.drawCentredString(A4[0]/2, 1.2*cm,
                                  rod_str + f"   |   Gerado em {datetime.now().strftime('%d/%m/%Y')}")
        canvas.setStrokeColor(VERDE)
        canvas.setLineWidth(0.5)
        canvas.line(0.8*cm, 1.5*cm, A4[0]-0.8*cm, 1.5*cm)
        canvas.restoreState()

    el = []

    # Cabeçalho
    el.append(Paragraph(forn_nome, s_title))
    el.append(Paragraph(f"Catálogo de produtos  —  {len(produtos)} item(ns)", s_sub))
    if tab_id and tabelas:
        tab_info = next((t for t in tabelas if t[0]==tab_id), None)
        if tab_info:
            el.append(Paragraph(f"Tabela: {tab_info[1]}", s_sub))
    el.append(HRFlowable(width="100%", thickness=2, color=VERDE, spaceAfter=8))

    # Estilo de sub-grupo (linha)
    s_subgrp = ParagraphStyle("cat_subgrp", parent=sty["Normal"],
                               fontSize=9, fontName="Helvetica-Bold",
                               textColor=VERDE, spaceBefore=4, spaceAfter=2)

    prev_cat = None
    for grp_nome, prods in grupos.items():
        bloco = []

        # Cabeçalho do grupo
        if grp_nome:
            if isinstance(grp_nome, tuple):
                cat_nome_g, linha_nome_g = grp_nome
                # Cabeçalho de Categoria — só imprime quando muda
                if cat_nome_g != prev_cat:
                    cat_row = [[Paragraph(f"  {cat_nome_g.upper()}", s_grp)]]
                    cat_tbl = Table(cat_row, colWidths=[LARGURA])
                    cat_tbl.setStyle(TableStyle([
                        ("BACKGROUND", (0,0), (-1,-1), VERDE),
                        ("TOPPADDING",    (0,0),(-1,-1), 5),
                        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
                    ]))
                    bloco.append(Spacer(1, 4))
                    bloco.append(cat_tbl)
                    prev_cat = cat_nome_g
                # Sub-cabeçalho de Linha
                bloco.append(Paragraph(f"    Linha: {linha_nome_g}", s_subgrp))
                bloco.append(Spacer(1, 1))
            else:
                grp_row = [[Paragraph(f"  {grp_nome.upper()}", s_grp)]]
                grp_tbl = Table(grp_row, colWidths=[LARGURA])
                grp_tbl.setStyle(TableStyle([
                    ("BACKGROUND", (0,0), (-1,-1), VERDE),
                    ("TOPPADDING",    (0,0),(-1,-1), 4),
                    ("BOTTOMPADDING", (0,0),(-1,-1), 4),
                ]))
                bloco.append(grp_tbl)
                bloco.append(Spacer(1, 2))

        # Cabeçalho da tabela de produtos
        hdr = [Paragraph(c, s_hdr) for c in col_labels]
        rows = [hdr]

        # Linhas de produtos
        for i, p in enumerate(prods):
            (pid, desc, desc_c, cod, um, uncx, peso, peso_cx,
             val, ean, ncm, cest, subcat, grupo,
             cat_nome, linha_nome, obs, ativo) = p

            # Nome do produto
            nome_exib = desc_c if desc_c else desc
            if not ativo:
                nome_exib = f"[INATIVO] {nome_exib}"
            info_extra = []
            if subcat: info_extra.append(subcat)
            if grupo:  info_extra.append(grupo)
            nome_cell = [Paragraph(nome_exib, s_prod_b)]
            if info_extra:
                nome_cell.append(Paragraph(", ".join(info_extra), s_prod))

            row = [nome_cell]
            if show["cod"]:  row.append(Paragraph(cod or "—", s_prod))
            if show["uncx"]: row.append(Paragraph(str(uncx) if uncx else "—", s_prod))
            if show["peso"]:
                p_str = f"{peso:.3f}".rstrip('0').rstrip('.') if peso else "—"
                row.append(Paragraph(f"{p_str} {um or ''}".strip(), s_prod))
            if show["val"]:   row.append(Paragraph(str(val or "—"), s_prod))
            if show["ean"]:   row.append(Paragraph(ean or "—", s_prod))
            if show["ncm"]:   row.append(Paragraph(ncm or "—", s_prod))
            if show["preco"]:
                pr = precos.get(pid)
                row.append(Paragraph(
                    _brl(pr[0]) if pr and pr[0] else "—", s_prod))
            if show["obs"]:   row.append(Paragraph(obs or "—", s_prod))

            rows.append(row)

        t = Table(rows, colWidths=col_widths, repeatRows=1)
        ts = TableStyle([
            # Cabeçalho
            ("BACKGROUND",    (0,0), (-1,0),  VERDE),
            ("TEXTCOLOR",     (0,0), (-1,0),  BRANCO),
            ("FONTSIZE",      (0,0), (-1,-1), 7),
            ("TOPPADDING",    (0,0), (-1,-1), 3),
            ("BOTTOMPADDING", (0,0), (-1,-1), 3),
            ("LEFTPADDING",   (0,0), (-1,-1), 4),
            ("RIGHTPADDING",  (0,0), (-1,-1), 4),
            ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#cccccc")),
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
            ("ROWBACKGROUNDS",(0,1), (-1,-1), [BRANCO, CINZA_L]),
        ])
        t.setStyle(ts)
        bloco.append(t)
        bloco.append(Spacer(1, 6))
        el.append(KeepTogether(bloco[:3]))  # tenta manter grupo junto
        if len(bloco) > 3:
            el.extend(bloco[3:])

    doc.build(el, onFirstPage=_rodape, onLaterPages=_rodape)
    buf.seek(0)
    return buf


# ═══════════════════════════════════════════════════════
# 2. MENSAGENS WHATSAPP COM BIBLIOTECA
# ═══════════════════════════════════════════════════════
def _garantir_tabela_mensagens():
    conn = conectar()
    conn.execute("""CREATE TABLE IF NOT EXISTS mensagem_modelo (
        mensagem_id  INTEGER PRIMARY KEY AUTOINCREMENT,
        nome         TEXT NOT NULL,
        assunto      TEXT,
        corpo        TEXT NOT NULL,
        via          TEXT DEFAULT 'WhatsApp',
        ativo        INTEGER DEFAULT 1)""")
    conn.commit(); conn.close()


def _tela_mensagens():
    _garantir_tabela_mensagens()
    st.subheader("💬 Biblioteca de mensagens & envio WhatsApp")

    ABAS_MSG = {
        "enviar":    "📤 Enviar mensagem",
        "modelos":   "📝 Gerenciar modelos",
    }
    if "msg_aba" not in st.session_state:
        st.session_state["msg_aba"] = "enviar"
    cols = st.columns(2)
    for col, (k, v) in zip(cols, ABAS_MSG.items()):
        ativa = st.session_state["msg_aba"] == k
        if col.button(v, key=f"msgnav_{k}", width="stretch",
                      type="primary" if ativa else "secondary"):
            st.session_state["msg_aba"] = k; st.rerun()
    st.divider()

    if st.session_state["msg_aba"] == "enviar":
        _tela_enviar_mensagem()
    else:
        _tela_gerenciar_modelos()


def _tela_enviar_mensagem():
    modelos = query("""SELECT mensagem_id, nome, assunto, corpo
        FROM mensagem_modelo WHERE ativo=1 ORDER BY nome""")

    clientes = query("SELECT cliente_id, nome_fantasia, status FROM cliente ORDER BY nome_fantasia")
    fornecs  = query("SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia")

    # Seleção de destinatário
    st.markdown("**1. Para quem?**")
    col1, col2 = st.columns(2)
    with col1:
        dest_tipo = st.selectbox("Tipo", ["Cliente","Fornecedor"], key="ms_tipo")
    with col2:
        if dest_tipo == "Cliente":
            dest_sel = st.selectbox("Cliente",
                                    clientes,
                                    format_func=lambda x: f"{x[1]} ({x[2]})" if x[2] else x[1],
                                    key="ms_cli")
            dest_id   = dest_sel[0] if dest_sel else None
            dest_nome = dest_sel[1] if dest_sel else ""
            dest_forn_id = None

            # Contatos com WhatsApp
            contatos = query("""SELECT contato_cliente_id, nome_contato,
                    departamento, whatsapp
                FROM contato_cliente
                WHERE cliente_id=? AND ativo=1 AND whatsapp IS NOT NULL
                ORDER BY nome_contato""", (dest_id,)) if dest_id else []
        else:
            dest_sel = st.selectbox("Fornecedor", fornecs,
                                    format_func=lambda x: x[1], key="ms_forn")
            dest_id      = None
            dest_forn_id = dest_sel[0] if dest_sel else None
            dest_nome    = dest_sel[1] if dest_sel else ""
            contatos = []

    # Contato de destino
    st.markdown("**2. Para qual contato?**")
    pessoa_nome = ""

    # Limpa campos quando cliente muda
    if st.session_state.get("ms_cli_anterior") != dest_id:
        st.session_state["ms_cli_anterior"] = dest_id
        st.session_state.pop("ms_wa_num", None)

    if dest_tipo == "Cliente":
        _cli_fone = query("SELECT COALESCE(fone,'') FROM cliente WHERE cliente_id=?",
                          (dest_id,)) if dest_id else []
        _fone_cli = _cli_fone[0][0] if _cli_fone and _cli_fone[0][0] else ""

        if contatos:
            ct_opts_full = [(None, "— usar fone do cadastro —")] + \
                           [(c[0], f"{c[1]}" + (f" — {c[2]}" if c[2] else "") +
                             f" | {c[3]}") for c in contatos]
            ct_sel = st.selectbox("Contato", ct_opts_full,
                                  format_func=lambda x: x[1], key="ms_ct")
            if ct_sel and ct_sel[0]:
                ct_info = next((c for c in contatos if c[0]==ct_sel[0]), None)
                if ct_info:
                    pessoa_nome = ct_info[1]
                    _fone_cli = ct_info[3] or _fone_cli

        # Usa session_state para preservar edição manual, mas inicializa com fone do cadastro
        if "ms_wa_num" not in st.session_state:
            st.session_state["ms_wa_num"] = _fone_cli

        wa_num = st.text_input("Número WhatsApp",
                               key="ms_wa_num",
                               placeholder="11 9 9999-9999",
                               help="Auto-preenchido com o fone do cadastro")
    else:
        wa_num = st.text_input("Número WhatsApp do fornecedor",
                               placeholder="11 9 9999-9999", key="ms_wa_forn")

    # Seleção do modelo
    st.markdown("**3. Qual mensagem?**")
    if modelos:
        mod_opts = [(None, "— escrever do zero —")] + \
                   [(m[0], f"{m[1]}" + (f" — {m[2]}" if m[2] else ""))
                    for m in modelos]
        mod_sel = st.selectbox("Modelo salvo", mod_opts,
                               format_func=lambda x: x[1], key="ms_modelo")

        if mod_sel and mod_sel[0]:
            modelo_info = next((m for m in modelos if m[0]==mod_sel[0]), None)
            corpo_base  = modelo_info[3] if modelo_info else ""
            assunto_base= modelo_info[2] if modelo_info else ""
        else:
            corpo_base   = ""
            assunto_base = ""
    else:
        corpo_base   = ""
        assunto_base = ""
        st.info("Nenhum modelo salvo ainda — escreva abaixo e salve como modelo se quiser.")

    assunto_msg = st.text_input("Assunto (para registro em Contatos)",
                                value=assunto_base, key="ms_assunto",
                                placeholder="Ex: Prospecção salsichas Specialli")

    # Editor de mensagem — personalizações automáticas
    st.markdown("**4. Edite a mensagem antes de enviar:**")
    st.caption("Variáveis automáticas: `{cliente}` = nome do cliente, `{vendedor}` = seu nome")

    # Obtém nome do vendedor
    vend = query("SELECT nome FROM vendedor WHERE ativo=1 LIMIT 1")
    nome_vend = vend[0][0] if vend else ""

    # Limpa session_state quando modelo muda E inicializa com conteúdo personalizado
    _mod_id = mod_sel[0] if mod_sel and mod_sel[0] else None
    if st.session_state.get("ms_modelo_anterior") != _mod_id:
        st.session_state["ms_modelo_anterior"] = _mod_id
        corpo_personalizado = corpo_base.replace(
            "{cliente}", dest_nome or "").replace("{vendedor}", nome_vend)
        st.session_state["ms_corpo"] = corpo_personalizado

    corpo_edit = st.text_area("Mensagem",
                              key="ms_corpo",
                              height=200,
                              help="Edite livremente antes de enviar.")

    # Registrar também em Contatos?
    registrar = st.checkbox("✅ Registrar este contato em Contatos & Negociações",
                            value=True, key="ms_registrar")

    if registrar:
        _kfn = "ms_forns_sel"
        if _kfn not in st.session_state: st.session_state[_kfn] = []
        st.multiselect("Fornecedores tratados na mensagem",
                       options=[(f[0],f[1]) for f in fornecs],
                       format_func=lambda x: x[1], key=_kfn)
        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        with col_r1:
            STATUS_TOPICO = ["Em andamento","A contatar","Aguardando retorno",
                             "Proposta enviada","Concluído","Cancelado"]
            ms_status = st.selectbox("Status", STATUS_TOPICO,
                                     index=1, key="ms_status")
        with col_r2:
            ms_prior = st.selectbox("Prioridade", ["Alta","Média","Baixa"],
                                    index=1, key="ms_prior")
        with col_r3:
            ms_tipo = st.selectbox("Tipo", ["Contato","Negociação"],
                                   key="ms_tipo_top")
        with col_r4:
            ms_fup = st.date_input("Próximo contato", value=None, key="ms_fup")

    st.divider()

    # Preview do link WhatsApp
    if wa_num and corpo_edit:
        num_clean = "".join(filter(str.isdigit, wa_num))
        if not num_clean.startswith("55"):
            num_clean = "55" + num_clean
        import urllib.parse
        texto_enc = urllib.parse.quote(corpo_edit)
        wa_link   = f"https://wa.me/{num_clean}?text={texto_enc}"

        col_wa, col_copia = st.columns(2)
        col_wa.markdown(
            f'<a href="{wa_link}" target="_blank">'
            f'<button style="background:#25D366;color:white;border:none;'
            f'padding:10px 20px;border-radius:8px;font-size:15px;'
            f'cursor:pointer;width:100%">💬 Abrir WhatsApp e enviar</button></a>',
            unsafe_allow_html=True
        )

        if col_copia.button("📋 Copiar mensagem", key="ms_copiar",
                            width="stretch"):
            st.code(corpo_edit, language=None)
            st.caption("Selecione o texto acima e copie.")

        # Após abrir o WhatsApp — botão de confirmar envio
        st.caption("Após enviar no WhatsApp, clique abaixo para confirmar o registro:")
        if st.button("✅ Confirmar envio e registrar", key="ms_confirmar",
                     type="primary", width="stretch"):
            if registrar and dest_id:
                # Registra em contato_registro + contato_interacao
                _forns = st.session_state.get("ms_forns_sel", [])
                conn   = conectar()
                from database import _check_supabase
                _ms_status = st.session_state.get("ms_status", "Em andamento")
                _ms_prior  = st.session_state.get("ms_prior", "Média")
                _ms_tipo   = st.session_state.get("ms_tipo_top", "Contato")
                _ms_fup    = st.session_state.get("ms_fup", None)
                _fup_val   = _ms_fup.isoformat() if _ms_fup and hasattr(_ms_fup,'isoformat') else None

                if _check_supabase():
                    novo_cid = conn.execute("""INSERT INTO contato_registro
                        (data_contato, via_comunicacao, tipo_entidade, cliente_id,
                         contato_pessoa, assunto, descricao, status, prioridade,
                         tipo_topico, data_followup, ativo)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,1)
                        RETURNING contato_id""",
                        (date.today().isoformat(), "WhatsApp", "cliente", dest_id,
                         pessoa_nome or None,
                         assunto_msg.strip() or "Mensagem WhatsApp",
                         corpo_edit.strip(),
                         _ms_status, _ms_prior, _ms_tipo, _fup_val)).fetchone()[0]
                else:
                    conn.execute("""INSERT INTO contato_registro
                        (data_contato, via_comunicacao, tipo_entidade, cliente_id,
                         contato_pessoa, assunto, descricao, status, prioridade,
                         tipo_topico, data_followup, ativo)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,1)""",
                        (date.today().isoformat(), "WhatsApp", "cliente", dest_id,
                         pessoa_nome or None,
                         assunto_msg.strip() or "Mensagem WhatsApp",
                         corpo_edit.strip(),
                         _ms_status, _ms_prior, _ms_tipo, _fup_val))
                    novo_cid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

                for ft in _forns:
                    fid = ft[0] if isinstance(ft,(list,tuple)) else ft
                    conn.execute("INSERT OR IGNORE INTO contato_x_fornecedor "
                                 "(contato_id, fornecedor_id) VALUES (?,?)",
                                 (novo_cid, fid))

                conn.execute("""INSERT INTO contato_interacao
                    (contato_id, data_interacao, via_comunicacao,
                     contato_pessoa, descricao, ativo)
                    VALUES (?,?,?,?,?,1)""",
                    (novo_cid, date.today().isoformat(), "WhatsApp",
                     pessoa_nome or None, corpo_edit.strip()))
                conn.commit(); conn.close()
                # Limpa form após salvar (Fix 5)
                for k in ["ms_wa_num","ms_corpo","ms_modelo_anterior",
                          "ms_assunto","ms_forns_sel","ms_cli_anterior",
                          "ms_status","ms_prior","ms_tipo_top","ms_fup"]:
                    st.session_state.pop(k, None)
                st.success(f"✅ Mensagem registrada em Contatos para **{dest_nome}**!")
                st.session_state["cat_msg_ok"] = f"✅ Registrado: {dest_nome}"
            else:
                st.success("✅ Envio confirmado!")
            st.rerun()
    else:
        if not wa_num and not corpo_edit:
            st.info("Preencha o número e a mensagem para gerar o link de envio.")
        elif not wa_num:
            st.info("Preencha o número WhatsApp para gerar o link.")
        elif not corpo_edit:
            st.info("Selecione um modelo ou escreva a mensagem para gerar o link.")


def _tela_gerenciar_modelos():
    modelos = query("""SELECT mensagem_id, nome, assunto, corpo, via
        FROM mensagem_modelo WHERE ativo=1 ORDER BY nome""")

    # Novo modelo
    with st.expander("➕ Criar novo modelo", expanded=not bool(modelos)):
        nm_nome   = st.text_input("Nome do modelo *",
                                  placeholder="Ex: Prospecção salsichas Specialli",
                                  key="nm_nome")
        nm_assunto= st.text_input("Assunto",
                                  placeholder="Ex: Apresentação Specialli",
                                  key="nm_assunto")
        nm_corpo  = st.text_area("Texto da mensagem *",
                                  placeholder="Olá, {cliente}! Tudo bem?\n\nMeu nome é Fernando...",
                                  height=200, key="nm_corpo")
        st.caption("Use `{cliente}` para o nome do cliente e `{vendedor}` para o seu nome — serão substituídos automaticamente ao enviar.")
        if st.button("💾 Salvar modelo", key="nm_salvar", type="primary"):
            if not nm_nome.strip() or not nm_corpo.strip():
                st.error("Nome e texto são obrigatórios.")
            else:
                conn = conectar()
                conn.execute("""INSERT INTO mensagem_modelo
                    (nome, assunto, corpo, via, ativo) VALUES (?,?,?,?,1)""",
                    (nm_nome.strip(), nm_assunto.strip() or None,
                     nm_corpo.strip(), "WhatsApp"))
                conn.commit(); conn.close()
                st.session_state["cat_msg"] = f"✅ Modelo '{nm_nome.strip()}' salvo!"
                st.rerun()

    if not modelos:
        st.info("Nenhum modelo salvo ainda.")
        return

    st.subheader(f"Modelos salvos ({len(modelos)})")
    for m in modelos:
        mid, nome, assunto, corpo, via = m
        with st.expander(f"📝 {nome}" + (f" — {assunto}" if assunto else "")):
            # Edição inline
            e_nome   = st.text_input("Nome", value=nome, key=f"em_n_{mid}")
            e_assunto= st.text_input("Assunto", value=assunto or "", key=f"em_a_{mid}")
            e_corpo  = st.text_area("Texto", value=corpo, height=150, key=f"em_c_{mid}")

            col_s, col_d = st.columns(2)
            if col_s.button("💾 Salvar", key=f"em_save_{mid}",
                            width="stretch", type="primary"):
                conn = conectar()
                conn.execute("""UPDATE mensagem_modelo SET
                    nome=?, assunto=?, corpo=? WHERE mensagem_id=?""",
                    (e_nome.strip(), e_assunto.strip() or None,
                     e_corpo.strip(), mid))
                conn.commit(); conn.close()
                st.session_state["cat_msg"] = "✅ Modelo atualizado."
                st.rerun()
            if col_d.button("🗑️ Excluir", key=f"em_del_{mid}",
                            width="stretch"):
                conn = conectar()
                conn.execute("UPDATE mensagem_modelo SET ativo=0 WHERE mensagem_id=?",
                             (mid,))
                conn.commit(); conn.close()
                st.session_state["cat_msg"] = "Modelo removido."
                st.rerun()