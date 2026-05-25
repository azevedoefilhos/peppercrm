# despesas.py — Módulo de controle de despesas operacionais
# PepperCRM — Azevedo e Filhos Representação Comercial

import streamlit as st
import pandas as pd
import io
from datetime import date, timedelta
from database import query, execute_write, conectar, _check_supabase

# ── Constantes ────────────────────────────────────────────────────────────────

CATEGORIAS = [
    "Combustível",
    "Estacionamento",
    "Pedágio",
    "Transporte (Uber/Táxi/Ônibus)",
    "Hospedagem",
    "Alimentação",
    "Xerox / Impressão",
    "Amostras / Brindes",
    "Correios / Envio",
    "Material de escritório",
    "Telefone / Internet",
    "Outros",
]

FORMAS_PGTO = ["Dinheiro", "Pix", "Cartão de débito", "Cartão de crédito"]
COMBUSTIVEL_TIPO = ["Gasolina", "Etanol (Álcool)", "Diesel"]


# ── Criação da tabela ─────────────────────────────────────────────────────────

def _criar_tabela():
    if _check_supabase():
        execute_write("""
            CREATE TABLE IF NOT EXISTS despesa (
                despesa_id        SERIAL PRIMARY KEY,
                data_despesa      DATE NOT NULL,
                categoria         TEXT NOT NULL,
                descricao         TEXT,
                cliente_id        INTEGER REFERENCES cliente(cliente_id),
                fornecedor_id     INTEGER REFERENCES fornecedor(fornecedor_id),
                tipo_visita       TEXT,
                valor             NUMERIC(10,2),
                forma_pagamento   TEXT,
                combustivel_tipo  TEXT,
                km_inicial        NUMERIC(10,1),
                km_final          NUMERIC(10,1),
                preco_litro       NUMERIC(10,3),
                media_km_litro    NUMERIC(10,2),
                reembolsavel      BOOLEAN DEFAULT FALSE,
                reembolsado       BOOLEAN DEFAULT FALSE,
                foto_base64       TEXT,
                foto_comprovante  TEXT,
                observacao        TEXT,
                ativo             BOOLEAN DEFAULT TRUE
            )
        """)
    else:
        execute_write("""
            CREATE TABLE IF NOT EXISTS despesa (
                despesa_id        INTEGER PRIMARY KEY AUTOINCREMENT,
                data_despesa      TEXT NOT NULL,
                categoria         TEXT NOT NULL,
                descricao         TEXT,
                cliente_id        INTEGER,
                fornecedor_id     INTEGER,
                tipo_visita       TEXT,
                valor             REAL,
                forma_pagamento   TEXT,
                combustivel_tipo  TEXT,
                km_inicial        REAL,
                km_final          REAL,
                preco_litro       REAL,
                media_km_litro    REAL,
                reembolsavel      INTEGER DEFAULT 0,
                reembolsado       INTEGER DEFAULT 0,
                foto_base64       TEXT,
                foto_comprovante  TEXT,
                observacao        TEXT,
                ativo             INTEGER DEFAULT 1
            )
        """)


# ── Entrada de despesa ────────────────────────────────────────────────────────

def _form_nova_despesa():
    st.subheader("➕ Registrar despesa")

    clientes  = query("SELECT cliente_id, nome_fantasia FROM cliente ORDER BY nome_fantasia")
    fornecs   = query("SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo!=0 ORDER BY nome_fantasia")

    cli_opts  = [(None, "— Nenhum cliente específico —")] + [(c[0], c[1]) for c in clientes]
    forn_opts = [(None, "— Nenhum fornecedor —")] + [(f[0], f[1]) for f in fornecs]

    with st.form("nova_despesa", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            data_d = st.date_input("Data", value=date.today(), key="nd_data")
            categoria = st.selectbox("Categoria", CATEGORIAS, key="nd_cat")
            cli_sel = st.selectbox("Cliente visitado / motivo",
                                   cli_opts, format_func=lambda x: x[1], key="nd_cli")
            forn_sel = st.selectbox("Fornecedor relacionado",
                                    forn_opts, format_func=lambda x: x[1], key="nd_forn")
        with col2:
            tipo_visita = st.selectbox("Tipo de atividade", [
                "— Não se aplica —",
                "Prospecção",
                "Visita de manutenção",
                "Entrega de amostras",
                "Reunião comercial",
                "Visita técnica",
                "Cobrança",
                "Outro",
            ], key="nd_tipo")
            forma_pgto = st.selectbox("Forma de pagamento", FORMAS_PGTO, key="nd_forma")
            reembolsavel = st.checkbox("Despesa reembolsável pela representada", key="nd_reimb")

        descricao = st.text_input("Descrição / Justificativa", key="nd_desc",
                                  placeholder="Ex: Visita ao Empório Lapilli — apresentação Diet House")

        # Campos de combustível
        is_comb = categoria == "Combustível"
        valor_calculado = None
        if is_comb:
            st.markdown("**⛽ Detalhes do combustível**")
            cc1, cc2, cc3, cc4 = st.columns(4)
            comb_tipo  = cc1.selectbox("Tipo", COMBUSTIVEL_TIPO, key="nd_comb_tipo")
            km_ini     = cc2.number_input("KM inicial", min_value=0.0, step=0.1, key="nd_km_ini")
            km_fim     = cc3.number_input("KM final",   min_value=0.0, step=0.1, key="nd_km_fim")
            preco_l    = cc4.number_input("R$/litro", min_value=0.0, step=0.01,
                                          format="%.3f", key="nd_preco_l")
            media_km   = st.number_input("Média do veículo (km/litro)",
                                         min_value=0.1, value=12.0, step=0.1, key="nd_media")
            km_total   = km_fim - km_ini
            if km_total > 0 and media_km > 0 and preco_l > 0:
                litros = km_total / media_km
                valor_calculado = round(litros * preco_l, 2)
                st.info(f"📏 {km_total:.1f} km rodados → "
                        f"{litros:.2f} litros × R$ {preco_l:.3f} = "
                        f"**R$ {valor_calculado:.2f}**")
        else:
            comb_tipo = km_ini = km_fim = preco_l = media_km = None

        col_v1, col_v2 = st.columns(2)
        with col_v1:
            valor = col_v1.number_input(
                "Valor (R$)",
                min_value=0.0, step=0.01, format="%.2f",
                value=float(valor_calculado) if valor_calculado else 0.0,
                key="nd_valor")
        with col_v2:
            obs = col_v2.text_input("Observação", key="nd_obs")

        # Upload de comprovante
        foto_b64 = None
        foto_file = st.file_uploader(
            "📷 Foto do comprovante (NF/Recibo) — opcional",
            type=["jpg","jpeg","png","webp","pdf"],
            key="nd_foto",
            help="Imagem será comprimida automaticamente antes de salvar")
        if foto_file:
            import base64
            from PIL import Image
            import io as _io
            if foto_file.type != "application/pdf":
                img = Image.open(foto_file)
                # Reduz para max 1200px e converte para JPEG
                img.thumbnail((1200, 1200), Image.LANCZOS)
                buf_img = _io.BytesIO()
                img.save(buf_img, format="JPEG", quality=70, optimize=True)
                foto_b64 = base64.b64encode(buf_img.getvalue()).decode()
                kb = len(buf_img.getvalue()) // 1024
                st.caption(f"✅ Foto processada — {kb} KB")
            else:
                foto_b64 = base64.b64encode(foto_file.read()).decode()
                kb = len(foto_b64) * 3 // 4 // 1024
                st.caption(f"✅ PDF anexado — ~{kb} KB")

        salvar = st.form_submit_button("💾 Salvar despesa", type="primary",
                                       use_container_width=True)

    if salvar:
        if valor <= 0 and not is_comb:
            st.warning("Informe o valor da despesa.")
            return
        if not descricao.strip() and cli_sel[0] is None:
            st.warning("Informe uma descrição ou selecione o cliente.")
            return

        _criar_tabela()
        execute_write("""
            INSERT INTO despesa (data_despesa, categoria, descricao,
                cliente_id, fornecedor_id, tipo_visita, valor, forma_pagamento,
                combustivel_tipo, km_inicial, km_final, preco_litro, media_km_litro,
                reembolsavel, foto_base64, observacao, ativo)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,1)
        """, (
            data_d.isoformat(), categoria, descricao.strip() or None,
            cli_sel[0], forn_sel[0],
            None if tipo_visita == "— Não se aplica —" else tipo_visita,
            valor, forma_pgto,
            comb_tipo, km_ini or None, km_fim or None,
            preco_l or None, media_km or None,
            1 if reembolsavel else 0,
            foto_b64,
            obs.strip() or None
        ))
        st.session_state["_desp_msg_ok"] = f"✅ Despesa de R$ {valor:.2f} registrada!"
        st.rerun()


# ── Lista de despesas ─────────────────────────────────────────────────────────

def _lista_despesas():
    st.subheader("📋 Despesas registradas")

    # Filtros
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        hoje = date.today()
        periodo = st.selectbox("Período", [
            "Este mês", "Mês anterior", "Últimos 30 dias",
            "Últimos 90 dias", "Este ano", "Todos"
        ], key="desp_periodo")
    with col2:
        cat_fil = st.selectbox("Categoria", ["Todas"] + CATEGORIAS, key="desp_cat")
    with col3:
        fornecs = query("SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo!=0 ORDER BY nome_fantasia")
        forn_opts = [(0, "Todos os fornecedores")] + [(f[0], f[1]) for f in fornecs]
        forn_fil = st.selectbox("Fornecedor", forn_opts,
                                format_func=lambda x: x[1], key="desp_forn")
    with col4:
        reimb_fil = st.selectbox("Reembolso", ["Todos","Reembolsável","Não reembolsável",
                                                "Pendente reembolso","Reembolsado"],
                                 key="desp_reimb")

    # Calcula datas
    if periodo == "Este mês":
        d_ini = hoje.replace(day=1).isoformat()
        d_fim = hoje.isoformat()
    elif periodo == "Mês anterior":
        primeiro = hoje.replace(day=1)
        ultimo_mes = primeiro - timedelta(days=1)
        d_ini = ultimo_mes.replace(day=1).isoformat()
        d_fim = ultimo_mes.isoformat()
    elif periodo == "Últimos 30 dias":
        d_ini = (hoje - timedelta(days=30)).isoformat()
        d_fim = hoje.isoformat()
    elif periodo == "Últimos 90 dias":
        d_ini = (hoje - timedelta(days=90)).isoformat()
        d_fim = hoje.isoformat()
    elif periodo == "Este ano":
        d_ini = hoje.replace(month=1, day=1).isoformat()
        d_fim = hoje.isoformat()
    else:
        d_ini = "2000-01-01"; d_fim = hoje.isoformat()

    where = ["d.ativo!=0", "d.data_despesa BETWEEN ? AND ?"]
    params = [d_ini, d_fim]
    if cat_fil != "Todas":
        where.append("d.categoria=?"); params.append(cat_fil)
    if forn_fil[0]:
        where.append("d.fornecedor_id=?"); params.append(forn_fil[0])
    if reimb_fil == "Reembolsável":
        where.append("d.reembolsavel=true")
    elif reimb_fil == "Não reembolsável":
        where.append("d.reembolsavel=false")
    elif reimb_fil == "Pendente reembolso":
        where.append("d.reembolsavel=true AND d.reembolsado=false")
    elif reimb_fil == "Reembolsado":
        where.append("d.reembolsado=true")

    despesas = query(f"""
        SELECT d.despesa_id, d.data_despesa, d.categoria,
               COALESCE(d.descricao,'—'),
               COALESCE(c.nome_fantasia,'—') AS cliente,
               COALESCE(f.nome_fantasia,'—') AS fornecedor,
               COALESCE(d.tipo_visita,'—'),
               d.valor, d.forma_pagamento,
               d.reembolsavel, d.reembolsado,
               d.km_inicial, d.km_final, d.combustivel_tipo,
               COALESCE(d.observacao,''),
               d.foto_base64
        FROM despesa d
        LEFT JOIN cliente c ON d.cliente_id=c.cliente_id
        LEFT JOIN fornecedor f ON d.fornecedor_id=f.fornecedor_id
        WHERE {' AND '.join(where)}
        ORDER BY d.data_despesa DESC, d.despesa_id DESC
    """, tuple(params))

    if not despesas:
        st.info("Nenhuma despesa encontrada para os filtros selecionados.")
        return

    # Métricas
    total_geral = sum(r[7] or 0 for r in despesas)
    total_reimb = sum(r[7] or 0 for r in despesas if r[9])
    total_pend  = sum(r[7] or 0 for r in despesas if r[9] and not r[10])
    por_cat = {}
    for r in despesas:
        por_cat[r[2]] = por_cat.get(r[2], 0) + (r[7] or 0)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total despesas", f"R$ {total_geral:,.2f}")
    m2.metric("Reembolsável", f"R$ {total_reimb:,.2f}")
    m3.metric("Pendente reembolso", f"R$ {total_pend:,.2f}")
    m4.metric("Registros", len(despesas))

    # Maior categoria
    if por_cat:
        cat_top = max(por_cat, key=por_cat.get)
        st.caption(f"Maior categoria: **{cat_top}** — R$ {por_cat[cat_top]:,.2f}")

    st.divider()

    # Tabela interativa
    df_desp = pd.DataFrame([{
        "ID":          r[0],
        "Data":        r[1],
        "Categoria":   r[2],
        "Descrição":   r[3],
        "Cliente":     r[4],
        "Fornecedor":  r[5],
        "Valor":       r[7],
        "Pagamento":   r[8],
        "Reemb.":      "✅" if r[10] else ("💰" if r[9] else "—"),
    } for r in despesas])

    sel = st.dataframe(
        df_desp, use_container_width=True, hide_index=True,
        on_select="rerun", selection_mode="single-row",
        column_config={
            "ID":         st.column_config.NumberColumn(width="small"),
            "Data":       st.column_config.TextColumn(width="small"),
            "Categoria":  st.column_config.TextColumn(width="medium"),
            "Descrição":  st.column_config.TextColumn(width="large"),
            "Valor":      st.column_config.NumberColumn(format="R$ %.2f", width="small"),
            "Reemb.":     st.column_config.TextColumn(width="small"),
        },
        key="df_despesas"
    )

    # Detalhe/edição ao selecionar
    rows_sel = sel.selection.rows if sel and sel.selection else []
    if rows_sel:
        idx  = rows_sel[0]
        row  = despesas[idx]
        did  = row[0]
        st.divider()
        st.markdown(f"#### 📄 Despesa #{did} — {row[2]}")
        tab_det, tab_edit, tab_del = st.tabs(["📄 Detalhe", "✏️ Editar", "🗑️ Excluir"])

        with tab_det:
            c1, c2 = st.columns(2)
            c1.markdown(f"**Data:** {row[1]}")
            c1.markdown(f"**Categoria:** {row[2]}")
            c1.markdown(f"**Cliente:** {row[4]}")
            c1.markdown(f"**Fornecedor:** {row[5]}")
            c1.markdown(f"**Tipo visita:** {row[6]}")
            c2.markdown(f"**Valor:** R$ {row[7]:,.2f}")
            c2.markdown(f"**Pagamento:** {row[8]}")
            c2.markdown(f"**Reembolsável:** {'Sim' if row[9] else 'Não'}")
            c2.markdown(f"**Reembolsado:** {'Sim' if row[10] else 'Não'}")
            if row[11] and row[12]:
                km = row[12] - row[11]
                c2.markdown(f"**KM rodados:** {km:.1f} km ({row[13]})")
            if row[14]:
                st.markdown(f"**Observação:** {row[14]}")

            # Exibe foto se existir
            if row[15]:
                import base64
                st.markdown("**📷 Comprovante:**")
                try:
                    img_bytes = base64.b64decode(row[15])
                    st.image(img_bytes, width=400)
                except Exception:
                    st.caption("(comprovante PDF — não visualizável inline)")

            # Marcar como reembolsado
            if row[9] and not row[10]:
                if st.button("✅ Marcar como reembolsado", key=f"reimb_{did}",
                             type="primary"):
                    execute_write("UPDATE despesa SET reembolsado=true WHERE despesa_id=?",
                                  (did,))
                    st.success("Marcado como reembolsado!")
                    st.rerun()

        with tab_edit:
            _form_editar_despesa(did, row)

        with tab_del:
            st.warning(f"⚠️ Confirma exclusão da despesa **{row[2]}** de R$ {row[7]:,.2f}?")
            col_s, col_n = st.columns(2)
            if col_s.button("🗑️ Sim, excluir", key=f"del_desp_{did}",
                            type="primary", use_container_width=True):
                execute_write("UPDATE despesa SET ativo=false WHERE despesa_id=?", (did,))
                st.success("Despesa excluída.")
                st.rerun()
            if col_n.button("Cancelar", key=f"canc_desp_{did}",
                            use_container_width=True):
                st.rerun()

    # Export Excel
    st.divider()
    if st.button("⬇️ Exportar Excel", key="exp_desp_xl"):
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            df_desp.to_excel(w, index=False, sheet_name="Despesas")
        st.download_button("📥 Baixar Excel", data=buf.getvalue(),
                           file_name=f"despesas_{d_ini}_{d_fim}.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


def _form_editar_despesa(did, row):
    """Formulário de edição de despesa existente."""
    clientes = query("SELECT cliente_id, nome_fantasia FROM cliente ORDER BY nome_fantasia")
    fornecs  = query("SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo!=0 ORDER BY nome_fantasia")
    cli_opts  = [(None,"— Nenhum —")] + [(c[0],c[1]) for c in clientes]
    forn_opts = [(None,"— Nenhum —")] + [(f[0],f[1]) for f in fornecs]

    _cli_idx  = next((i for i,x in enumerate(cli_opts)  if x[0]==row[0]),  0) if row else 0
    _forn_idx = next((i for i,x in enumerate(forn_opts) if x[0]==row[0]),  0) if row else 0

    with st.form(f"edit_desp_{did}"):
        col1, col2 = st.columns(2)
        with col1:
            data_d    = col1.date_input("Data", value=date.fromisoformat(str(row[1])[:10]))
            categoria = col1.selectbox("Categoria", CATEGORIAS,
                                       index=CATEGORIAS.index(row[2]) if row[2] in CATEGORIAS else 0)
            cli_sel   = col1.selectbox("Cliente", cli_opts,
                                       format_func=lambda x: x[1], index=_cli_idx)
            forn_sel  = col1.selectbox("Fornecedor", forn_opts,
                                       format_func=lambda x: x[1], index=_forn_idx)
        with col2:
            valor      = col2.number_input("Valor (R$)", value=float(row[7] or 0),
                                           min_value=0.0, step=0.01, format="%.2f")
            forma_pgto = col2.selectbox("Forma pagamento", FORMAS_PGTO,
                                        index=FORMAS_PGTO.index(row[8]) if row[8] in FORMAS_PGTO else 0)
            reembolsavel = col2.checkbox("Reembolsável", value=bool(row[9]))
            reembolsado  = col2.checkbox("Reembolsado",  value=bool(row[10]))

        descricao = st.text_input("Descrição", value=row[3] if row[3] != "—" else "")
        obs       = st.text_input("Observação", value=row[14] or "")

        if st.form_submit_button("💾 Salvar alterações", type="primary",
                                 use_container_width=True):
            execute_write("""
                UPDATE despesa SET data_despesa=?, categoria=?, descricao=?,
                    cliente_id=?, fornecedor_id=?, valor=?, forma_pagamento=?,
                    reembolsavel=?, reembolsado=?, observacao=?
                WHERE despesa_id=?
            """, (data_d.isoformat(), categoria, descricao.strip() or None,
                  cli_sel[0], forn_sel[0], valor, forma_pgto,
                  reembolsavel, reembolsado, obs.strip() or None, did))
            st.success("✅ Despesa atualizada!")
            st.rerun()


# ── Relatório de despesas ─────────────────────────────────────────────────────

def _relatorio_despesas():
    st.subheader("📊 Relatório de despesas")

    hoje = date.today()
    col1, col2, col3 = st.columns(3)
    mes_ano = col1.selectbox("Mês/Ano", [
        f"{(hoje.replace(day=1) - timedelta(days=30*i)).strftime('%m/%Y')}" for i in range(12)
    ], key="rel_desp_mes")
    forn_opts = [(0,"Todos")] + [(f[0],f[1]) for f in query(
        "SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo!=0 ORDER BY nome_fantasia")]
    forn_sel = col2.selectbox("Fornecedor", forn_opts,
                               format_func=lambda x: x[1], key="rel_desp_forn")
    apenas_reimb = col3.checkbox("Apenas reembolsáveis", key="rel_desp_reimb")

    mes, ano = mes_ano.split("/")
    d_ini = f"{ano}-{mes}-01"
    import calendar
    d_fim = f"{ano}-{mes}-{calendar.monthrange(int(ano), int(mes))[1]}"

    where = ["d.ativo!=0", "d.data_despesa BETWEEN ? AND ?"]
    params = [d_ini, d_fim]
    if forn_sel[0]:
        where.append("d.fornecedor_id=?"); params.append(forn_sel[0])
    if apenas_reimb:
        where.append("d.reembolsavel=true")

    despesas = query(f"""
        SELECT d.categoria, SUM(d.valor) as total,
               COUNT(*) as qtd,
               SUM(CASE WHEN d.reembolsavel THEN d.valor ELSE 0 END) as reimb,
               SUM(CASE WHEN d.reembolsado  THEN d.valor ELSE 0 END) as reemb_ok
        FROM despesa d
        WHERE {' AND '.join(where)}
        GROUP BY d.categoria
        ORDER BY total DESC
    """, tuple(params))

    if not despesas:
        st.info("Nenhuma despesa no período.")
        return

    total_geral = sum(r[1] or 0 for r in despesas)
    total_reimb = sum(r[3] or 0 for r in despesas)
    total_reemb = sum(r[4] or 0 for r in despesas)

    m1, m2, m3 = st.columns(3)
    m1.metric("Total do mês", f"R$ {total_geral:,.2f}")
    m2.metric("A reembolsar", f"R$ {(total_reimb - total_reemb):,.2f}")
    m3.metric("Já reembolsado", f"R$ {total_reemb:,.2f}")

    df_rel = pd.DataFrame([{
        "Categoria":  r[0],
        "Valor total": f"R$ {r[1]:,.2f}",
        "Registros":  r[2],
        "Reembolsável": f"R$ {r[3]:,.2f}",
        "Reembolsado":  f"R$ {r[4]:,.2f}",
    } for r in despesas])
    st.dataframe(df_rel, use_container_width=True, hide_index=True)

    # PDF do relatório
    if st.button("📄 Gerar PDF para fornecedor", key="pdf_desp_rel"):
        _pdf_despesas(d_ini, d_fim, forn_sel[1] if forn_sel[0] else "Todos",
                      apenas_reimb, mes_ano)


def _pdf_despesas(d_ini, d_fim, forn_nome, apenas_reimb, mes_ano):
    """Gera PDF de prestação de contas de despesas."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER

    VERDE = colors.HexColor("#2E7D32")
    sty   = getSampleStyleSheet()
    s_t   = ParagraphStyle("t", parent=sty["Title"], fontSize=14, textColor=VERDE)
    s_s   = ParagraphStyle("s", parent=sty["Normal"], fontSize=9, textColor=colors.grey)
    s_td  = ParagraphStyle("td", parent=sty["Normal"], fontSize=8, leading=10)
    s_r   = ParagraphStyle("r", parent=sty["Normal"], fontSize=7,
                            textColor=colors.grey, alignment=TA_CENTER)

    where = ["d.ativo!=0", "d.data_despesa BETWEEN ? AND ?"]
    params = [d_ini, d_fim]
    if forn_nome != "Todos":
        where.append("f.nome_fantasia=?"); params.append(forn_nome)
    if apenas_reimb:
        where.append("d.reembolsavel=true")

    rows = query(f"""
        SELECT d.data_despesa, d.categoria, d.descricao,
               COALESCE(c.nome_fantasia,'—'), d.tipo_visita,
               d.valor, d.forma_pagamento,
               CASE WHEN d.reembolsavel THEN 'Sim' ELSE 'Não' END,
               COALESCE(d.observacao,''), d.foto_base64
        FROM despesa d
        LEFT JOIN cliente c ON d.cliente_id=c.cliente_id
        LEFT JOIN fornecedor f ON d.fornecedor_id=f.fornecedor_id
        WHERE {' AND '.join(where)}
        ORDER BY d.data_despesa
    """, tuple(params))

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=1.5*cm, rightMargin=1.5*cm,
                            topMargin=1.5*cm, bottomMargin=1.5*cm)
    el  = []
    rep = query("SELECT nome_fantasia FROM representante WHERE ativo!=0 LIMIT 1")
    rep_nome = rep[0][0] if rep else "Azevedo e Filhos"

    el.append(Paragraph("Relatório de Despesas Operacionais", s_t))
    el.append(Paragraph(
        f"{rep_nome} | Fornecedor: {forn_nome} | Período: {mes_ano} | "
        f"{'Apenas reembolsáveis' if apenas_reimb else 'Todas as despesas'}",
        s_s))
    el.append(Spacer(1, 0.4*cm))

    cab = ["Data","Categoria","Descrição","Cliente","Tipo visita",
           "Valor","Pgto","Reimb.","Obs."]
    widths = [1.8*cm,2.5*cm,3.5*cm,2.5*cm,2*cm,1.8*cm,2*cm,1.2*cm,2.2*cm]
    tbl = [cab] + [[
        Paragraph(str(r[i] or "—")[:40], s_td) for i in range(9)
    ] for r in rows]

    t = Table(tbl, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0), VERDE),
        ("TEXTCOLOR",     (0,0),(-1,0), colors.white),
        ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0),(-1,-1), 7),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.white, colors.HexColor("#F5F5F5")]),
        ("GRID",          (0,0),(-1,-1), 0.3, colors.HexColor("#CCC")),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("LEFTPADDING",   (0,0),(-1,-1), 3),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ]))
    el.append(t)
    total = sum(r[5] or 0 for r in rows)
    el.append(Spacer(1, 0.3*cm))
    el.append(Paragraph(f"<b>Total: R$ {total:,.2f}</b>", s_s))

    # Anexa fotos dos comprovantes
    fotos = [(r[1], r[2], r[3], r[9]) for r in rows if r[9]]
    if fotos:
        from reportlab.platypus import PageBreak
        from reportlab.lib.utils import ImageReader
        import base64 as _b64
        import io as _io2
        el.append(PageBreak())
        el.append(Paragraph("<b>Comprovantes / NFs</b>", s_s))
        el.append(Spacer(1, 0.3*cm))
        for cat, desc, cli, foto_b64 in fotos:
            try:
                img_bytes = _b64.b64decode(foto_b64)
                img_buf   = _io2.BytesIO(img_bytes)
                from reportlab.platypus import Image as RLImage
                rl_img = RLImage(img_buf, width=14*cm, height=10*cm,
                                 kind='proportional')
                el.append(Paragraph(f"<b>{cat}</b> — {desc or '—'} | {cli}", s_td))
                el.append(rl_img)
                el.append(Spacer(1, 0.5*cm))
            except Exception:
                el.append(Paragraph(f"[Comprovante não disponível — {cat}]", s_td))

    el.append(Spacer(1, 0.3*cm))
    el.append(Paragraph(
        f"PepperCRM — {rep_nome} | Gerado em {date.today().strftime('%d/%m/%Y')} | Confidencial",
        s_r))
    doc.build(el)

    st.download_button("📥 Baixar PDF", data=buf.getvalue(),
                       file_name=f"despesas_{forn_nome.replace(' ','_')}_{mes_ano.replace('/','_')}.pdf",
                       mime="application/pdf")


# ── Tela principal ────────────────────────────────────────────────────────────

def tela_despesas():
    _criar_tabela()

    st.header("💰 Despesas Operacionais")
    if st.button("⬅ Voltar"):
        from crm_app import ir
        ir("home")

    _msg = st.session_state.pop("_desp_msg_ok", None)
    if _msg: st.success(_msg)

    ABAS = {"nova":"➕ Nova despesa",
            "lista":"📋 Despesas",
            "relatorio":"📊 Relatório"}
    if "desp_aba" not in st.session_state:
        st.session_state["desp_aba"] = "nova"

    cols = st.columns(3)
    for col, (k, v) in zip(cols, ABAS.items()):
        ativa = st.session_state["desp_aba"] == k
        if col.button(v, key=f"desp_nav_{k}", use_container_width=True,
                      type="primary" if ativa else "secondary"):
            st.session_state["desp_aba"] = k
            st.rerun()

    st.divider()
    a = st.session_state["desp_aba"]
    if   a == "nova":      _form_nova_despesa()
    elif a == "lista":     _lista_despesas()
    elif a == "relatorio": _relatorio_despesas()
