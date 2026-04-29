# mix_analise.py — PepperCRM
# Análise de cobertura de mix ideal por PDV / cliente
# Mostra: cobertura %, produtos nunca pedidos, sugestão de oferta

import streamlit as st
import pandas as pd
import io
from database import query


def _ir(p):
    st.session_state["pagina"] = p
    st.rerun()


def _fmt_brl(v):
    if not v:
        return "—"
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ═══════════════════════════════════════════════════════
# ENTRADA PRINCIPAL
# ═══════════════════════════════════════════════════════

def tela_mix_analise():
    st.header("Análise de mix por PDV")
    if st.button("⬅ Voltar"):
        _ir("home")

    ABAS_MIX = {"pdv":"Análise por PDV","geral":"Visão geral","oferta":"Sugestão de oferta"}
    if "mix_aba" not in st.session_state: st.session_state["mix_aba"] = "pdv"
    cols = st.columns(3)
    for col,(k,v) in zip(cols, ABAS_MIX.items()):
        ativa = st.session_state["mix_aba"] == k
        if col.button(v, key=f"mxnav_{k}", use_container_width=True,
                      type="primary" if ativa else "secondary"):
            st.session_state["mix_aba"] = k; st.rerun()
    st.divider()
    a = st.session_state["mix_aba"]
    if a=="pdv":    _analise_pdv()
    elif a=="geral":_visao_geral()
    elif a=="oferta":_sugestao_oferta()


# ═══════════════════════════════════════════════════════
# 1. ANÁLISE POR PDV
# ═══════════════════════════════════════════════════════

def _analise_pdv():
    st.subheader("Cobertura de mix — PDV específico")

    clientes = query("""
        SELECT cliente_id, nome_fantasia, cidade, estado
        FROM cliente WHERE ativo=1 ORDER BY nome_fantasia
    """)
    if not clientes:
        st.info("Nenhum cliente cadastrado.")
        return

    col1, col2 = st.columns(2)
    with col1:
        cli_sel = st.selectbox(
            "Cliente",
            clientes,
            format_func=lambda x: f"{x[1]} — {x[2]}/{x[3]}",
            key="mx_cli"
        )
    with col2:
        forns_cli = query("""
            SELECT f.fornecedor_id, f.nome_fantasia
            FROM cliente_fornecedor cf
            JOIN fornecedor f ON cf.fornecedor_id = f.fornecedor_id
            WHERE cf.cliente_id=? AND cf.ativo=1 AND f.ativo=1
            ORDER BY f.nome_fantasia
        """, (cli_sel[0],))

        if not forns_cli:
            st.warning("Este cliente não tem fornecedores vinculados.")
            return
        forn_sel = st.selectbox(
            "Fornecedor",
            forns_cli,
            format_func=lambda x: x[1],
            key="mx_forn"
        )

    cli_id  = cli_sel[0]
    forn_id = forn_sel[0]

    # PDVs do cliente
    pdvs = query("""
        SELECT pdv_id, numero_loja, nome_loja
        FROM pdv WHERE cliente_id=? AND ativo=1
        ORDER BY numero_loja, nome_loja
    """, (cli_id,))

    pdv_opts = [(None, "— Cliente direto (sem PDV)")] + [
        (p[0], f"Loja {p[1]} — {p[2]}") for p in pdvs
    ]
    pdv_sel = st.selectbox(
        "PDV / Loja",
        pdv_opts,
        format_func=lambda x: x[1],
        key="mx_pdv"
    )
    pdv_id = pdv_sel[0]

    # Período de análise
    periodo = st.selectbox(
        "Considerar pedidos dos últimos",
        ["30 dias", "60 dias", "90 dias", "6 meses", "1 ano", "Todo o histórico"],
        index=1,
        key="mx_per"
    )
    dias_map = {
        "30 dias": 30, "60 dias": 60, "90 dias": 90,
        "6 meses": 180, "1 ano": 365
    }
    if periodo in dias_map:
        data_corte = f"date('now','-{dias_map[periodo]} days')"
    else:
        data_corte = "date('1900-01-01')"

    if st.button("Analisar mix", type="primary", key="btn_mx"):
        _executar_analise(cli_id, forn_id, pdv_id, data_corte, pdv_sel[1])


def _executar_analise(cli_id, forn_id, pdv_id, data_corte, pdv_label):
    # Mix cadastrado para este PDV/fornecedor
    if pdv_id:
        mix = query("""
            SELECT p.produto_id, p.codigo_produto, p.descricao_curta,
                   p.unidades_caixa, tpi.preco_caixa
            FROM mix_cliente mc
            JOIN produto p ON mc.produto_id = p.produto_id
            LEFT JOIN cliente_fornecedor cf
                   ON cf.cliente_id=mc.cliente_id AND cf.fornecedor_id=mc.fornecedor_id
            LEFT JOIN tabela_preco_item tpi
                   ON tpi.tabela_preco_id=cf.tabela_preco_id AND tpi.produto_id=p.produto_id
            WHERE mc.cliente_id=? AND mc.fornecedor_id=? AND mc.pdv_id=? AND mc.ativo=1
            ORDER BY p.descricao_curta
        """, (cli_id, forn_id, pdv_id))
    else:
        mix = query("""
            SELECT p.produto_id, p.codigo_produto, p.descricao_curta,
                   p.unidades_caixa, tpi.preco_caixa
            FROM mix_cliente mc
            JOIN produto p ON mc.produto_id = p.produto_id
            LEFT JOIN cliente_fornecedor cf
                   ON cf.cliente_id=mc.cliente_id AND cf.fornecedor_id=mc.fornecedor_id
            LEFT JOIN tabela_preco_item tpi
                   ON tpi.tabela_preco_id=cf.tabela_preco_id AND tpi.produto_id=p.produto_id
            WHERE mc.cliente_id=? AND mc.fornecedor_id=? AND mc.pdv_id IS NULL AND mc.ativo=1
            ORDER BY p.descricao_curta
        """, (cli_id, forn_id))

    if not mix:
        st.warning("Nenhum produto no mix para este PDV/fornecedor. "
                   "Cadastre o mix em Clientes → Mix por PDV.")
        return

    total_mix = len(mix)

    # Para cada produto do mix, verifica se foi pedido no período
    resultado = []
    for prod in mix:
        prod_id = prod[0]

        ultimo_pedido = query(f"""
            SELECT p.data_pedido, pi.quantidade, pi.preco_final
            FROM pedido_item pi
            JOIN pedido p ON pi.pedido_id = p.pedido_id
            WHERE pi.produto_id=?
              AND p.cliente_id=?
              AND p.fornecedor_id=?
              AND {'p.pdv_id=?' if pdv_id else 'p.pdv_id IS NULL'}
              AND p.status_pedido NOT IN ('CANCELADO')
              AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
              AND p.data_pedido >= {data_corte}
            ORDER BY p.data_pedido DESC LIMIT 1
        """, (prod_id, cli_id, forn_id, pdv_id) if pdv_id else (prod_id, cli_id, forn_id))

        nunca_pedido = query(f"""
            SELECT COUNT(*) FROM pedido_item pi
            JOIN pedido p ON pi.pedido_id=p.pedido_id
            WHERE pi.produto_id=?
              AND p.cliente_id=?
              AND p.fornecedor_id=?
              AND {'p.pdv_id=?' if pdv_id else 'p.pdv_id IS NULL'}
              AND p.status_pedido NOT IN ('CANCELADO')
        """, (prod_id, cli_id, forn_id, pdv_id) if pdv_id else (prod_id, cli_id, forn_id))

        foi_pedido_periodo = len(ultimo_pedido) > 0
        total_historico    = nunca_pedido[0][0] if nunca_pedido else 0

        resultado.append({
            "produto_id":    prod_id,
            "codigo":        prod[1] or "—",
            "descricao":     prod[2] or "—",
            "un_cx":         prod[3] or 1,
            "preco":         prod[4],
            "pedido_period": foi_pedido_periodo,
            "ultima_data":   ultimo_pedido[0][0] if ultimo_pedido else None,
            "ultima_qtd":    ultimo_pedido[0][1] if ultimo_pedido else None,
            "nunca_pedido":  total_historico == 0,
        })

    pedidos_no_periodo = sum(1 for r in resultado if r["pedido_period"])
    nunca_pedidos      = sum(1 for r in resultado if r["nunca_pedido"])
    cobertura_pct      = round(pedidos_no_periodo / total_mix * 100, 1)

    # ── Métricas de cobertura ────────────────────────
    st.subheader(f"Mix: {pdv_label}")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total no mix",          total_mix)
    col2.metric("Pedidos no periodo",    pedidos_no_periodo)
    col3.metric("Cobertura do mix",      f"{cobertura_pct}%")
    col4.metric("Nunca pedidos",         nunca_pedidos)

    # Barra de progresso de cobertura
    cor = "normal" if cobertura_pct >= 70 else ("off" if cobertura_pct < 40 else "inverse")
    st.progress(cobertura_pct / 100)

    # ── Tabela completa ──────────────────────────────
    st.divider()

    # Filtro de exibição
    filtro = st.radio(
        "Exibir",
        ["Todos", "Pedidos no periodo", "Não pedidos no período", "Nunca pedidos"],
        horizontal=True,
        key="mx_filtro"
    )

    df_data = []
    for r in resultado:
        if filtro == "Pedidos no periodo"      and not r["pedido_period"]: continue
        if filtro == "Não pedidos no período"  and r["pedido_period"]:     continue
        if filtro == "Nunca pedidos"           and not r["nunca_pedido"]:  continue

        situacao = "✅ Ativo" if r["pedido_period"] else (
                   "🆕 Nunca pedido" if r["nunca_pedido"] else "⚠️ Ausente no período")

        df_data.append({
            "Código":         r["codigo"],
            "Descrição":      r["descricao"],
            "Un/Cx":          r["un_cx"],
            "Preço/Cx":       _fmt_brl(r["preco"]),
            "Situacao":       situacao,
            "Último pedido":  r["ultima_data"] or "—",
            "Última qtd.":    r["ultima_qtd"] or "—",
        })

    if df_data:
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"{len(df_data)} produto(s) exibido(s)")

        # Exportar
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w:
            df.to_excel(w, index=False, sheet_name="Mix PDV")
        buf.seek(0)
        st.download_button(
            "⬇️ Exportar Excel",
            data=buf,
            file_name=f"mix_analise_{pdv_label.replace(' ','_')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # Guarda resultado para aba de sugestão
    st.session_state["mx_resultado"] = resultado
    st.session_state["mx_cli_id"]    = cli_id
    st.session_state["mx_forn_id"]   = forn_id
    st.session_state["mx_pdv_label"] = pdv_label


# ═══════════════════════════════════════════════════════
# 2. VISÃO GERAL — TODOS OS CLIENTES
# ═══════════════════════════════════════════════════════

def _visao_geral():
    st.subheader("Cobertura de mix — todos os clientes")

    forns = query(
        "SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia"
    )
    if not forns:
        st.info("Nenhum fornecedor cadastrado.")
        return

    col1, col2 = st.columns(2)
    with col1:
        forn_sel = st.selectbox("Fornecedor", forns,
                                format_func=lambda x: x[1], key="vg_forn")
    with col2:
        periodo = st.selectbox(
            "Período de análise",
            ["30 dias", "60 dias", "90 dias", "6 meses", "Todo o histórico"],
            index=1, key="vg_per"
        )
    dias_map = {"30 dias":30,"60 dias":60,"90 dias":90,"6 meses":180}
    data_corte = f"date('now','-{dias_map[periodo]} days')" \
                 if periodo in dias_map else "date('1900-01-01')"

    forn_id = forn_sel[0]

    dados = query(f"""
        SELECT c.nome_fantasia                              AS cliente,
               COALESCE(pdv.nome_loja,'Direto')            AS pdv,
               COUNT(DISTINCT mc.produto_id)               AS total_mix,
               COUNT(DISTINCT CASE
                   WHEN EXISTS (
                       SELECT 1 FROM pedido_item pi2
                       JOIN pedido p2 ON pi2.pedido_id=p2.pedido_id
                       WHERE pi2.produto_id=mc.produto_id
                         AND p2.cliente_id=mc.cliente_id
                         AND p2.fornecedor_id=mc.fornecedor_id
                         AND p2.status_pedido NOT IN ('CANCELADO')
                         AND pi2.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
                         AND p2.data_pedido >= {data_corte}
                   ) THEN mc.produto_id END)               AS pedidos_periodo
        FROM mix_cliente mc
        JOIN cliente c ON mc.cliente_id=c.cliente_id
        LEFT JOIN pdv  ON mc.pdv_id=pdv.pdv_id
        WHERE mc.fornecedor_id=? AND mc.ativo=1 AND c.ativo=1
        GROUP BY mc.cliente_id, mc.pdv_id, c.nome_fantasia, pdv.nome_loja
        ORDER BY c.nome_fantasia, pdv.nome_loja
    """, (forn_id,))

    if not dados:
        st.info("Nenhum dado de mix encontrado para este fornecedor.")
        return

    df = pd.DataFrame(dados,
                      columns=["Cliente","PDV","Total mix","Pedidos no periodo"])
    df["Cobertura (%)"] = (
        df["Pedidos no periodo"] / df["Total mix"] * 100
    ).round(1).fillna(0)
    df["Situacao"] = df["Cobertura (%)"].apply(
        lambda v: "✅ Boa" if v >= 70 else ("⚠️ Parcial" if v >= 40 else "🔴 Baixa")
    )

    # Métricas gerais
    col1, col2, col3 = st.columns(3)
    col1.metric("PDVs analisados", len(df))
    col2.metric("Cobertura média",
                f"{df['Cobertura (%)'].mean():.1f}%".replace(".",","))
    col3.metric("PDVs com cobertura < 40%",
                len(df[df["Cobertura (%)"] < 40]))

    st.dataframe(df, use_container_width=True, hide_index=True)

    # Gráfico de barras — cobertura por PDV
    if len(df) <= 20:
        df_chart = df.copy()
        df_chart.index = df_chart["Cliente"] + " / " + df_chart["PDV"]
        st.bar_chart(df_chart["Cobertura (%)"])

    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df.to_excel(w, index=False, sheet_name="Cobertura mix")
    buf.seek(0)
    st.download_button(
        "⬇️ Exportar Excel",
        data=buf,
        file_name="cobertura_mix_geral.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# ═══════════════════════════════════════════════════════
# 3. SUGESTÃO DE OFERTA
# ═══════════════════════════════════════════════════════

def _sugestao_oferta():
    st.subheader("Sugestão de oferta para próxima visita")
    st.caption(
        "Baseada nos produtos do mix que nunca foram pedidos ou "
        "que estão ausentes no período analisado."
    )

    resultado = st.session_state.get("mx_resultado")
    pdv_label = st.session_state.get("mx_pdv_label", "")

    if not resultado:
        st.info(
            "Execute a análise na aba **Análise por PDV** primeiro para "
            "gerar as sugestões."
        )
        return

    # Produtos para sugerir: nunca pedidos primeiro, depois ausentes no período
    nunca   = [r for r in resultado if r["nunca_pedido"]]
    ausente = [r for r in resultado if not r["pedido_period"] and not r["nunca_pedido"]]

    if not nunca and not ausente:
        st.success(
            "Parabéns! Todos os produtos do mix foram pedidos no período analisado. "
            "Não há sugestões de oferta."
        )
        return

    st.write(f"**PDV:** {pdv_label}")

    total_oport = len(nunca) + len(ausente)
    valor_oport = sum(
        (r["preco"] or 0)
        for r in (nunca + ausente)
    )

    col1, col2 = st.columns(2)
    col1.metric("Produtos a oferecer", total_oport)
    col2.metric("Potencial (R$/cx cada)", _fmt_brl(valor_oport))

    if nunca:
        st.subheader("🆕 Nunca foram pedidos — prioridade máxima")
        st.caption("Estes produtos estão no mix mas o cliente nunca comprou.")
        _tabela_sugestao(nunca)

    if ausente:
        st.subheader("⚠️ Ausentes no período")
        st.caption("Já foram pedidos antes, mas não no período analisado.")
        _tabela_sugestao(ausente)

    # Exportar lista de sugestões
    todos = nunca + ausente
    df_exp = pd.DataFrame([{
        "Código":     r["codigo"],
        "Descrição":  r["descricao"],
        "Un/Cx":      r["un_cx"],
        "Preço/Cx":   r["preco"] or 0,
        "Tipo":       "Nunca pedido" if r["nunca_pedido"] else "Ausente no período",
        "Último ped.": r["ultima_data"] or "—",
    } for r in todos])

    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df_exp.to_excel(w, index=False, sheet_name="Sugestão oferta")
    buf.seek(0)
    st.download_button(
        "⬇️ Exportar lista de sugestões",
        data=buf,
        file_name=f"sugestao_oferta_{pdv_label.replace(' ','_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


def _tabela_sugestao(lista):
    df = pd.DataFrame([{
        "Código":       r["codigo"],
        "Descrição":    r["descricao"],
        "Un/Cx":        r["un_cx"],
        "Preço/Cx":     _fmt_brl(r["preco"]),
        "Último ped.":  r["ultima_data"] or "Nunca",
    } for r in lista])
    st.dataframe(df, use_container_width=True, hide_index=True)