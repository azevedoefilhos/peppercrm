# ver_pedidos.py -- PepperCRM
# Visualizacao, edicao e histórico de pedidos

import streamlit as st
import pandas as pd
import io
import urllib.parse
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                Paragraph, Spacer, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from database import conectar, query, registrar_historico

STATUS_PEDIDO = ["ABERTO","ENVIADO","CONFIRMADO","FATURADO","ENTREGUE","DEVOLVIDO","CANCELADO","RECUSADO"]
STATUS_ITEM   = ["NORMAL","BONIFICADO","PENDENTE","DEVOLVIDO","CANCELADO"]
EDITAVEIS     = {"ABERTO","ENVIADO"}

ICONE_STATUS = {
    "ABERTO":     "🟡",
    "ENVIADO":    "📤",
    "CONFIRMADO": "🟢",
    "FATURADO":   "🧾",
    "ENTREGUE":   "✅",
    "DEVOLVIDO":  "🔄",
    "CANCELADO":  "🔴",
    "RECUSADO":   "⛔",
}

def _ir(p):
    st.session_state["pagina"] = p
    st.rerun()

def _brl(v):
    if v is None: return "—"
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")


def tela_ver_pedidos():
    st.header("Pedidos")

    # Roteamento interno: lista | detalhe | historico
    modo   = st.session_state.get("vp_modo", "lista")
    ped_id = st.session_state.get("pedido_ativo_id")

    if modo == "lista":
        if st.button("⬅ Voltar"):
            _ir("home")
        _lista_pedidos()

    elif modo == "detalhe" and ped_id:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            if st.button("⬅ Lista de pedidos"):
                st.session_state["vp_modo"] = "lista"
                st.session_state.pop("pedido_ativo_id", None)
                st.rerun()
        with col2:
            if st.button("📋 Historico", use_container_width=True):
                st.session_state["vp_modo"] = "historico"
                st.rerun()
        with col3:
            if st.button("⬅ Voltar ao menu", use_container_width=True):
                _ir("home")
        _tela_editar_pedido()

    elif modo == "historico" and ped_id:
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("⬅ Voltar ao pedido"):
                st.session_state["vp_modo"] = "detalhe"
                st.rerun()
        with col2:
            if st.button("Lista de pedidos", use_container_width=True):
                st.session_state["vp_modo"] = "lista"
                st.session_state.pop("pedido_ativo_id", None)
                st.rerun()
        _tela_historico()

    else:
        st.session_state["vp_modo"] = "lista"
        st.rerun()


def _lista_pedidos():
    col1, col2, col3, col4 = st.columns(4)

    clientes = [(None,"Todos")] + query(
        "SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo=1 ORDER BY nome_fantasia")
    fornecs  = [(None,"Todos")] + query(
        "SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia")

    with col1:
        cli_f  = st.selectbox("Cliente",    clientes, format_func=lambda x: x[1], key="f_cli")
    with col2:
        forn_f = st.selectbox("Fornecedor", fornecs,  format_func=lambda x: x[1], key="f_forn")
    with col3:
        stat_f = st.selectbox("Status", ["Todos"] + STATUS_PEDIDO, key="f_stat")
    with col4:
        periodo = st.selectbox("Período", ["Todos","Hoje","7 dias","30 dias","90 dias"], key="f_per")

    where, params = ["1=1"], []
    if cli_f and cli_f[0]:
        where.append("p.cliente_id=?"); params.append(cli_f[0])
    if forn_f and forn_f[0]:
        where.append("p.fornecedor_id=?"); params.append(forn_f[0])
    if stat_f != "Todos":
        where.append("p.status_pedido=?"); params.append(stat_f)
    dias_map = {"Hoje":0,"7 dias":7,"30 dias":30,"90 dias":90}
    if periodo in dias_map:
        where.append(f"p.data_pedido >= date('now','-{dias_map[periodo]} days')")

    dados = query(f"""
        SELECT p.pedido_id, p.data_pedido,
               c.nome_fantasia,
               COALESCE(pdv.nome_loja,'—') AS pdv,
               f.nome_fantasia,
               COALESCE(p.nr_pedido_cliente,'—'),
               COALESCE(p.nr_pedido_fornecedor,'—'),
               COALESCE(p.prazo_pagamento,'—'),
               COALESCE(p.data_entrega,'—'),
               ROUND(SUM(pi.preco_final * pi.quantidade
                     * (1 - COALESCE(p.desconto_geral,0)/100.0)), 2) AS total,
               COUNT(pi.pedido_item_id),
               p.status_pedido
        FROM pedido p
        JOIN cliente c    ON p.cliente_id=c.cliente_id
        JOIN fornecedor f ON p.fornecedor_id=f.fornecedor_id
        LEFT JOIN pdv     ON p.pdv_id=pdv.pdv_id
        LEFT JOIN pedido_item pi ON p.pedido_id=pi.pedido_id
        WHERE {' AND '.join(where)}
        GROUP BY p.pedido_id
        ORDER BY p.data_pedido DESC, p.pedido_id DESC
    """, tuple(params))

    if not dados:
        st.info("Nenhum pedido encontrado.")
        return

    # Exportar
    col_c, col_e = st.columns([3,1])
    total_geral = sum(r[9] or 0 for r in dados)
    col_c.caption(f"{len(dados)} pedido(s) — Total filtrado: **{_brl(total_geral)}**")
    with col_e:
        df_exp = pd.DataFrame([(
            r[0], r[1], r[2], r[3], r[4],
            f"{ICONE_STATUS.get(r[11],'')} {r[11]}",
            r[5], r[6], r[10], _brl(r[9])
        ) for r in dados],
        columns=["#","Data","Cliente","PDV","Fornecedor","Status","Nr.Cliente","Nr.Forn.","Itens","Total"])
        buf = io.BytesIO()
        df_exp.to_excel(buf, index=False, sheet_name="Pedidos")
        buf.seek(0)
        st.download_button("⬇️ Exportar Excel", data=buf, file_name="pedidos.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)

    df = pd.DataFrame(dados, columns=[
        "ID","Data","Cliente","PDV","Fornecedor",
        "Nr.Cliente","Nr.Forn.","Prazo","Entrega","Total","Itens","Status"])
    df["Total"] = df["Total"].apply(lambda v: _brl(v))
    df["Status"] = df["Status"].apply(lambda s: f"{ICONE_STATUS.get(s,'⚪')} {s}")
    st.dataframe(df[["ID","Data","Cliente","PDV","Fornecedor","Status","Itens","Total","Entrega"]],
                 use_container_width=True, hide_index=True)

    st.divider()
    ids = [(r[0], f"Pedido #{r[0]} — {r[2]} / {r[4]} — {r[1]}") for r in dados]
    sel = st.selectbox("Selecionar pedido para editar/detalhar",
                       ids, format_func=lambda x: x[1], key="sel_ped_lista")
    if st.button("📂 Abrir pedido selecionado", type="primary"):
        st.session_state["pedido_ativo_id"] = sel[0]
        st.session_state["vp_modo"] = "detalhe"
        st.rerun()


def _tela_editar_pedido():
    ped_id = st.session_state.get("pedido_ativo_id")
    if not ped_id:
        st.info("Selecione um pedido na lista.")
        return

    conn = conectar()
    ped  = conn.execute("""
        SELECT p.*, c.nome_fantasia AS cliente_nome,
               f.nome_fantasia AS forn_nome,
               pdv.nome_loja   AS pdv_nome,
               tp.nome_tabela,
               p.data_entrega_realizada
        FROM pedido p
        JOIN cliente c    ON p.cliente_id=c.cliente_id
        JOIN fornecedor f ON p.fornecedor_id=f.fornecedor_id
        LEFT JOIN pdv     ON p.pdv_id=pdv.pdv_id
        LEFT JOIN tabela_preco tp ON p.tabela_preco_id=tp.tabela_preco_id
        WHERE p.pedido_id=?""", (ped_id,)).fetchone()
    conn.close()
    if not ped: st.error("Pedido não encontrado."); return

    editavel = ped["status_pedido"] in EDITAVEIS
    icone    = ICONE_STATUS.get(ped["status_pedido"], "⚪")

    # ── CABECALHO: identidade + status + acoes ────────
    st.subheader(f"Pedido #{ped_id}")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            f"**{ped['cliente_nome']}**  |  "
            f"{ped['pdv_nome'] or 'Matriz'}  |  "
            f"**{ped['forn_nome']}**"
        )
        entrega_prev  = (ped['data_entrega'] or '—')[:10]
        entrega_real  = ped['data_entrega_realizada']
        entrega_label = entrega_prev
        if entrega_real:
            entrega_label = f"{entrega_prev} → ✅ realizada {entrega_real[:10]}"
        st.caption(
            f"Data: {(ped['data_pedido'] or '—')[:10]}  "
            f"| Entrega prevista: {entrega_label}  "
            f"| Tabela: {ped['nome_tabela'] or '—'}  "
            f"| Prazo: {ped['prazo_pagamento'] or '—'}  "
            f"| Frete: {ped['frete'] or '—'}"
        )
        if ped["observacao"]:
            st.caption(f"Obs.: {ped['observacao']}")
        if ped["nr_pedido_cliente"] or ped["nr_pedido_fornecedor"]:
            st.caption(
                f"Nr. cliente: {ped['nr_pedido_cliente'] or '—'}  "
                f"| Nr. fornecedor: {ped['nr_pedido_fornecedor'] or '—'}"
            )
    with col2:
        # Status em destaque no cabecalho
        st.markdown(f"**Status atual:**")
        st.markdown(f"### {icone} {ped['status_pedido']}")

    st.divider()

    # ── ALTERAR STATUS (no cabecalho, logo apos identidade) ──
    _form_alterar_status(ped_id, ped)

    if not editavel:
        st.info(
            f"Pedido **{ped['status_pedido']}** — somente leitura.  "
            f"Apenas pedidos ABERTO ou ENVIADO permitem editar itens e cabecalho."
        )

    st.divider()

    # ── EDITAR CABECALHO (expander) ───────────────────
    with st.expander("✏️ Editar dados do cabecalho", expanded=False):
        if editavel:
            _form_editar_cabecalho(ped_id, ped)
        else:
            st.caption("Pedido somente leitura.")

    # ── ACOES RAPIDAS: WhatsApp + Romaneio ───────────
    itens_ped = query("""
        SELECT pi.pedido_item_id, p.codigo_produto, p.descricao_curta,
               p.unidades_caixa, pi.quantidade,
               pi.preco_tabela, pi.desconto, pi.preco_final,
               pi.status_item,
               ROUND(pi.quantidade * pi.preco_final, 2) AS subtotal
        FROM pedido_item pi
        JOIN produto p ON pi.produto_id=p.produto_id
        WHERE pi.pedido_id=?
        ORDER BY p.descricao_curta
    """, (ped_id,))

    col_wa, col_xl, col_sp = st.columns(3)

    with col_wa:
        if itens_ped:
            msg = _gerar_mensagem_whatsapp(ped, itens_ped)
            # Numero do fornecedor — tenta buscar do cadastro
            forn_fone = query("""
                SELECT cf.fone FROM contato_fornecedor cf
                JOIN fornecedor f ON cf.fornecedor_id=f.fornecedor_id
                WHERE f.nome_fantasia=? AND cf.ativo=1 AND cf.fone IS NOT NULL
                ORDER BY cf.contato_fornecedor_id LIMIT 1
            """, (ped["forn_nome"],))
            numero_wa = ""
            if forn_fone and forn_fone[0][0]:
                numero_wa = "".join(c for c in forn_fone[0][0] if c.isdigit())
                if len(numero_wa) == 11:   # DDD + numero sem 55
                    numero_wa = "55" + numero_wa

            msg_enc = urllib.parse.quote(msg)
            wa_url  = f"https://wa.me/{numero_wa}?text={msg_enc}" if numero_wa                       else f"https://wa.me/?text={msg_enc}"

            st.link_button("Enviar pelo WhatsApp",
                           wa_url, use_container_width=True)
            with st.expander("Ver texto do pedido"):
                st.text(msg)

    with col_xl:
        if itens_ped:
            buf = _romaneio_excel(ped, itens_ped)
            cli_slug = "".join(c for c in (ped["cliente_nome"] or "")
                               if c.isalnum() or c == " ").strip().replace(" ","_")
            st.download_button(
                "Baixar romaneio Excel",
                data=buf,
                file_name=f"pedido_{ped_id}_{cli_slug}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

    with col_sp:
        if itens_ped:
            buf_pdf = _romaneio_pdf(ped, itens_ped)
            cli_slug = "".join(c for c in (ped["cliente_nome"] or "")
                               if c.isalnum() or c == " ").strip().replace(" ","_")
            st.download_button(
                "Baixar romaneio PDF",
                data=buf_pdf,
                file_name=f"pedido_{ped_id}_{cli_slug}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

    st.divider()

    # ── ITENS ─────────────────────────────────────────
    st.subheader("Itens do pedido")
    _tela_itens_pedido(ped_id, ped, editavel)

    if editavel:
        with st.expander("➕ Adicionar produto ao pedido"):
            _form_adicionar_item(ped_id, ped)


# ═══════════════════════════════════════════════════════
# WHATSAPP — gera mensagem formatada e abre link
# ═══════════════════════════════════════════════════════

def _gerar_mensagem_whatsapp(ped, itens):
    """Monta o texto do pedido para enviar pelo WhatsApp."""
    rep = query("SELECT nome_fantasia, fone, email FROM representante WHERE ativo=1 LIMIT 1")
    rep_nome  = rep[0][0] if rep else "Representante"
    rep_fone  = rep[0][1] if rep else ""

    linhas = []
    linhas.append(f"PEDIDO #{ped['pedido_id']}")
    linhas.append("=" * 35)
    linhas.append(f"De: {rep_nome}")
    linhas.append(f"Para: {ped['forn_nome']}")
    linhas.append(f"Cliente: {ped['cliente_nome']}")
    if ped["pdv_nome"] and ped["pdv_nome"] != "Matriz":
        linhas.append(f"PDV: {ped['pdv_nome']}")
    linhas.append(f"Data: {(ped['data_pedido'] or '')[:10]}")
    if ped["data_entrega"]:
        linhas.append(f"Entrega: {ped['data_entrega'][:10]}")
    linhas.append(f"Tabela: {ped['nome_tabela'] or '—'}")
    linhas.append(f"Prazo: {ped['prazo_pagamento'] or '—'}")
    if ped["nr_pedido_cliente"]:
        linhas.append(f"Nr. pedido cliente: {ped['nr_pedido_cliente']}")
    linhas.append("")
    linhas.append("ITENS:")
    linhas.append("-" * 35)

    total_cx  = 0
    total_val = 0.0
    for item in itens:
        (iid, cod, desc, un_cx, qtd,
         preco_tab, desconto, preco_fin, status_item, subtotal) = item
        if qtd and qtd > 0:
            sub = (preco_fin or 0) * qtd
            desc_g = float(ped["desconto_geral"] or 0)
            sub_final = sub * (1 - desc_g / 100)
            total_cx  += qtd
            total_val += sub_final
            desc_txt = f" (desc {desconto:.0f}%)" if desconto else ""
            sub_fmt = f"R${sub_final:,.2f}".replace(",","X").replace(".",",").replace("X",".")
            linhas.append(
                f"{cod}  {desc}\n"
                f"  {qtd} cx x R${preco_fin:.2f}{desc_txt} = {sub_fmt}"
            )

    linhas.append("-" * 35)
    desc_g = float(ped["desconto_geral"] or 0)
    if desc_g:
        linhas.append(f"Desconto geral: {desc_g:.1f}%")
    val_fmt = f"R${total_val:,.2f}".replace(",","X").replace(".",",").replace("X",".")
    linhas.append(f"TOTAL: {total_cx} caixas | {val_fmt}")
    if ped["observacao"]:
        linhas.append(f"\nObs: {ped['observacao']}")
    if rep_fone:
        linhas.append(f"\n{rep_nome} | {rep_fone}")

    return "\n".join(linhas)


def _romaneio_excel(ped, itens):
    """Gera Excel formatado de romaneio do pedido."""
    rep = query("SELECT nome_fantasia, fone, email FROM representante WHERE ativo=1 LIMIT 1")
    rep_nome = rep[0][0] if rep else "Representante"

    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        # Dados do cabecalho
        cab = {
            "Campo": ["Pedido #","Representante","Fornecedor","Cliente","PDV",
                      "Data","Entrega","Tabela","Prazo","Frete",
                      "Nr. cliente","Nr. fornecedor","Desconto geral (%)","Observacao"],
            "Valor": [
                str(ped["pedido_id"]),
                rep_nome,
                ped["forn_nome"] or "",
                ped["cliente_nome"] or "",
                ped["pdv_nome"] or "Matriz",
                (ped["data_pedido"] or "")[:10],
                (ped["data_entrega"] or "")[:10],
                ped["nome_tabela"] or "—",
                ped["prazo_pagamento"] or "—",
                ped["frete"] or "—",
                ped["nr_pedido_cliente"] or "",
                ped["nr_pedido_fornecedor"] or "",
                str(ped["desconto_geral"] or 0),
                ped["observacao"] or "",
            ]
        }
        pd.DataFrame(cab).to_excel(writer, sheet_name="Cabecalho", index=False)

        # Dados dos itens
        linhas = []
        total_cx = 0
        total_val = 0.0
        desc_g = float(ped["desconto_geral"] or 0)
        for item in itens:
            (iid, cod, desc, un_cx, qtd,
             preco_tab, desconto, preco_fin, status_item, subtotal) = item
            if not qtd or qtd <= 0:
                continue
            sub = (preco_fin or 0) * qtd * (1 - desc_g / 100)
            total_cx  += qtd
            total_val += sub
            linhas.append({
                "Codigo":       cod or "",
                "Descricao":    desc or "",
                "Un/Cx":        un_cx or 1,
                "Qtd (cx)":     qtd,
                "Preco tab.":   round(preco_tab or 0, 2),
                "Desc. item %": round(desconto or 0, 2),
                "Preco final":  round(preco_fin or 0, 4),
                "Desc. geral %":round(desc_g, 2),
                "Subtotal":     round(sub, 2),
                "Status item":  status_item or "NORMAL",
            })

        if linhas:
            df_itens = pd.DataFrame(linhas)
            # Linha de totais
            totais = {k: "" for k in df_itens.columns}
            totais["Descricao"]  = "TOTAL"
            totais["Qtd (cx)"]   = total_cx
            totais["Subtotal"]   = round(total_val, 2)
            df_itens = pd.concat([df_itens, pd.DataFrame([totais])],
                                 ignore_index=True)
            df_itens.to_excel(writer, sheet_name="Itens", index=False)

            # Formata planilha de itens
            ws = writer.sheets["Itens"]
            ws.column_dimensions["B"].width = 40
            ws.column_dimensions["A"].width = 14
            for col in ["C","D","E","F","G","H","I","J"]:
                ws.column_dimensions[col].width = 13

    buf.seek(0)
    return buf


def _romaneio_pdf(ped, itens):
    """Gera PDF formatado de romaneio do pedido."""
    rep = query("""SELECT nome_fantasia, fone, email, cnpj,
                          cidade, estado, endereco
                   FROM representante WHERE ativo=1 LIMIT 1""")
    rep_nome  = rep[0][0] if rep else "Representante"
    rep_fone  = rep[0][1] if rep else ""
    rep_email = rep[0][2] if rep else ""
    rep_cnpj  = rep[0][3] if rep else ""
    rep_cid   = f"{rep[0][4] or ''}/{rep[0][5] or ''}" if rep else ""

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=1.8*cm, rightMargin=1.8*cm,
                            topMargin=1.5*cm, bottomMargin=1.5*cm)
    styles = getSampleStyleSheet()

    # Estilos customizados
    titulo_style = ParagraphStyle("titulo", parent=styles["Normal"],
                                  fontSize=16, fontName="Helvetica-Bold",
                                  textColor=colors.HexColor("#1a1a2e"),
                                  spaceAfter=2)
    subtit_style = ParagraphStyle("subtit", parent=styles["Normal"],
                                  fontSize=9, textColor=colors.HexColor("#555555"),
                                  spaceAfter=1)
    campo_style  = ParagraphStyle("campo", parent=styles["Normal"],
                                  fontSize=9, spaceAfter=2)
    label_style  = ParagraphStyle("label", parent=styles["Normal"],
                                  fontSize=7, fontName="Helvetica-Bold",
                                  textColor=colors.HexColor("#888888"),
                                  spaceAfter=0)
    rodape_style = ParagraphStyle("rodape", parent=styles["Normal"],
                                  fontSize=7, textColor=colors.HexColor("#888888"),
                                  alignment=TA_CENTER)

    desc_g = float(ped["desconto_geral"] or 0)
    total_val = 0.0
    total_cx  = 0

    elementos = []

    # ── Cabecalho ──────────────────────────────────────
    cab_data = [[
        Paragraph(f"<b>{rep_nome}</b>", titulo_style),
        Paragraph(f"PEDIDO #{ped['pedido_id']}", ParagraphStyle(
            "pid", parent=styles["Normal"], fontSize=20,
            fontName="Helvetica-Bold", textColor=colors.HexColor("#2d6a4f"),
            alignment=TA_RIGHT)),
    ]]
    cab_table = Table(cab_data, colWidths=[10*cm, 7.5*cm])
    cab_table.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    elementos.append(cab_table)

    # Info do representante
    info_rep = []
    if rep_cnpj:  info_rep.append(f"CNPJ: {rep_cnpj}")
    if rep_cid:   info_rep.append(rep_cid)
    if rep_fone:  info_rep.append(f"Tel: {rep_fone}")
    if rep_email: info_rep.append(rep_email)
    if info_rep:
        elementos.append(Paragraph(" | ".join(info_rep), subtit_style))

    elementos.append(HRFlowable(width="100%", thickness=2,
                                color=colors.HexColor("#2d6a4f"), spaceAfter=8))

    # ── Dados do pedido ────────────────────────────────
    # Monta tabela de cabecalho em formato simples: label | valor | label | valor
    def lin(l1, v1, l2="", v2=""):
        return [
            Paragraph(l1, label_style),
            Paragraph(str(v1 or "—"), campo_style),
            Paragraph(l2, label_style),
            Paragraph(str(v2 or "—"), campo_style),
        ]

    linhas_cab = [
        lin("FORNECEDOR",        ped["forn_nome"],
            "CLIENTE",           ped["cliente_nome"]),
        lin("PDV / LOCAL ENTREGA", ped["pdv_nome"] or "Matriz",
            "DATA DO PEDIDO",    (ped["data_pedido"] or "")[:10]),
        lin("TABELA DE PRECO",   ped["nome_tabela"] or "—",
            "DATA DE ENTREGA",   (ped["data_entrega"] or "—")[:10]),
        lin("PRAZO PAGAMENTO",   ped["prazo_pagamento"] or "—",
            "FRETE",             ped["frete"] or "—"),
    ]
    if ped["nr_pedido_cliente"] or ped["nr_pedido_fornecedor"]:
        linhas_cab.append(
            lin("NR. PEDIDO CLIENTE",    ped["nr_pedido_cliente"] or "—",
                "NR. PEDIDO FORNECEDOR", ped["nr_pedido_fornecedor"] or "—")
        )
    if ped["observacao"]:
        linhas_cab.append(
            lin("OBSERVACAO", ped["observacao"], "", "")
        )

    t_cab = Table(linhas_cab, colWidths=[3.5*cm, 5.25*cm, 3.5*cm, 5.25*cm])
    t_cab.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (0,-1), colors.HexColor("#f5f5f5")),
        ("BACKGROUND",    (2,0), (2,-1), colors.HexColor("#f5f5f5")),
        ("FONTNAME",      (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME",      (2,0), (2,-1), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 8),
        ("TEXTCOLOR",     (0,0), (0,-1), colors.HexColor("#555555")),
        ("TEXTCOLOR",     (2,0), (2,-1), colors.HexColor("#555555")),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#dddddd")),
        ("ROWBACKGROUNDS",(0,0), (-1,-1), [colors.white, colors.HexColor("#fafafa")]),
    ]))
    elementos.append(t_cab)

    elementos.append(HRFlowable(width="100%", thickness=1,
                                color=colors.HexColor("#cccccc"), spaceAfter=6))

    # ── Grade de itens ─────────────────────────────────
    header_style = ParagraphStyle("hdr", parent=styles["Normal"],
                                  fontSize=7, fontName="Helvetica-Bold",
                                  textColor=colors.white)
    cell_style   = ParagraphStyle("cel", parent=styles["Normal"],
                                  fontSize=8)
    cell_r_style = ParagraphStyle("celr", parent=styles["Normal"],
                                  fontSize=8, alignment=TA_RIGHT)

    header_row = [
        Paragraph("CODIGO",    header_style),
        Paragraph("DESCRICAO", header_style),
        Paragraph("UN/CX",     header_style),
        Paragraph("QTD (CX)",  header_style),
        Paragraph("PRECO/CX",  header_style),
        Paragraph("DESC %",    header_style),
        Paragraph("SUBTOTAL",  header_style),
    ]
    rows = [header_row]

    for item in itens:
        (iid, cod, desc, un_cx, qtd,
         preco_tab, desconto, preco_fin, status_item, subtotal) = item
        if not qtd or qtd <= 0:
            continue
        sub = (preco_fin or 0) * qtd * (1 - desc_g / 100)
        total_val += sub
        total_cx  += qtd
        sub_fmt = f"R$ {sub:,.2f}".replace(",","X").replace(".",",").replace("X",".")
        pf_fmt  = f"R$ {(preco_fin or 0):,.2f}".replace(",","X").replace(".",",").replace("X",".")
        desc_txt = f"{desconto:.1f}%".replace(".",",") if desconto else "—"
        rows.append([
            Paragraph(cod or "—",       cell_style),
            Paragraph(desc or "—",      cell_style),
            Paragraph(str(un_cx or 1),  cell_style),
            Paragraph(str(qtd),         cell_r_style),
            Paragraph(pf_fmt,           cell_r_style),
            Paragraph(desc_txt,         cell_r_style),
            Paragraph(sub_fmt,          cell_r_style),
        ])

    col_ws = [2.2*cm, 6.8*cm, 1.5*cm, 1.8*cm, 2.2*cm, 1.5*cm, 2.5*cm]
    t_itens = Table(rows, colWidths=col_ws, repeatRows=1)
    t_itens.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  colors.HexColor("#2d6a4f")),
        ("TEXTCOLOR",     (0,0), (-1,0),  colors.white),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [colors.white, colors.HexColor("#f0f7f4")]),
        ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#cccccc")),
        ("FONTSIZE",      (0,0), (-1,-1), 8),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("ALIGN",         (3,1), (-1,-1), "RIGHT"),
    ]))
    elementos.append(t_itens)
    elementos.append(Spacer(1, 0.4*cm))

    # ── Totais ─────────────────────────────────────────
    tot_fmt = f"R$ {total_val:,.2f}".replace(",","X").replace(".",",").replace("X",".")
    totais_data = [
        ["Total de caixas:", str(total_cx),
         "Total do pedido:", tot_fmt],
    ]
    if desc_g:
        totais_data.append([
            "Desconto geral aplicado:", f"{desc_g:.1f}%", "", ""
        ])

    t_tot = Table(totais_data, colWidths=[4.5*cm, 2.5*cm, 4*cm, 6.5*cm])
    t_tot.setStyle(TableStyle([
        ("FONTNAME",   (0,0), (-1,-1), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 10),
        ("ALIGN",      (1,0), (1,-1), "RIGHT"),
        ("ALIGN",      (3,0), (3,-1), "RIGHT"),
        ("TEXTCOLOR",  (2,0), (3,-1), colors.HexColor("#2d6a4f")),
        ("TOPPADDING", (0,0), (-1,-1), 4),
    ]))
    elementos.append(t_tot)

    elementos.append(Spacer(1, 0.8*cm))
    elementos.append(HRFlowable(width="100%", thickness=1,
                                color=colors.HexColor("#cccccc"), spaceAfter=6))

    # ── Assinatura ─────────────────────────────────────
    ass_data = [[
        Paragraph("_______________________________<br/>Representante Comercial",
                  ParagraphStyle("ass", parent=styles["Normal"],
                                 fontSize=8, alignment=TA_CENTER)),
        Paragraph("_______________________________<br/>Cliente / Comprador",
                  ParagraphStyle("ass2", parent=styles["Normal"],
                                 fontSize=8, alignment=TA_CENTER)),
    ]]
    t_ass = Table(ass_data, colWidths=[8.75*cm, 8.75*cm])
    t_ass.setStyle(TableStyle([
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("TOPPADDING", (0,0), (-1,-1), 20),
    ]))
    elementos.append(t_ass)
    elementos.append(Spacer(1, 0.5*cm))

    from datetime import datetime as _dt
    elementos.append(Paragraph(
        f"Documento gerado pelo PepperCRM em {_dt.now().strftime('%d/%m/%Y %H:%M')}",
        rodape_style))

    doc.build(elementos)
    buf.seek(0)
    return buf


def _form_editar_cabecalho(ped_id, ped):
    with st.form(f"cab_{ped_id}"):
        col1, col2 = st.columns(2)
        with col1:
            nr_cli  = st.text_input("Nr. pedido cliente",    value=ped["nr_pedido_cliente"]    or "")
            nr_forn = st.text_input("Nr. pedido fornecedor", value=ped["nr_pedido_fornecedor"] or "")
            prazo   = st.text_input("Prazo de pagamento",    value=ped["prazo_pagamento"]      or "")
        with col2:
            frete   = st.text_input("Frete",                 value=ped["frete"]                or "")
            desc_g  = st.number_input("Desconto geral (%)", min_value=0.0, max_value=100.0,
                                      value=float(ped["desconto_geral"] or 0), step=0.5)
            entrega = st.text_input("Data de entrega",       value=ped["data_entrega"]         or "",
                                    placeholder="AAAA-MM-DD")
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            entrega_prev_e = st.text_input(
                "Data de entrega prevista", value=ped["data_entrega"] or "",
                placeholder="AAAA-MM-DD")
        with col_e2:
            entrega_real_e = st.text_input(
                "Data de entrega realizada",
                value=ped["data_entrega_realizada"] or "",
                placeholder="AAAA-MM-DD — preencha quando entregue")
        obs    = st.text_input("Observação", value=ped["observacao"] or "")
        salvar = st.form_submit_button("💾 Salvar cabeçalho", type="primary")

    if salvar:
        conn = conectar()
        campos = {
            "nr_pedido_cliente":    (ped["nr_pedido_cliente"],    nr_cli    or None),
            "nr_pedido_fornecedor": (ped["nr_pedido_fornecedor"], nr_forn   or None),
            "prazo_pagamento":      (ped["prazo_pagamento"],      prazo     or None),
            "frete":                (ped["frete"],                frete     or None),
            "desconto_geral":       (ped["desconto_geral"],       desc_g),
            "data_entrega":         (ped["data_entrega"],         entrega   or None),
            "observacao":           (ped["observacao"],           obs       or None),
        }
        for campo, (antes, depois) in campos.items():
            if str(antes or "") != str(depois or ""):
                registrar_historico(conn, ped_id, campo, antes, depois)
        conn.execute("""UPDATE pedido SET
            nr_pedido_cliente=?, nr_pedido_fornecedor=?,
            prazo_pagamento=?, frete=?, desconto_geral=?,
            data_entrega=?, data_entrega_realizada=?, observacao=?
            WHERE pedido_id=?""",
            (nr_cli or None, nr_forn or None, prazo or None,
             frete or None, desc_g,
             entrega_prev_e or None,
             entrega_real_e or None,
             obs or None, ped_id))
        conn.commit(); conn.close()
        st.success("✅ Cabeçalho atualizado!")
        st.rerun()


def _tela_itens_pedido(ped_id, ped, editavel):
    itens = query("""
        SELECT pi.pedido_item_id, p.codigo_produto, p.descricao_curta,
               p.unidades_caixa, pi.quantidade,
               pi.preco_tabela, pi.desconto, pi.preco_final,
               pi.status_item,
               ROUND(pi.quantidade * pi.preco_final, 2) AS subtotal
        FROM pedido_item pi
        JOIN produto p ON pi.produto_id=p.produto_id
        WHERE pi.pedido_id=?
        ORDER BY p.descricao_curta""", (ped_id,))

    if not itens:
        st.info("Nenhum item neste pedido."); return

    total_bruto = sum(r[9] for r in itens if r[9])
    desc_g      = float(ped["desconto_geral"] or 0)
    total_final = total_bruto * (1 - desc_g / 100)

    hc = st.columns([1.2, 3, 0.8, 0.8, 1.2, 0.8, 1.2, 1.5, 1.2])
    for col, txt in zip(hc, ["Código","Descrição","Un/Cx","Qtd.","Preço tab.","Desc.%","Preço fin.","Status","Subtotal"]):
        col.markdown(f"<small><b>{txt}</b></small>", unsafe_allow_html=True)
    st.divider()

    for item in itens:
        (item_id, codigo, desc_c, un_cx, qtd,
         preco_tab, desconto, preco_fin, status_item, subtotal) = item

        cols = st.columns([1.2, 3, 0.8, 0.8, 1.2, 0.8, 1.2, 1.5, 1.2])
        cols[0].caption(codigo or "—")
        cols[1].write(desc_c or "—")
        cols[2].caption(str(un_cx or "—"))
        cols[8].caption(_brl(subtotal))

        if editavel:
            with cols[3]:
                nova_qtd  = st.number_input("", min_value=0, value=int(qtd or 0),
                                            key=f"qtd_{item_id}", label_visibility="collapsed")
            cols[4].caption(_brl(preco_tab))
            with cols[5]:
                novo_desc = st.number_input("", min_value=0.0, max_value=100.0,
                                            value=float(desconto or 0), step=0.5,
                                            key=f"dsc_{item_id}", label_visibility="collapsed")
            cols[6].caption(_brl(preco_fin))
            with cols[7]:
                novo_status = st.selectbox("", STATUS_ITEM,
                                           index=STATUS_ITEM.index(status_item)
                                                 if status_item in STATUS_ITEM else 0,
                                           key=f"st_{item_id}", label_visibility="collapsed")
            col_sv, col_rm = st.columns(2)
            with col_sv:
                if st.button("💾 Salvar", key=f"sv_{item_id}", use_container_width=True):
                    _salvar_item(ped_id, item_id, qtd, nova_qtd,
                                 desconto, novo_desc, preco_tab,
                                 status_item, novo_status)
            with col_rm:
                if st.button("🗑️ Remover", key=f"rm_{item_id}", use_container_width=True):
                    _remover_item(ped_id, item_id, desc_c)
        else:
            cols[3].caption(str(qtd))
            cols[4].caption(_brl(preco_tab))
            cols[5].caption(f"{desconto or 0}%")
            cols[6].caption(_brl(preco_fin))
            cols[7].caption(f"{ICONE_STATUS.get(status_item,'')} {status_item}")

        st.divider()

    col1, col2, col3 = st.columns(3)
    col1.metric("Itens", len(itens))
    col2.metric("Total bruto", _brl(total_bruto))
    col3.metric(f"Total c/ desc.geral ({desc_g:.1f}%)", _brl(total_final))


def _salvar_item(ped_id, item_id, qtd_antes, qtd_depois,
                 desc_antes, desc_depois, preco_tab,
                 status_antes, status_depois):
    conn = conectar()
    if int(qtd_antes) != int(qtd_depois):
        registrar_historico(conn, ped_id, f"item_{item_id}_quantidade", qtd_antes, qtd_depois)
    if float(desc_antes or 0) != float(desc_depois):
        registrar_historico(conn, ped_id, f"item_{item_id}_desconto", desc_antes, desc_depois)
    if status_antes != status_depois:
        registrar_historico(conn, ped_id, f"item_{item_id}_status", status_antes, status_depois)
    novo_pf = float(preco_tab or 0) * (1 - float(desc_depois) / 100)
    conn.execute("""UPDATE pedido_item
        SET quantidade=?, desconto=?, preco_final=?, status_item=?
        WHERE pedido_item_id=?""",
        (qtd_depois, desc_depois, round(novo_pf, 4), status_depois, item_id))
    conn.commit(); conn.close()
    st.success("Item atualizado!"); st.rerun()


def _remover_item(ped_id, item_id, descricao):
    conn = conectar()
    registrar_historico(conn, ped_id, "item_removido", descricao, None, f"Item #{item_id} removido")
    conn.execute("DELETE FROM pedido_item WHERE pedido_item_id=?", (item_id,))
    conn.commit(); conn.close()
    st.success(f"Item '{descricao}' removido."); st.rerun()


def _form_adicionar_item(ped_id, ped):
    forn_id = ped["fornecedor_id"]
    tab_id  = ped["tabela_preco_id"]
    busca   = st.text_input("Buscar produto (código ou descrição)", key=f"busca_add_{ped_id}")

    if busca and len(busca) >= 2:
        resultados = query("""
            SELECT p.produto_id, p.codigo_produto, p.descricao_curta,
                   p.unidades_caixa, tpi.preco_caixa, tpi.desconto_maximo
            FROM produto p
            LEFT JOIN tabela_preco_item tpi
                   ON tpi.produto_id=p.produto_id AND tpi.tabela_preco_id=?
            WHERE p.fornecedor_id=? AND p.ativo=1
              AND (p.codigo_produto LIKE ? OR p.descricao LIKE ? OR p.descricao_curta LIKE ?)
            ORDER BY p.descricao_curta LIMIT 20
        """, (tab_id, forn_id, f"%{busca}%", f"%{busca}%", f"%{busca}%"))

        if resultados:
            prod = st.selectbox("Produto", resultados,
                                format_func=lambda x: f"{x[1]} — {x[2]} ({_brl(x[4])}/cx)",
                                key=f"prod_sel_add_{ped_id}")
            col1, col2 = st.columns(2)
            with col1:
                nova_qtd  = st.number_input("Quantidade (cx)", min_value=1, value=1,
                                            key=f"nqtd_{ped_id}")
            with col2:
                novo_desc = st.number_input("Desconto (%)", min_value=0.0,
                                            max_value=float(prod[5] or 100),
                                            value=0.0, step=0.5, key=f"ndsc_{ped_id}")

            if st.button("➕ Adicionar item", type="primary", key=f"btn_add_item_{ped_id}"):
                preco_tab   = float(prod[4] or 0)
                preco_final = preco_tab * (1 - novo_desc / 100)
                existe = query("""SELECT pedido_item_id FROM pedido_item
                    WHERE pedido_id=? AND produto_id=?""", (ped_id, prod[0]))
                conn = conectar()
                if existe:
                    conn.execute("""UPDATE pedido_item SET quantidade=quantidade+?, status_item='NORMAL'
                        WHERE pedido_id=? AND produto_id=?""", (nova_qtd, ped_id, prod[0]))
                    registrar_historico(conn, ped_id, "item_qty_incrementada", None, nova_qtd,
                                        f"Produto #{prod[0]}")
                else:
                    conn.execute("""INSERT INTO pedido_item
                        (pedido_id, produto_id, preco_tabela, desconto, preco_final, quantidade, status_item)
                        VALUES (?,?,?,?,?,?,'NORMAL')""",
                        (ped_id, prod[0], preco_tab, novo_desc, round(preco_final,4), nova_qtd))
                    registrar_historico(conn, ped_id, "item_adicionado", None, prod[2], f"'{prod[2]}' adicionado")
                conn.commit(); conn.close()
                st.success(f"'{prod[2]}' adicionado!"); st.rerun()
        else:
            st.info("Nenhum produto encontrado.")


def _form_alterar_status(ped_id, ped):
    st.subheader("Status do pedido")
    status_atual = ped["status_pedido"]
    idx = STATUS_PEDIDO.index(status_atual) if status_atual in STATUS_PEDIDO else 0

    col1, col2 = st.columns([2,1])
    with col1:
        novo_status = st.selectbox("Alterar status para", STATUS_PEDIDO,
                                   index=idx, key=f"novo_status_{ped_id}")
    with col2:
        obs_status = st.text_input("Observação", key=f"obs_status_{ped_id}")

    if st.button("✓ Confirmar alteração de status", type="primary",
                 key=f"btn_status_{ped_id}",
                 disabled=(novo_status == status_atual)):
        conn = conectar()
        registrar_historico(conn, ped_id, "status_pedido",
                            status_atual, novo_status, obs_status or None)
        conn.execute("UPDATE pedido SET status_pedido=? WHERE pedido_id=?",
                     (novo_status, ped_id))
        conn.commit(); conn.close()
        icone = ICONE_STATUS.get(novo_status,"")
        st.success(f"{icone} Status alterado para **{novo_status}**!")
        st.rerun()


def _tela_historico():
    ped_id = st.session_state.get("pedido_ativo_id")
    if not ped_id:
        st.info("Selecione um pedido na aba Lista para ver o histórico.")
        return

    st.subheader(f"Histórico do Pedido #{ped_id}")
    historico = query("""SELECT data_hora, campo, valor_antes, valor_depois, observacao
        FROM pedido_historico WHERE pedido_id=?
        ORDER BY historico_id DESC""", (ped_id,))

    if not historico:
        st.info("Nenhuma alteração registrada para este pedido."); return

    df = pd.DataFrame(historico, columns=["Data/Hora","Campo","Antes","Depois","Observacao"])
    df["Antes"]     = df["Antes"].fillna("—")
    df["Depois"]    = df["Depois"].fillna("—")
    df["Observacao"] = df["Observacao"].fillna("—")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption(f"{len(histórico)} registro(s) de alteração")

    # Exportar histórico
    buf = io.BytesIO()
    df.to_excel(buf, index=False, sheet_name=f"Histórico Pedido {ped_id}")
    buf.seek(0)
    st.download_button("⬇️ Exportar histórico Excel", data=buf,
                       file_name=f"histórico_pedido_{ped_id}.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")