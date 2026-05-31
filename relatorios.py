from cache_helpers import cache_clientes, cache_fornecedores, cache_categorias, cache_produtos_fornecedor
# relatorios.py — PepperCRM
# Relatórios de vendas: cliente, fornecedor, produto, categoria,
# comparação de períodos, evolução mensal + exportação Excel

import streamlit as st
from database import _cache_fornecedores, _cache_todos_clientes
import pandas as pd
import io
from database import query

# ─────────────────────────────────────────────────────
# REGRA DE NEGÓCIO — itens válidos para relatório
# Exclui: pedidos CANCELADO
#         itens PENDENTE ou DEVOLVIDO
# ─────────────────────────────────────────────────────
_FILTRO_BASE = """
    FROM pedido_item pi
    JOIN pedido  p  ON pi.pedido_id  = p.pedido_id
    JOIN produto pr ON pi.produto_id = pr.produto_id
    JOIN cliente c  ON p.cliente_id  = c.cliente_id
    JOIN fornecedor f ON p.fornecedor_id = f.fornecedor_id
    LEFT JOIN categoria cat ON pr.categoria_id = cat.categoria_id
    WHERE p.status_pedido  NOT IN ('CANCELADO','RECUSADO')
      AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO')
"""

_VALOR_ITEM = """
    pi.quantidade * pi.preco_final
          * (1 - COALESCE(p.desconto_geral,0)/100.0)
"""


def _ir(p):
    st.session_state["pagina"] = p
    st.session_state["_scroll_topo"] = True
    st.rerun()


def _fmt_brl(v):
    if v is None:
        return "R$ 0,00"
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _excel_download(df: pd.DataFrame, nome: str):
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Relatório")
    buf.seek(0)
    st.download_button(
        label="⬇️ Exportar Excel",
        data=buf,
        file_name=f"{nome}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


def _filtro_periodo(col_data, label="Período"):
    """Retorna (data_ini, data_fim) como strings AAAA-MM-DD."""
    from datetime import date as _date
    opcoes = ["Mês atual", "Mês anterior", "Trimestre atual",
              "Ano atual", "Personalizado"]
    op = st.selectbox(label, opcoes, key=f"periodo_{label}")

    _hoje = _date.today()
    _hoje_str = f"'{_hoje.isoformat()}'"

    if op == "Mês atual":
        _ini = _date(_hoje.year, _hoje.month, 1)
        return (f"'{_ini.isoformat()}'", _hoje_str)
    elif op == "Mês anterior":
        _ini_mes = _date(_hoje.year, _hoje.month, 1)
        from datetime import timedelta as _td
        _fim_ant = _ini_mes - _td(days=1)
        _ini_ant = _date(_fim_ant.year, _fim_ant.month, 1)
        return (f"'{_ini_ant.isoformat()}'", f"'{_fim_ant.isoformat()}'")
    elif op == "Trimestre atual":
        from datetime import timedelta as _td
        _ini = (_hoje - _td(days=90)).replace(day=1)
        return (f"'{_ini.isoformat()}'", _hoje_str)
    elif op == "Ano atual":
        _ini = _date(_hoje.year, 1, 1)
        return (f"'{_ini.isoformat()}'", _hoje_str)
    else:
        col1, col2 = st.columns(2)
        with col1:
            d_ini = st.date_input("De", key=f"di_{label}")
        with col2:
            d_fim = st.date_input("Até", key=f"df_{label}")
        return (f"'{d_ini}'", f"'{d_fim}'")


def _filtro_fornecedor(key="forn_rel"):
    forns = [(None, "Todos")] + list(cache_fornecedores())
    sel = st.selectbox("Fornecedor", forns, format_func=lambda x: x[1], key=key)
    return sel[0] if sel else None


# ═══════════════════════════════════════════════════════
# ENTRADA PRINCIPAL
# ═══════════════════════════════════════════════════════

def tela_relatorios():
    st.header("Relatórios de Vendas")
    if st.button("⬅ Voltar"):
        _ir("home")

    ABAS_REL = {
        "cli":"Por cliente","forn":"Por fornecedor","prod":"Por produto",
        "cat":"Por categoria","evol":"Evolução mensal","comp":"Comparação",
        "sem":"Sem pedido","rank":"Ranking PDVs",
        "cluster":"🎯 Cluster","napres":"🏭 Não apresentados",
        "cobertura":"📡 Cobertura","compet":"⚔️ Competitivo"
    }
    if "rel_aba" not in st.session_state: st.session_state["rel_aba"] = "cli"
    # Linha 1: primeiras 5
    r1 = list(ABAS_REL.items())[:5]; r2 = list(ABAS_REL.items())[5:]
    for row in [r1, r2]:
        cols2 = st.columns(len(row))
        for col,(k,v) in zip(cols2, row):
            ativa = st.session_state["rel_aba"] == k
            if col.button(v, key=f"rnav_{k}", width="stretch",
                          type="primary" if ativa else "secondary"):
                st.session_state["rel_aba"] = k; st.rerun()
    st.divider()
    _ABAS_CALL = {
        "cli":_rel_cliente,"forn":_rel_fornecedor,"prod":_rel_produto,
        "cat":_rel_categoria,"evol":_rel_evolucao,"comp":_rel_comparacao,
        "sem":_rel_sem_pedido,"rank":_rel_ranking_pdv,
        "cluster":_rel_cluster,"napres":_rel_nao_apresentados,
        "cobertura":_rel_cobertura,"compet":_rel_competitivo
    }
    _ABAS_CALL.get(st.session_state["rel_aba"], _rel_cliente)()
    # Dummy para manter compatibilidade de indentação
    aba = [None]*10  # aba não usado mais, key="tabs_relato9751")



# ═══════════════════════════════════════════════════════
# 1. POR CLIENTE
# ═══════════════════════════════════════════════════════

def _rel_cliente():
    st.subheader("Vendas por cliente")
    col1, col2 = st.columns(2)
    with col1:
        d_ini, d_fim = _filtro_periodo("data_pedido", "Período — cliente")
    with col2:
        forn_id = _filtro_fornecedor("forn_cli")

    where_extra = ""
    params = []
    if forn_id:
        where_extra += " AND p.fornecedor_id=?"
        params.append(forn_id)

    dados = query(f"""
        SELECT c.nome_fantasia                           AS cliente,
               f.nome_fantasia                           AS fornecedor,
               COUNT(DISTINCT p.pedido_id)               AS pedidos,
               SUM(pi.quantidade)                        AS caixas,
               ROUND(SUM({_VALOR_ITEM}), 2)              AS total
        {_FILTRO_BASE}
          AND p.data_pedido BETWEEN {d_ini} AND {d_fim}
          {where_extra}
        GROUP BY c.cliente_id, c.nome_fantasia, f.fornecedor_id, f.nome_fantasia
        ORDER BY total DESC
    """, tuple(params))

    if not dados:
        st.info("Nenhum dado encontrado para o período.")
        return

    df = pd.DataFrame(dados, columns=["Cliente","Fornecedor","Pedidos","Caixas","Total (R$)"])

    # Métricas resumo
    col1, col2, col3 = st.columns(3)
    col1.metric("Clientes ativos", df["Cliente"].nunique())
    col2.metric("Total de pedidos", int(df["Pedidos"].sum()))
    col3.metric("Total vendas", _fmt_brl(df["Total (R$)"].sum()))

    df["Total (R$)"] = df["Total (R$)"].apply(_fmt_brl)
    st.dataframe(df, width="stretch", hide_index=True)

    df_exp = pd.DataFrame(dados, columns=["Cliente","Fornecedor","Pedidos","Caixas","Total (R$)"])
    _excel_download(df_exp, "vendas_por_cliente")


# ═══════════════════════════════════════════════════════
# 2. POR FORNECEDOR
# ═══════════════════════════════════════════════════════

def _rel_fornecedor():
    st.subheader("Vendas por fornecedor")
    d_ini, d_fim = _filtro_periodo("data_pedido", "Período — fornecedor")

    dados = query(f"""
        SELECT f.nome_fantasia                           AS fornecedor,
               COUNT(DISTINCT p.pedido_id)               AS pedidos,
               COUNT(DISTINCT p.cliente_id)              AS clientes,
               SUM(pi.quantidade)                        AS caixas,
               ROUND(SUM({_VALOR_ITEM}), 2)              AS total
        {_FILTRO_BASE}
          AND p.data_pedido BETWEEN {d_ini} AND {d_fim}
        GROUP BY f.fornecedor_id
        ORDER BY total DESC
    """)

    if not dados:
        st.info("Nenhum dado encontrado para o período.")
        return

    df = pd.DataFrame(dados, columns=["Fornecedor","Pedidos","Clientes","Caixas","Total (R$)"])

    col1, col2 = st.columns(2)
    col1.metric("Total geral", _fmt_brl(df["Total (R$)"].sum()))
    col2.metric("Total de pedidos", int(df["Pedidos"].sum()))

    # Gráfico de barras simples via dataframe
    df_chart = df[["Fornecedor","Total (R$)"]].copy()
    df_chart = df_chart.rename(columns={"Total (R$)": "Total"})
    st.bar_chart(df_chart.set_index("Fornecedor"))

    df["Total (R$)"] = df["Total (R$)"].apply(_fmt_brl)
    st.dataframe(df, width="stretch", hide_index=True)

    df_exp = pd.DataFrame(dados, columns=["Fornecedor","Pedidos","Clientes","Caixas","Total (R$)"])
    _excel_download(df_exp, "vendas_por_fornecedor")


# ═══════════════════════════════════════════════════════
# 3. POR PRODUTO
# ═══════════════════════════════════════════════════════

def _rel_produto():
    st.subheader("Produtos mais vendidos")
    col1, col2, col3 = st.columns(3)
    with col1:
        d_ini, d_fim = _filtro_periodo("data_pedido", "Período — produto")
    with col2:
        forn_id = _filtro_fornecedor("forn_prod")
    with col3:
        top_n = st.number_input("Exibir top", min_value=5, max_value=100,
                                value=20, step=5, key="top_prod")

    where_extra = ""
    params = []
    if forn_id:
        where_extra += " AND p.fornecedor_id=?"
        params.append(forn_id)

    dados = query(f"""
        SELECT pr.codigo_produto                         AS codigo,
               pr.descricao_curta                        AS produto,
               f.nome_fantasia                           AS fornecedor,
               cat.nome_categoria                        AS categoria,
               SUM(pi.quantidade)                        AS caixas,
               COUNT(DISTINCT p.pedido_id)               AS pedidos,
               COUNT(DISTINCT p.cliente_id)              AS clientes,
               ROUND(SUM({_VALOR_ITEM}), 2)              AS total
        {_FILTRO_BASE}
          AND p.data_pedido BETWEEN {d_ini} AND {d_fim}
          {where_extra}
        GROUP BY pr.produto_id, pr.codigo_produto, pr.descricao_curta, f.nome_fantasia, cat.nome_categoria
        ORDER BY caixas DESC
        LIMIT {int(top_n)}
    """, tuple(params))

    if not dados:
        st.info("Nenhum dado encontrado.")
        return

    df = pd.DataFrame(dados,
                      columns=["Código","Produto","Fornecedor","Categoria",
                               "Caixas","Pedidos","Clientes","Total (R$)"])

    col1, col2 = st.columns(2)
    col1.metric("Produtos diferentes", len(df))
    col2.metric("Total vendas", _fmt_brl(df["Total (R$)"].sum()))

    # Top 10 gráfico
    df_chart = df.head(10)[["Produto","Caixas"]].copy()
    st.bar_chart(df_chart.set_index("Produto"))

    df["Total (R$)"] = df["Total (R$)"].apply(_fmt_brl)
    st.dataframe(df, width="stretch", hide_index=True)

    df_exp = pd.DataFrame(dados,
                          columns=["Código","Produto","Fornecedor","Categoria",
                                   "Caixas","Pedidos","Clientes","Total (R$)"])
    _excel_download(df_exp, "produtos_mais_vendidos")


# ═══════════════════════════════════════════════════════
# 4. POR CATEGORIA
# ═══════════════════════════════════════════════════════

def _rel_categoria():
    st.subheader("Vendas por categoria")
    col1, col2 = st.columns(2)
    with col1:
        d_ini, d_fim = _filtro_periodo("data_pedido", "Período — categoria")
    with col2:
        forn_id = _filtro_fornecedor("forn_cat")

    where_extra = ""
    params = []
    if forn_id:
        where_extra += " AND p.fornecedor_id=?"
        params.append(forn_id)

    dados = query(f"""
        SELECT COALESCE(cat.nome_categoria,'Sem categoria') AS categoria,
               f.nome_fantasia                              AS fornecedor,
               COUNT(DISTINCT pr.produto_id)                AS produtos,
               SUM(pi.quantidade)                           AS caixas,
               ROUND(SUM({_VALOR_ITEM}), 2)                 AS total
        {_FILTRO_BASE}
          AND p.data_pedido BETWEEN {d_ini} AND {d_fim}
          {where_extra}
        GROUP BY cat.categoria_id, cat.nome_categoria, f.fornecedor_id, f.nome_fantasia
        ORDER BY total DESC
    """, tuple(params))

    if not dados:
        st.info("Nenhum dado encontrado.")
        return

    df = pd.DataFrame(dados,
                      columns=["Categoria","Fornecedor","Produtos","Caixas","Total (R$)"])

    total_geral = df["Total (R$)"].sum()
    df["Participação (%)"] = (df["Total (R$)"] / total_geral * 100).round(1)

    col1, col2 = st.columns(2)
    col1.metric("Total geral", _fmt_brl(total_geral))
    col2.metric("Categorias", len(df))

    df_chart = df[["Categoria","Total (R$)"]].copy()
    st.bar_chart(df_chart.set_index("Categoria"))

    df["Total (R$)"] = df["Total (R$)"].apply(_fmt_brl)
    st.dataframe(df, width="stretch", hide_index=True)

    df_exp = pd.DataFrame(dados,
                          columns=["Categoria","Fornecedor","Produtos","Caixas","Total (R$)"])
    df_exp["Participação (%)"] = (df_exp["Total (R$)"] / total_geral * 100).round(1)
    _excel_download(df_exp, "vendas_por_categoria")


# ═══════════════════════════════════════════════════════
# 5. EVOLUÇÃO MENSAL
# ═══════════════════════════════════════════════════════

def _rel_evolucao():
    st.subheader("Evolução mensal de vendas")
    col1, col2 = st.columns(2)
    with col1:
        forn_id = _filtro_fornecedor("forn_evol")
    with col2:
        meses = st.number_input("Últimos N meses", min_value=3,
                                max_value=24, value=12, key="meses_evol")

    where_extra = ""
    params = []
    if forn_id:
        where_extra += " AND p.fornecedor_id=?"
        params.append(forn_id)

    dados = query(f"""
        SELECT strftime('%Y-%m', p.data_pedido)          AS mes,
               f.nome_fantasia                           AS fornecedor,
               COUNT(DISTINCT p.pedido_id)               AS pedidos,
               SUM(pi.quantidade)                        AS caixas,
               ROUND(SUM({_VALOR_ITEM}), 2)              AS total
        {_FILTRO_BASE}
          AND p.data_pedido >= date('now', '-{int(meses)} months')
          {where_extra}
        GROUP BY mes, f.fornecedor_id, f.nome_fantasia
        ORDER BY mes
    """, tuple(params))

    if not dados:
        st.info("Nenhum dado encontrado.")
        return

    df = pd.DataFrame(dados,
                      columns=["Mês","Fornecedor","Pedidos","Caixas","Total (R$)"])

    # Gráfico de linha por fornecedor
    df_pivot = df.pivot_table(
        index="Mês", columns="Fornecedor",
        values="Total (R$)", aggfunc="sum"
    ).fillna(0)

    st.line_chart(df_pivot)

    # Tabela
    col1, col2, col3 = st.columns(3)
    col1.metric("Meses com venda", df["Mês"].nunique())
    col2.metric("Total pedidos", int(df["Pedidos"].sum()))
    col3.metric("Total geral", _fmt_brl(df["Total (R$)"].sum()))

    df_show = df.copy()
    df_show["Total (R$)"] = df_show["Total (R$)"].apply(_fmt_brl)
    st.dataframe(df_show, width="stretch", hide_index=True)

    _excel_download(df, "evolucao_mensal")


# ═══════════════════════════════════════════════════════
# 6. COMPARAÇÃO DE PERÍODOS
# ═══════════════════════════════════════════════════════

def _rel_comparacao():
    st.subheader("Comparação de períodos")
    st.caption("Compare dois períodos lado a lado — por cliente, fornecedor ou produto.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Período A**")
        d_ini_a, d_fim_a = _filtro_periodo("data_pedido", "Período A")
    with col2:
        st.markdown("**Período B**")
        d_ini_b, d_fim_b = _filtro_periodo("data_pedido", "Período B")

    col1, col2 = st.columns(2)
    with col1:
        agrup = st.selectbox("Agrupar por",
                             ["Cliente", "Fornecedor", "Produto", "Categoria"],
                             key="agrup_comp")
    with col2:
        forn_id = _filtro_fornecedor("forn_comp")

    where_extra = ""
    params_a = []
    params_b = []
    if forn_id:
        where_extra += " AND p.fornecedor_id=?"
        params_a.append(forn_id)
        params_b.append(forn_id)

    grupo_map = {
        "Cliente":    ("c.nome_fantasia", "c.cliente_id"),
        "Fornecedor": ("f.nome_fantasia", "f.fornecedor_id"),
        "Produto":    ("pr.descricao_curta", "pr.produto_id"),
        "Categoria":  ("COALESCE(cat.nome_categoria,'Sem categoria')", "cat.categoria_id"),
    }
    grupo_col, grupo_id = grupo_map[agrup]

    def _buscar(d_ini, d_fim, params):
        return query(f"""
            SELECT {grupo_col} AS grupo,
                   ROUND(SUM({_VALOR_ITEM}), 2) AS total,
                   SUM(pi.quantidade) AS caixas,
                   COUNT(DISTINCT p.pedido_id) AS pedidos
            {_FILTRO_BASE}
              AND p.data_pedido BETWEEN {d_ini} AND {d_fim}
              {where_extra}
            GROUP BY {grupo_id}
            ORDER BY total DESC
        """, tuple(params))

    dados_a = _buscar(d_ini_a, d_fim_a, params_a)
    dados_b = _buscar(d_ini_b, d_fim_b, params_b)

    if not dados_a and not dados_b:
        st.info("Nenhum dado encontrado em nenhum dos períodos.")
        return

    df_a = pd.DataFrame(dados_a, columns=[agrup, "Total A", "Caixas A", "Pedidos A"]) \
           if dados_a else pd.DataFrame(columns=[agrup, "Total A", "Caixas A", "Pedidos A"])

    df_b = pd.DataFrame(dados_b, columns=[agrup, "Total B", "Caixas B", "Pedidos B"]) \
           if dados_b else pd.DataFrame(columns=[agrup, "Total B", "Caixas B", "Pedidos B"])

    df = pd.merge(df_a, df_b, on=agrup, how="outer").fillna(0)

    df["Variação (%)"] = df.apply(
        lambda r: round((r["Total B"] - r["Total A"]) / r["Total A"] * 100, 1)
        if r["Total A"] > 0 else None,
        axis=1
    )

    # Métricas de resumo
    tot_a = df["Total A"].sum()
    tot_b = df["Total B"].sum()
    var   = round((tot_b - tot_a) / tot_a * 100, 1) if tot_a > 0 else None

    col1, col2, col3 = st.columns(3)
    col1.metric("Total período A", _fmt_brl(tot_a))
    col2.metric("Total período B", _fmt_brl(tot_b),
                delta=f"{var:+.1f}%" if var is not None else None)
    col3.metric("Variação absoluta",
                _fmt_brl(tot_b - tot_a))

    # Gráfico comparativo
    df_chart = df[[agrup, "Total A", "Total B"]].set_index(agrup)
    st.bar_chart(df_chart)

    # Tabela com variação colorida
    df_show = df.copy()
    df_show["Total A"] = df_show["Total A"].apply(_fmt_brl)
    df_show["Total B"] = df_show["Total B"].apply(_fmt_brl)
    df_show["Variação (%)"] = df_show["Variação (%)"].apply(
        lambda v: f"{v:+.1f}%" if v is not None else "—"
    )
    st.dataframe(df_show, width="stretch", hide_index=True)

    _excel_download(df, "comparacao_periodos")


# ═══════════════════════════════════════════════════════
# 7. CLIENTES SEM PEDIDO NO PERIODO
# ═══════════════════════════════════════════════════════

def _rel_sem_pedido():
    st.subheader("Clientes sem pedido no periodo")
    st.caption("Identifique clientes que nao fizeram pedido no periodo selecionado — oportunidades de visita e reativacao.")

    col1, col2, col3 = st.columns(3)
    with col1:
        d_ini, d_fim = _filtro_periodo("data_pedido", "Periodo — sem pedido")
    with col2:
        forn_id = _filtro_fornecedor("forn_semp")
    with col3:
        TIPOS_PDV_R = ["Todos","Supermercado","Hipermercado","Atacadista","Mini Mercado",
                       "Mercearia","Emporio","Sacolao","Hortifruti","Acougue","Casa de Carnes",
                       "Peixaria","Padaria","Confeitaria","Delicatessen","Hamburgueria",
                       "Restaurante","Lanchonete","Bar / Boteco","Clube / Associacao","Outro"]
        fil_tipo_pdv_sp = st.selectbox("Tipo de PDV", TIPOS_PDV_R, key="fil_tipo_pdv_sp")

    where_forn = "AND p2.fornecedor_id=?" if forn_id else ""
    params = [forn_id] if forn_id else []
    params_sub = [forn_id] if forn_id else []
    where_tipo_pdv = ""
    if fil_tipo_pdv_sp != "Todos":
        where_tipo_pdv = """AND EXISTS (
            SELECT 1 FROM pdv px WHERE px.cliente_id=c.cliente_id
            AND px.tipo_pdv=?)"""
        params.append(fil_tipo_pdv_sp)
        params_sub.append(fil_tipo_pdv_sp)

    dados = query(f"""
        SELECT c.cliente_id, c.nome_fantasia AS cliente,
               c.cidade, c.estado, c.status,
               MAX(p2.data_pedido) AS ultimo_pedido,
               COUNT(DISTINCT p2.pedido_id) AS total_pedidos_historico
        FROM cliente c
        LEFT JOIN pedido p2 ON p2.cliente_id=c.cliente_id
            AND p2.status_pedido NOT IN ('CANCELADO','RECUSADO')
            {where_forn}
        WHERE c.ativo!=0
          {where_tipo_pdv}
          AND NOT EXISTS (
              SELECT 1 FROM pedido p3
              WHERE p3.cliente_id=c.cliente_id
                AND p3.status_pedido NOT IN ('CANCELADO','RECUSADO')
                AND p3.data_pedido BETWEEN {d_ini} AND {d_fim}
                {'AND p3.fornecedor_id=?' if forn_id else ''}
          )
        GROUP BY c.cliente_id
        ORDER BY ultimo_pedido DESC NULLS LAST
    """, tuple(params + params_sub))

    if not dados:
        st.success("Todos os clientes ativos fizeram pedido no periodo selecionado!")
        return

    df = pd.DataFrame(dados,
                      columns=["ID","Cliente","Cidade","UF","Status",
                               "Ultimo pedido","Pedidos (historico)"])
    df["Ultimo pedido"] = df["Ultimo pedido"].fillna("Nunca pediu")

    col1, col2 = st.columns(2)
    col1.metric("Clientes sem pedido no periodo", len(df))
    nunca = (df["Ultimo pedido"] == "Nunca pediu").sum()
    col2.metric("Destes, nunca pediram", int(nunca))

    st.dataframe(df[["Cliente","Cidade","UF","Status","Ultimo pedido","Pedidos (historico)"]],
                 width="stretch", hide_index=True)
    _excel_download(df, "clientes_sem_pedido")


# ═══════════════════════════════════════════════════════
# 8. RANKING DE PDVs
# ═══════════════════════════════════════════════════════

def _rel_ranking_pdv():
    st.subheader("Ranking de PDVs por valor de pedidos")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        d_ini, d_fim = _filtro_periodo("data_pedido", "Periodo — PDV")
    with col2:
        forn_id = _filtro_fornecedor("forn_pdv")
    with col3:
        TIPOS_PDV_RK = ["Todos","Supermercado","Hipermercado","Atacadista","Mini Mercado",
                        "Mercearia","Emporio","Sacolao","Hortifruti","Acougue","Casa de Carnes",
                        "Peixaria","Padaria","Confeitaria","Delicatessen","Hamburgueria",
                        "Restaurante","Lanchonete","Bar / Boteco","Clube / Associacao","Outro"]
        fil_tipo_pdv_rk = st.selectbox("Tipo de PDV", TIPOS_PDV_RK, key="fil_tipo_pdv_rk")
    with col4:
        top_n = st.number_input("Exibir top", min_value=5,
                                max_value=100, value=20, step=5, key="top_pdv")

    where_extra = ""
    params = []
    if forn_id:
        where_extra += " AND p.fornecedor_id=?"
        params.append(forn_id)
    if fil_tipo_pdv_rk != "Todos":
        where_extra += " AND COALESCE(pdv.tipo_pdv,'') =?"
        params.append(fil_tipo_pdv_rk)

    dados = query(f"""
        SELECT c.nome_fantasia AS cliente,
               COALESCE(pdv.nome_loja, 'Matriz/Direto') AS pdv,
               COALESCE(pdv.cidade, c.cidade, '') AS cidade,
               COALESCE(pdv.estado, c.estado, '') AS uf,
               COUNT(DISTINCT p.pedido_id) AS pedidos,
               SUM(pi.quantidade) AS caixas,
               ROUND(SUM({_VALOR_ITEM}), 2) AS total
        FROM pedido_item pi
        JOIN pedido p ON pi.pedido_id=p.pedido_id
        JOIN cliente c ON p.cliente_id=c.cliente_id
        JOIN produto pr ON pi.produto_id=pr.produto_id
        JOIN fornecedor f ON p.fornecedor_id=f.fornecedor_id
        LEFT JOIN categoria cat ON pr.categoria_id=cat.categoria_id
        LEFT JOIN pdv ON p.pdv_id=pdv.pdv_id
        WHERE p.status_pedido != 'CANCELADO'
          AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO')
          AND p.data_pedido BETWEEN {d_ini} AND {d_fim}
          {where_extra}
        GROUP BY p.cliente_id, c.nome_fantasia, c.cidade, c.estado, p.pdv_id, COALESCE(p.pdv_id, 0), pdv.nome_loja, pdv.numero_loja, pdv.cidade, pdv.estado
        ORDER BY total DESC
        LIMIT {int(top_n)}
    """, tuple(params))

    if not dados:
        st.info("Nenhum dado encontrado para o periodo.")
        return

    df = pd.DataFrame(dados,
                      columns=["Cliente","PDV","Cidade","UF","Pedidos","Caixas","Total (R$)"])

    col1, col2 = st.columns(2)
    col1.metric("PDVs no ranking", len(df))
    col2.metric("Total geral", _fmt_brl(df["Total (R$)"].sum()))

    df_chart = df.head(10).copy()
    df_chart["Label"] = df_chart["Cliente"] + " / " + df_chart["PDV"]
    st.bar_chart(df_chart.set_index("Label")[["Total (R$)"]])

    df["Total (R$)"] = df["Total (R$)"].apply(_fmt_brl)
    st.dataframe(df, width="stretch", hide_index=True)

    df_exp = pd.DataFrame(dados,
                          columns=["Cliente","PDV","Cidade","UF","Pedidos","Caixas","Total (R$)"])
    _excel_download(df_exp, "ranking_pdvs")


# ═══════════════════════════════════════════════════════
# 9. RELATÓRIO POR CLUSTER / TAMANHO DE PDV
# ═══════════════════════════════════════════════════════

def _rel_cluster():
    st.subheader("🎯 Segmentação por Cluster e Tamanho de PDV")
    st.caption(
        "Cruza o perfil do PDV (cluster e tamanho) com vendas e cobertura de fornecedores. "
        "Use para priorizar abordagens e identificar oportunidades por segmento."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        forns = query(
            "SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo!=0 ORDER BY nome_fantasia")
        forn_opts = [("todos", "Todos os fornecedores")] + [(f[0], f[1]) for f in forns]
        forn_sel  = st.selectbox("Fornecedor", forn_opts,
                                 format_func=lambda x: x[1], key="rc_forn")
    with col2:
        clusters = ["Todos","A","B","C","D","A/B","B/C","C/D"]
        cl_sel   = st.selectbox("Cluster", clusters, key="rc_cluster")
    with col3:
        tamanhos = ["Todos","GG","G","M","P","PP"]
        tam_sel  = st.selectbox("Tamanho", tamanhos, key="rc_tam")

    st.divider()

    # ── Seção 1: Mapa de cobertura de fornecedor por cluster ──────────────
    st.markdown("#### 📊 Cobertura por cluster — clientes ativos vs abordados")
    st.caption("Mostra quantos PDVs de cada cluster já compraram de cada fornecedor.")

    _forn_id_cob = int(forn_sel[0]) if str(forn_sel[0]).lower() != 'todos' else None
    _forn_where  = "AND p.fornecedor_id = ?" if _forn_id_cob else ""
    _forn_params = (_forn_id_cob,) if _forn_id_cob else ()
    cob = query(f"""
        SELECT
            pdv.cluster,
            pdv.tamanho_pdv,
            COUNT(DISTINCT c.cliente_id)                              AS total_pdvs,
            COUNT(DISTINCT CASE WHEN p.pedido_id IS NOT NULL
                  THEN c.cliente_id END)                              AS pdvs_com_pedido,
            ROUND(COUNT(DISTINCT CASE WHEN p.pedido_id IS NOT NULL
                  THEN c.cliente_id END) * 100.0
                  / NULLIF(COUNT(DISTINCT c.cliente_id),0), 1)        AS cobertura_pct
        FROM cliente c
        JOIN pdv ON pdv.pdv_id = c.cliente_id
        LEFT JOIN pedido p ON p.cliente_id = c.cliente_id
            AND p.status_pedido NOT IN ('CANCELADO','RECUSADO')
            {_forn_where}
        WHERE c.status NOT IN ('Inativo','Encerrado')
          AND (? = 'Todos' OR pdv.cluster = ?)
          AND (? = 'Todos' OR pdv.tamanho_pdv = ?)
        GROUP BY pdv.cluster, pdv.tamanho_pdv
        ORDER BY pdv.cluster, pdv.tamanho_pdv
    """, _forn_params + (cl_sel, cl_sel, tam_sel, tam_sel))

    if cob:
        df_cob = pd.DataFrame(cob, columns=["Cluster","Tamanho","Total PDVs",
                                             "Com pedido","Cobertura %"])
        # Coloração visual da cobertura
        def _cor_cob(val):
            try:
                v = float(val)
                if v >= 80:   return "background-color:#c8e6c9"
                elif v >= 50: return "background-color:#fff9c4"
                else:         return "background-color:#ffcdd2"
            except: return ""

        st.dataframe(
            df_cob.style.map(_cor_cob, subset=["Cobertura %"]),
            width="stretch", hide_index=True
        )
        _excel_download(df_cob, "cobertura_cluster")
    else:
        st.info("Nenhum dado encontrado para os filtros selecionados.")

    st.divider()

    # ── Seção 2: Lista de PDVs por cluster com status de compra ──────────
    st.markdown("#### 📋 PDVs por segmento — detalhe individual")

    _forn_where2 = "AND p.fornecedor_id = ?" if _forn_id_cob else ""
    _forn_params2 = (_forn_id_cob,) if _forn_id_cob else ()
    pdvs = query(f"""
        SELECT
            c.cliente_id,
            c.nome_fantasia,
            c.cidade,
            pdv.cluster,
            pdv.tamanho_pdv,
            pdv.tipo_pdv,
            c.status,
            COUNT(DISTINCT p.pedido_id)                               AS qtd_pedidos,
            ROUND(COALESCE(SUM(pi.quantidade * pi.preco_final
                * (1 - COALESCE(p.desconto_geral,0)/100.0)),0),2)     AS total_comprado,
            MAX(p.data_pedido)                                        AS ultimo_pedido
        FROM cliente c
        JOIN pdv ON pdv.pdv_id = c.cliente_id
        LEFT JOIN pedido p ON p.cliente_id = c.cliente_id
            AND p.status_pedido NOT IN ('CANCELADO','RECUSADO')
            {_forn_where2}
        LEFT JOIN pedido_item pi ON pi.pedido_id = p.pedido_id
            AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO')
        WHERE c.status NOT IN ('Inativo','Encerrado')
          AND (? = 'Todos' OR pdv.cluster = ?)
          AND (? = 'Todos' OR pdv.tamanho_pdv = ?)
        GROUP BY c.cliente_id, c.nome_fantasia, c.cidade,
                 pdv.cluster, pdv.tamanho_pdv, pdv.tipo_pdv, c.status
        ORDER BY pdv.cluster, pdv.tamanho_pdv, total_comprado DESC
    """, _forn_params2 + (cl_sel, cl_sel, tam_sel, tam_sel))

    if not pdvs:
        st.info("Nenhum PDV encontrado.")
        return

    df_pdvs = pd.DataFrame(pdvs, columns=[
        "ID","PDV","Cidade","Cluster","Tamanho","Tipo",
        "Status","Pedidos","Total R$","Último pedido"])

    # Métricas resumidas
    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("Total PDVs",       len(df_pdvs))
    mc2.metric("Com compras",      int((df_pdvs["Pedidos"]>0).sum()))
    mc3.metric("Sem compras",      int((df_pdvs["Pedidos"]==0).sum()))
    mc4.metric("Volume total",     _fmt_brl(df_pdvs["Total R$"].sum()))

    # Formata coluna de valor
    df_display = df_pdvs.copy()
    df_display["Total R$"] = df_display["Total R$"].apply(_fmt_brl)
    df_display["Sem compra"] = df_pdvs["Pedidos"].apply(
        lambda x: "⚠️ Sem pedido" if x == 0 else "")

    st.dataframe(df_display.drop(columns=["ID"]),
                 width="stretch", hide_index=True)

    # Exportação Excel com duas abas
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df_cob_exp = pd.DataFrame(cob, columns=["Cluster","Tamanho","Total PDVs",
                                                  "Com pedido","Cobertura %"]) if cob else pd.DataFrame()
        if not df_cob_exp.empty:
            df_cob_exp.to_excel(writer, index=False, sheet_name="Cobertura por cluster")
        df_pdvs.to_excel(writer, index=False, sheet_name="PDVs detalhe")
    buf.seek(0)
    forn_label = forn_sel[1].replace(" ","_")[:20]
    st.download_button("⬇️ Exportar Excel completo", data=buf,
                       file_name=f"cluster_{forn_label}.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ═══════════════════════════════════════════════════════
# 10. FORNECEDORES NÃO APRESENTADOS
# ═══════════════════════════════════════════════════════

def _rel_nao_apresentados():
    st.subheader("🏭 Clientes sem apresentação por fornecedor")
    st.caption(
        "Clientes da carteira que nunca tiveram contato registrado "
        "sobre determinado fornecedor e nunca compraram dele. "
        "Use para identificar oportunidades e priorizar visitas."
    )

    forns = query(
        "SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo!=0 ORDER BY nome_fantasia")
    if not forns:
        st.info("Nenhum fornecedor cadastrado.")
        return

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        forn_sel = st.selectbox("Fornecedor", forns,
                                format_func=lambda x: x[1], key="rna_forn")
    with col2:
        status_opts = ["Todos","Prospecto","Visitado","Ativo","Inativo","Suspenso"]
        status_sel  = st.selectbox("Status do cliente", status_opts, key="rna_status")
    with col3:
        # Tipo de PDV — busca perfil do cliente (campo perfil) e tipo_pdv
        perfis = query("""SELECT DISTINCT perfil FROM cliente
                          WHERE perfil IS NOT NULL ORDER BY perfil""")
        perf_opts = ["Todos"] + [p[0] for p in perfis if p[0]]
        perf_sel  = st.selectbox("Tipo / Perfil", perf_opts, key="rna_perfil")
    with col4:
        cidades = query("""SELECT DISTINCT cidade FROM cliente
                           WHERE cidade IS NOT NULL ORDER BY cidade""")
        cid_opts = ["Todas"] + [c[0] for c in cidades if c[0]]
        cid_sel  = st.selectbox("Cidade", cid_opts, key="rna_cidade")

    # WHERE — usa status (campo correto) em vez de ativo
    where        = []
    where_params = []
    if status_sel != "Todos":
        where.append("c.status=?");  where_params.append(status_sel)
    if perf_sel != "Todos":
        where.append("c.perfil=?");  where_params.append(perf_sel)
    if cid_sel != "Todas":
        where.append("c.cidade=?");  where_params.append(cid_sel)

    where_sql = ("WHERE " + " AND ".join(where)) if where else ""

    fid = forn_sel[0]
    params_nao = tuple(where_params) + (fid, fid)

    nao_apres = query(f"""
        SELECT c.cliente_id, c.nome_fantasia, c.cidade,
               COALESCE(c.status,'—'),
               COALESCE(c.perfil,'—'),
               (SELECT COUNT(*) FROM pedido p
                WHERE p.cliente_id=c.cliente_id
                  AND p.status_pedido NOT IN ('CANCELADO','RECUSADO')) AS qtd_pedidos,
               MAX(v.data_visita) AS ultima_visita
        FROM cliente c
        LEFT JOIN visita_cliente v ON v.cliente_id = c.cliente_id
        {where_sql}
          {'AND' if where else 'WHERE'}
          c.cliente_id NOT IN (
              SELECT DISTINCT cr.cliente_id
              FROM contato_registro cr
              JOIN contato_x_fornecedor cxf ON cxf.contato_id = cr.contato_id
              WHERE cxf.fornecedor_id = ?
                AND cr.cliente_id IS NOT NULL
                AND cr.ativo = 1
          )
          AND c.cliente_id NOT IN (
              SELECT DISTINCT p.cliente_id
              FROM pedido p
              WHERE p.fornecedor_id = ?
                AND p.status_pedido NOT IN ('CANCELADO','RECUSADO')
          )
        GROUP BY c.cliente_id
        ORDER BY c.status, c.nome_fantasia
    """, params_nao)

    # Total com os mesmos filtros (sem restrição de apresentação)
    total = query(
        f"SELECT COUNT(*) FROM cliente c {where_sql}",
        tuple(where_params)
    )[0][0]

    nao_apres_count = len(nao_apres)
    apres_count     = total - nao_apres_count

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total na seleção",  total)
    c2.metric("Já apresentados",   apres_count)
    c3.metric("Não apresentados",  nao_apres_count)
    c4.metric("Cobertura",
              f"{apres_count/total*100:.0f}%" if total else "—")

    if not nao_apres:
        st.success(f"✅ Todos os clientes selecionados já foram apresentados à **{forn_sel[1]}**!")
        return

    if total > 0:
        st.progress(apres_count / total)
    st.divider()

    st.markdown(f"**{nao_apres_count} cliente(s) sem apresentação de {forn_sel[1]}:**")

    hcols = st.columns([3, 1.2, 1.2, 1.2, 1, 1.5])
    for col, txt in zip(hcols, ["Cliente","Cidade","Status","Tipo/Perfil","Pedidos","Última visita"]):
        col.markdown(f"<small><b>{txt}</b></small>", unsafe_allow_html=True)
    st.divider()

    STATUS_ICONE = {"Prospecto":"🔵","Visitado":"🟣","Ativo":"🟢",
                    "Inativo":"⚫","Suspenso":"🟡","Encerrado":"🔴"}

    for row in nao_apres:
        (cid_id, nome, cidade, status, perfil, qtd_ped, ult_vis) = row
        c = st.columns([3, 1.2, 1.2, 1.2, 1, 1.5])
        c[0].write(nome)
        c[1].caption(cidade or "—")
        c[2].caption(f"{STATUS_ICONE.get(status,'•')} {status}")
        c[3].caption(perfil)
        c[4].caption(str(qtd_ped) if qtd_ped else "—")
        c[5].caption(ult_vis or "Nunca")

    st.divider()
    df_exp = pd.DataFrame(nao_apres, columns=[
        "ID","Cliente","Cidade","Status","Tipo/Perfil","Pedidos","Ultima visita"])
    buf = io.BytesIO()
    df_exp.to_excel(buf, index=False, sheet_name=f"Nao apres {forn_sel[1][:18]}")
    buf.seek(0)
    st.download_button(
        f"⬇️ Exportar lista — {forn_sel[1]}",
        data=buf,
        file_name=f"nao_apres_{forn_sel[1].replace(' ','_')[:18]}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# ═══════════════════════════════════════════════════════
# 11. COBERTURA POR FORNECEDOR
# ═══════════════════════════════════════════════════════

def _rel_cobertura():
    st.subheader("📡 Cobertura por fornecedor")
    st.caption(
        "Mostra quantos clientes da carteira já foram abordados, quantos compraram "
        "e quantos estão em negociação — por fornecedor. "
        "Use para planejar prospecção e identificar onde há espaço para crescer."
    )

    forns = query(
        "SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo!=0 ORDER BY nome_fantasia")
    if not forns:
        st.info("Nenhum fornecedor cadastrado.")
        return

    # ── Filtros ───────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        forn_sel = st.selectbox("Fornecedor", forns,
                                format_func=lambda x: x[1], key="cob_forn")
    with col2:
        perfis_cob = ["Todos"] + [r[0] for r in query(
            "SELECT DISTINCT perfil FROM cliente WHERE perfil IS NOT NULL ORDER BY perfil"
        ) if r[0]]
        tipo_sel = st.selectbox("Tipo / Perfil", perfis_cob, key="cob_tipo")
    with col3:
        cidades = ["Todas"] + [r[0] for r in query(
            "SELECT DISTINCT cidade FROM cliente WHERE cidade IS NOT NULL ORDER BY cidade"
        ) if r[0]]
        cid_sel = st.selectbox("Cidade", cidades, key="cob_cid")
    with col4:
        status_cli = ["Todos","Prospecto","Visitado","Ativo","Inativo"]
        st_sel = st.selectbox("Status cliente", status_cli, key="cob_st")

    fid = forn_sel[0]

    # ── WHERE dinâmico — usa status (campo correto) sem c.ativo!=0 ──────────
    # Filtra por perfil do cliente (campo do cadastro) + cidade + status
    # LEFT JOIN pdv mantido para quem já tem PDV, mas não exclui quem não tem
    where = []
    params_base = []
    if tipo_sel != "Todos":
        # Filtra por perfil do cliente (Hamburgueria, Padaria, etc.)
        where.append("c.perfil = ?"); params_base.append(tipo_sel)
    if cid_sel != "Todas":
        where.append("c.cidade = ?"); params_base.append(cid_sel)
    if st_sel != "Todos":
        where.append("c.status = ?"); params_base.append(st_sel)
    where_sql = " AND ".join(where) if where else "1=1"

    # ── Dados de cobertura ────────────────────────────────────────────────
    total_cli = query(f"""
        SELECT COUNT(DISTINCT c.cliente_id)
        FROM cliente c
        LEFT JOIN pdv ON pdv.pdv_id = c.cliente_id
        WHERE {where_sql}
    """, tuple(params_base))[0][0]

    abordados = query(f"""
        SELECT COUNT(DISTINCT c.cliente_id)
        FROM cliente c
        LEFT JOIN pdv ON pdv.pdv_id = c.cliente_id
        WHERE {where_sql}
          AND c.cliente_id IN (
              SELECT DISTINCT cr.cliente_id
              FROM contato_registro cr
              JOIN contato_x_fornecedor cxf ON cxf.contato_id = cr.contato_id
              WHERE cxf.fornecedor_id = ? AND cr.cliente_id IS NOT NULL AND cr.ativo = 1
          )
    """, tuple(params_base) + (fid,))[0][0]

    compraram = query(f"""
        SELECT COUNT(DISTINCT c.cliente_id)
        FROM cliente c
        LEFT JOIN pdv ON pdv.pdv_id = c.cliente_id
        WHERE {where_sql}
          AND c.cliente_id IN (
              SELECT DISTINCT p.cliente_id FROM pedido p
              WHERE p.fornecedor_id = ?
                AND p.status_pedido NOT IN ('CANCELADO','RECUSADO')
          )
    """, tuple(params_base) + (fid,))[0][0]

    em_negoc = query(f"""
        SELECT COUNT(DISTINCT c.cliente_id)
        FROM cliente c
        LEFT JOIN pdv ON pdv.pdv_id = c.cliente_id
        WHERE {where_sql}
          AND c.cliente_id IN (
              SELECT DISTINCT cr.cliente_id
              FROM contato_registro cr
              JOIN contato_x_fornecedor cxf ON cxf.contato_id = cr.contato_id
              WHERE cxf.fornecedor_id = ? AND cr.cliente_id IS NOT NULL
                AND cr.ativo = 1
                AND cr.tipo_topico = 'Negociação'
                AND cr.status NOT IN ('Concluído','Cancelado')
          )
    """, tuple(params_base) + (fid,))[0][0]

    nao_abordados = total_cli - abordados

    # ── KPIs de cobertura ─────────────────────────────────────────────────
    st.markdown(f"#### {forn_sel[1]}")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total na carteira",    total_cli)
    c2.metric("Já abordados",         abordados,
              help="Clientes com pelo menos 1 contato vinculado a este fornecedor")
    c3.metric("Compraram",            compraram,
              help="Clientes com ao menos 1 pedido confirmado")
    c4.metric("Em negociação",        em_negoc,
              help="Com tópico tipo Negociação em aberto para este fornecedor")
    c5.metric("Não abordados",        nao_abordados,
              delta=f"-{nao_abordados}" if nao_abordados else None,
              delta_color="inverse",
              help="Clientes ativos que ainda não foram contatados sobre este fornecedor")

    # Barras de progresso
    if total_cli > 0:
        pct_ab  = abordados  / total_cli
        pct_cmp = compraram  / total_cli
        st.progress(pct_ab,
                    text=f"Cobertura de abordagem: {abordados}/{total_cli} ({pct_ab*100:.0f}%)")
        st.progress(pct_cmp,
                    text=f"Conversão em compra:    {compraram}/{total_cli} ({pct_cmp*100:.0f}%)")

    st.divider()

    # ── Funil de conversão visual ─────────────────────────────────────────
    if total_cli > 0:
        st.markdown("**Funil comercial**")
        etapas = [
            ("🏪 Total na carteira",  total_cli,  "#4a90d9"),
            ("📞 Abordados",          abordados,  "#2d6a4f"),
            ("🤝 Em negociação",      em_negoc,   "#f4a261"),
            ("✅ Compraram",          compraram,  "#2a9d8f"),
        ]
        for label, valor, cor in etapas:
            pct = valor / total_cli if total_cli else 0
            barra = "█" * int(pct * 30)
            espaco = "░" * (30 - len(barra))
            st.markdown(
                f'<div style="font-size:12px;margin:2px 0">'
                f'<span style="display:inline-block;width:180px">{label}</span>'
                f'<span style="color:{cor};font-family:monospace">{barra}{espaco}</span>'
                f'  <b>{valor}</b> <span style="color:#888">({pct*100:.0f}%)</span>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.divider()

    # ── Lista detalhada por segmento ──────────────────────────────────────
    SEGMENTOS = {
        "🔵 Não abordados — oportunidade imediata": f"""
            SELECT c.cliente_id, c.nome_fantasia, c.cidade, c.status,
                   COALESCE(pdv.tipo_pdv,'—'), COALESCE(pdv.cluster,'—'),
                   NULL as ultimo_contato, NULL as ultima_compra
            FROM cliente c LEFT JOIN pdv ON pdv.pdv_id=c.cliente_id
            WHERE {where_sql}
              AND c.cliente_id NOT IN (
                  SELECT DISTINCT cr.cliente_id FROM contato_registro cr
                  JOIN contato_x_fornecedor cxf ON cxf.contato_id=cr.contato_id
                  WHERE cxf.fornecedor_id=? AND cr.cliente_id IS NOT NULL AND cr.ativo!=0)
              AND c.cliente_id NOT IN (
                  SELECT DISTINCT p.cliente_id FROM pedido p
                  WHERE p.fornecedor_id=? AND p.status_pedido NOT IN ('CANCELADO','RECUSADO'))
            ORDER BY c.status, c.nome_fantasia""",

        "🤝 Em negociação — acompanhar": f"""
            SELECT c.cliente_id, c.nome_fantasia, c.cidade, c.status,
                   COALESCE(pdv.tipo_pdv,'—'), COALESCE(pdv.cluster,'—'),
                   MAX(cr.data_contato), NULL
            FROM cliente c LEFT JOIN pdv ON pdv.pdv_id=c.cliente_id
            JOIN contato_registro cr ON cr.cliente_id=c.cliente_id
            JOIN contato_x_fornecedor cxf ON cxf.contato_id=cr.contato_id
            WHERE {where_sql}
              AND cxf.fornecedor_id=? AND cr.ativo!=0
              AND cr.tipo_topico='Negociação'
              AND cr.status NOT IN ('Concluído','Cancelado')
            GROUP BY c.cliente_id, c.nome_fantasia, c.cidade, c.status, pdv.tipo_pdv, pdv.cluster
            ORDER BY MAX(cr.data_contato) DESC""",

        "✅ Clientes ativos (já compraram)": f"""
            SELECT c.cliente_id, c.nome_fantasia, c.cidade, c.status,
                   COALESCE(pdv.tipo_pdv,'—'), COALESCE(pdv.cluster,'—'),
                   MAX(cr.data_contato), MAX(p.data_pedido)
            FROM cliente c LEFT JOIN pdv ON pdv.pdv_id=c.cliente_id
            LEFT JOIN contato_registro cr ON cr.cliente_id=c.cliente_id
            JOIN pedido p ON p.cliente_id=c.cliente_id
            WHERE {where_sql}
              AND p.fornecedor_id=? AND p.status_pedido NOT IN ('CANCELADO','RECUSADO')
              AND (cxf.fornecedor_id IS NULL OR cxf.fornecedor_id=?)
            LEFT JOIN contato_x_fornecedor cxf ON cxf.contato_id=cr.contato_id
            GROUP BY c.cliente_id, c.nome_fantasia, c.cidade, c.status, pdv.tipo_pdv, pdv.cluster
            ORDER BY MAX(p.data_pedido) DESC""",
    }

    # Queries simplificadas e corretas
    seg_queries = {
        "🔵 Não abordados — oportunidade imediata": (
            f"""SELECT c.cliente_id, c.nome_fantasia, c.cidade, c.status,
                COALESCE(c.perfil,'—') AS tipo, COALESCE(pdv.cluster,'—') AS cluster,
                NULL AS ultimo_ct, NULL AS ultima_cpra
            FROM cliente c LEFT JOIN pdv ON pdv.pdv_id=c.cliente_id
            WHERE {where_sql}
              AND c.cliente_id NOT IN (
                  SELECT DISTINCT cr.cliente_id FROM contato_registro cr
                  JOIN contato_x_fornecedor cxf ON cxf.contato_id=cr.contato_id
                  WHERE cxf.fornecedor_id=? AND cr.cliente_id IS NOT NULL AND cr.ativo!=0)
              AND c.cliente_id NOT IN (
                  SELECT DISTINCT p.cliente_id FROM pedido p
                  WHERE p.fornecedor_id=? AND p.status_pedido NOT IN ('CANCELADO','RECUSADO'))
            ORDER BY c.status, c.nome_fantasia""",
            tuple(params_base) + (fid, fid)
        ),
        "🤝 Em negociação — acompanhar": (
            f"""SELECT c.cliente_id, c.nome_fantasia, c.cidade, c.status,
                COALESCE(c.perfil,'—'), COALESCE(pdv.cluster,'—'),
                MAX(cr.data_contato), NULL
            FROM cliente c LEFT JOIN pdv ON pdv.pdv_id=c.cliente_id
            JOIN contato_registro cr ON cr.cliente_id=c.cliente_id
            JOIN contato_x_fornecedor cxf ON cxf.contato_id=cr.contato_id
            WHERE {where_sql}
              AND cxf.fornecedor_id=? AND cr.ativo!=0
              AND cr.tipo_topico='Negociação'
              AND cr.status NOT IN ('Concluído','Cancelado')
            GROUP BY c.cliente_id, c.nome_fantasia, c.cidade, c.status, c.perfil, pdv.cluster ORDER BY MAX(cr.data_contato) DESC""",
            tuple(params_base) + (fid,)
        ),
        "✅ Compraram — manter ativo": (
            f"""SELECT c.cliente_id, c.nome_fantasia, c.cidade, c.status,
                COALESCE(c.perfil,'—'), COALESCE(pdv.cluster,'—'),
                NULL, MAX(p.data_pedido)
            FROM cliente c LEFT JOIN pdv ON pdv.pdv_id=c.cliente_id
            JOIN pedido p ON p.cliente_id=c.cliente_id
            WHERE {where_sql}
              AND p.fornecedor_id=? AND p.status_pedido NOT IN ('CANCELADO','RECUSADO')
            GROUP BY c.cliente_id, c.nome_fantasia, c.cidade, c.status, c.perfil, pdv.cluster ORDER BY MAX(p.data_pedido) DESC""",
            tuple(params_base) + (fid,)
        ),
    }

    for titulo, (sql, params_seg) in seg_queries.items():
        dados = query(sql, params_seg)
        if not dados:
            continue

        with st.expander(f"{titulo}  ({len(dados)})", expanded=titulo.startswith("🔵")):
            # Cabeçalho
            hc = st.columns([3, 1.5, 1.2, 1, 1, 1.5, 1])
            for col, txt in zip(hc, ["Cliente","Cidade","Status","Tipo PDV","Cluster",
                                      "Últ. contato / pedido","Ação"]):
                col.markdown(f"<small><b>{txt}</b></small>", unsafe_allow_html=True)
            st.divider()

            for row in dados:
                (cid_r, nome, cidade, status_r, tipo_pdv,
                 cluster, extra1, extra2) = row
                data_exib = extra2 or extra1 or "—"
                col1,col2,col3,col4,col5,col6,col7 = st.columns([3,1.5,1.2,1,1,1.5,1])
                col1.write(nome)
                col2.caption(cidade or "—")
                col3.caption(status_r or "—")
                col4.caption(tipo_pdv)
                col5.caption(cluster)
                col6.caption(data_exib)
                if col7.button("📞", key=f"cob_ir_{cid_r}_{titulo[:3]}",
                               width="stretch",
                               help="Registrar contato"):
                    st.session_state["ct_aba"] = "novo"
                    st.session_state["nn_cli_id_pre"] = cid_r
                    from crm_app import ir as _ir_fn
                    _ir_fn("contatos")

            # Exportação Excel
            df_exp = pd.DataFrame(dados, columns=[
                "ID","Cliente","Cidade","Status","Tipo PDV",
                "Cluster","Extra1","Extra2"])
            buf = io.BytesIO()
            df_exp.to_excel(buf, index=False,
                            sheet_name=titulo[:30].replace("—","").strip())
            buf.seek(0)
            st.download_button(
                f"⬇️ Exportar {titulo[:30]}",
                data=buf,
                file_name=f"cobertura_{forn_sel[1][:15]}_{titulo[:10]}.xlsx".replace(" ","_"),
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=f"exp_cob_{titulo[:6]}"
            )


# ═══════════════════════════════════════════════════════════════════
# 12. ANÁLISE COMPETITIVA POR PRODUTO
# ═══════════════════════════════════════════════════════════════════

def _rel_competitivo():
    st.subheader("⚔️ Análise competitiva por produto")
    st.caption(
        "Selecione um produto e veja todos os concorrentes diretos e indiretos "
        "com os últimos preços pesquisados, diferença em R$ e %, share de frentes "
        "e histórico de variação. Use como argumento em negociações e visitas."
    )

    # ── Filtros ──────────────────────────────────────────────────────────
    forns = cache_fornecedores()
    if not forns:
        st.info("Nenhum fornecedor cadastrado."); return

    col1, col2, col3 = st.columns(3)
    with col1:
        forn_sel = st.selectbox("Fornecedor", forns,
                                format_func=lambda x: x[1], key="rc_forn")
    with col2:
        cats = query("""SELECT DISTINCT cat.categoria_id, cat.nome_categoria
            FROM produto p JOIN categoria cat ON p.categoria_id=cat.categoria_id
            WHERE p.fornecedor_id=? AND p.ativo!=0
            ORDER BY cat.nome_categoria""", (forn_sel[0],))
        cat_opts = [(None,"Todas as categorias")] + list(cats)
        cat_sel  = st.selectbox("Categoria", cat_opts,
                                format_func=lambda x: x[1], key="rc_cat")
    with col3:
        # Período das pesquisas
        periodo_opts = [
            ("30",  "Últimos 30 dias"),
            ("60",  "Últimos 60 dias"),
            ("90",  "Últimos 90 dias"),
            ("180", "Últimos 6 meses"),
            ("999", "Todo o histórico"),
        ]
        per_sel = st.selectbox("Período", periodo_opts,
                               format_func=lambda x: x[1], key="rc_per")

    # Lista de produtos com concorrentes cadastrados
    where_p = ["p.fornecedor_id=?", "p.ativo!=0"]
    params_p = [forn_sel[0]]
    if cat_sel[0]:
        where_p.append("p.categoria_id=?"); params_p.append(cat_sel[0])

    prods = query(f"""
        SELECT p.produto_id, p.descricao_curta, p.codigo_produto,
               p.peso, p.unidade_medida,
               COALESCE(cat.nome_categoria,'—')
        FROM produto p
        LEFT JOIN categoria cat ON p.categoria_id=cat.categoria_id
        JOIN produto_concorrente_relacao pcr ON pcr.produto_id=p.produto_id
        WHERE {' AND '.join(where_p)}
        GROUP BY p.produto_id, p.descricao_curta, p.codigo_produto, p.peso, p.unidade_medida, cat.nome_categoria
        ORDER BY cat.nome_categoria, p.descricao_curta
    """, tuple(params_p))

    if not prods:
        st.info(
            "Nenhum produto com concorrentes vinculados encontrado. "
            "Cadastre os vínculos em Concorrentes → Produtos e relações."
        )
        return

    with col1:
        prod_sel = st.selectbox(
            "Produto",
            prods,
            format_func=lambda x: f"{x[1]} ({x[2]})",
            key="rc_prod"
        )

    pid       = prod_sel[0]
    prod_nome = prod_sel[1] or prod_sel[2]
    prod_peso = prod_sel[3]
    prod_um   = prod_sel[4]
    dias      = int(per_sel[0])

    # ── Busca preço nosso mais recente ────────────────────────────────────
    nosso_preco = query(f"""
        SELECT ppi.preco, pp.data_pesquisa, pp.pesquisa_id,
               pdv.nome_loja, cli.nome_fantasia
        FROM pesquisa_preco_item ppi
        JOIN pesquisa_preco pp ON ppi.pesquisa_id=pp.pesquisa_id
        LEFT JOIN pdv pdv       ON pp.pdv_id=pdv.pdv_id
        LEFT JOIN cliente cli   ON pp.cliente_id=cli.cliente_id
        WHERE ppi.produto_id=?
          AND ppi.produto_concorrente_id IS NULL
          AND pp.fornecedor_id=?
          AND pp.status='finalizado'
          AND pp.data_pesquisa >= date('now','-{dias} days')
          AND ppi.preco IS NOT NULL
        ORDER BY pp.data_pesquisa DESC
        LIMIT 1
    """, (pid, forn_sel[0]))

    preco_ref = nosso_preco[0][0] if nosso_preco else None
    data_ref  = nosso_preco[0][1][:10] if nosso_preco else None
    pdv_ref   = (nosso_preco[0][3] or nosso_preco[0][4]) if nosso_preco else None

    # ── Busca concorrentes com último preço pesquisado ────────────────────
    concorrentes = query(f"""
        SELECT
            pc.produto_concorrente_id,
            conc.marca_concorrente,
            pc.descricao_curta,
            pc.peso,
            pc.unidade_medida,
            COALESCE(pc.auditavel,1) AS auditavel,
            pcr.tipo_relacao,
            -- Último preço
            (SELECT ppi2.preco FROM pesquisa_preco_item ppi2
             JOIN pesquisa_preco pp2 ON ppi2.pesquisa_id=pp2.pesquisa_id
             WHERE ppi2.produto_concorrente_id=pc.produto_concorrente_id
               AND pp2.status='finalizado'
               AND pp2.data_pesquisa >= date('now','-{dias} days')
               AND ppi2.preco IS NOT NULL
             ORDER BY pp2.data_pesquisa DESC LIMIT 1) AS ultimo_preco,
            -- Data do último preço
            (SELECT pp2.data_pesquisa FROM pesquisa_preco_item ppi2
             JOIN pesquisa_preco pp2 ON ppi2.pesquisa_id=pp2.pesquisa_id
             WHERE ppi2.produto_concorrente_id=pc.produto_concorrente_id
               AND pp2.status='finalizado'
               AND pp2.data_pesquisa >= date('now','-{dias} days')
               AND ppi2.preco IS NOT NULL
             ORDER BY pp2.data_pesquisa DESC LIMIT 1) AS data_ultimo,
            -- PDV do último preço
            (SELECT COALESCE(pdv2.nome_loja, cli2.nome_fantasia,'—')
             FROM pesquisa_preco_item ppi2
             JOIN pesquisa_preco pp2 ON ppi2.pesquisa_id=pp2.pesquisa_id
             LEFT JOIN pdv pdv2    ON pp2.pdv_id=pdv2.pdv_id
             LEFT JOIN cliente cli2 ON pp2.cliente_id=cli2.cliente_id
             WHERE ppi2.produto_concorrente_id=pc.produto_concorrente_id
               AND pp2.status='finalizado'
               AND pp2.data_pesquisa >= date('now','-{dias} days')
               AND ppi2.preco IS NOT NULL
             ORDER BY pp2.data_pesquisa DESC LIMIT 1) AS pdv_ultimo,
            -- Média de frentes
            (SELECT ROUND(AVG(ppi2.frentes),1) FROM pesquisa_preco_item ppi2
             JOIN pesquisa_preco pp2 ON ppi2.pesquisa_id=pp2.pesquisa_id
             WHERE ppi2.produto_concorrente_id=pc.produto_concorrente_id
               AND pp2.status='finalizado'
               AND pp2.data_pesquisa >= date('now','-{dias} days')) AS media_frentes,
            -- Em oferta na última pesquisa
            (SELECT ppi2.em_oferta FROM pesquisa_preco_item ppi2
             JOIN pesquisa_preco pp2 ON ppi2.pesquisa_id=pp2.pesquisa_id
             WHERE ppi2.produto_concorrente_id=pc.produto_concorrente_id
               AND pp2.status='finalizado'
               AND pp2.data_pesquisa >= date('now','-{dias} days')
             ORDER BY pp2.data_pesquisa DESC LIMIT 1) AS em_oferta,
            -- Qtd pesquisas no período
            (SELECT COUNT(*) FROM pesquisa_preco_item ppi2
             JOIN pesquisa_preco pp2 ON ppi2.pesquisa_id=pp2.pesquisa_id
             WHERE ppi2.produto_concorrente_id=pc.produto_concorrente_id
               AND pp2.status='finalizado'
               AND pp2.data_pesquisa >= date('now','-{dias} days')) AS n_pesquisas
        FROM produto_concorrente_relacao pcr
        JOIN produto_concorrente pc ON pcr.produto_concorrente_id=pc.produto_concorrente_id
        JOIN concorrente conc       ON pc.concorrente_id=conc.concorrente_id
        WHERE pcr.produto_id=? AND pc.ativo!=0
        ORDER BY pcr.tipo_relacao ASC,
                 CASE WHEN (SELECT ppi2.preco FROM pesquisa_preco_item ppi2
                            JOIN pesquisa_preco pp2 ON ppi2.pesquisa_id=pp2.pesquisa_id
                            WHERE ppi2.produto_concorrente_id=pc.produto_concorrente_id
                              AND pp2.status='finalizado' AND ppi2.preco IS NOT NULL
                            ORDER BY pp2.data_pesquisa DESC LIMIT 1) IS NULL THEN 1 ELSE 0 END,
                 (SELECT ppi2.preco FROM pesquisa_preco_item ppi2
                  JOIN pesquisa_preco pp2 ON ppi2.pesquisa_id=pp2.pesquisa_id
                  WHERE ppi2.produto_concorrente_id=pc.produto_concorrente_id
                    AND pp2.status='finalizado' AND ppi2.preco IS NOT NULL
                  ORDER BY pp2.data_pesquisa DESC LIMIT 1) ASC
    """, (pid,))

    if not concorrentes:
        st.info(f"Nenhum concorrente vinculado a **{prod_nome}**.")
        return

    st.divider()

    # ── Cabeçalho do produto ──────────────────────────────────────────────
    peso_fmt = ""
    if prod_peso:
        peso_fmt = (f"{int(prod_peso)}{prod_um}"
                    if float(prod_peso) == int(float(prod_peso))
                    else f"{prod_peso}{prod_um}")

    col_h1, col_h2, col_h3, col_h4 = st.columns(4)
    col_h1.markdown(f"**{prod_nome}** {peso_fmt}")
    if preco_ref:
        col_h2.metric(
            "Nosso preço",
            f"R$ {preco_ref:,.2f}".replace(",","X").replace(".",",").replace("X","."),
            help=f"Pesquisado em {data_ref} — {pdv_ref or '—'}"
        )
        col_h3.caption(f"📅 {data_ref}")
        col_h3.caption(f"📍 {pdv_ref or '—'}")
    else:
        col_h2.warning("Sem preço nosso no período")
    col_h4.metric("Concorrentes", len(concorrentes))

    st.divider()

    # ── Tabela de concorrentes ────────────────────────────────────────────
    def brl(v):
        try: return f"R$ {float(v):,.2f}".replace(",","X").replace(".",",").replace("X",".")
        except: return "—"

    def diff_pct(nosso, conc):
        if not nosso or not conc: return None
        return (conc - nosso) / nosso * 100

    # Separa diretos e indiretos
    diretos   = [c for c in concorrentes if c[6] == "direto"]
    indiretos = [c for c in concorrentes if c[6] != "direto"]

    for grupo_label, grupo in [
        ("🔴 Concorrentes diretos", diretos),
        ("🟡 Concorrentes indiretos", indiretos)
    ]:
        if not grupo: continue
        st.markdown(f"#### {grupo_label}")

        # Cabeçalho da tabela
        hc = st.columns([2, 2.5, 1, 1.5, 1.5, 1, 1, 1])
        for col, txt in zip(hc, ["Marca","Produto","Peso","Último preço",
                                  "vs Nosso","Frentes","Oferta","Pesquisas"]):
            col.markdown(f"<small><b>{txt}</b></small>", unsafe_allow_html=True)
        st.divider()

        for row in grupo:
            (pc_id, marca, desc_c, peso_c, um_c, auditavel,
             tipo_rel, ultimo_preco, data_ult, pdv_ult,
             media_frt, em_oferta, n_pesq) = row

            # Peso do concorrente formatado
            peso_c_fmt = ""
            if peso_c:
                peso_c_fmt = (f"{int(peso_c)}{um_c}"
                              if float(peso_c) == int(float(peso_c))
                              else f"{peso_c}{um_c}")

            # Diferença de preço
            diff = diff_pct(preco_ref, ultimo_preco) if ultimo_preco else None

            if diff is not None:
                if diff > 0:
                    diff_str = f"🔴 +{diff:.1f}%"   # conc mais caro — bom para nós
                    diff_help = "Concorrente mais caro — argumento de preço a favor"
                elif diff < 0:
                    diff_str = f"🟢 {diff:.1f}%"    # conc mais barato — atenção
                    diff_help = "Concorrente mais barato — monitorar de perto"
                else:
                    diff_str = "⚪ igual"
                    diff_help = "Mesmo preço"
            else:
                diff_str = "—"
                diff_help = "Sem preço nosso para comparar"

            c = st.columns([2, 2.5, 1, 1.5, 1.5, 1, 1, 1])
            c[0].write(marca)
            c[1].write(desc_c or "—")
            c[1].caption(f"📅 {(data_ult or '')[:10]}  📍 {pdv_ult or '—'}")
            c[2].caption(peso_c_fmt or "—")
            c[3].write(brl(ultimo_preco) if ultimo_preco else "🚫 Sem dados")
            c[4].caption(diff_str if diff is not None else "—",
                         help=diff_help if diff is not None else "")
            c[5].caption(f"{media_frt:.0f}" if media_frt else "—")
            c[6].caption("🏷️ Sim" if em_oferta else ("Não" if em_oferta is not None else "—"))
            c[7].caption(str(n_pesq) if n_pesq else "0")

        st.divider()

    # ── Histórico de preços do produto nosso vs concorrente direto ────────
    st.markdown("#### 📈 Histórico de preços — comparativo")

    # Pega o concorrente direto com mais pesquisas para o gráfico
    direto_mais_pesquisas = max(
        diretos, key=lambda x: x[12] or 0) if diretos else None

    if direto_mais_pesquisas and preco_ref:
        pc_id_graf = direto_mais_pesquisas[0]
        marca_graf = direto_mais_pesquisas[1]
        desc_graf  = direto_mais_pesquisas[2]

        hist_conc = query(f"""
            SELECT pp.data_pesquisa, AVG(ppi.preco)
            FROM pesquisa_preco_item ppi
            JOIN pesquisa_preco pp ON ppi.pesquisa_id=pp.pesquisa_id
            WHERE ppi.produto_concorrente_id=?
              AND pp.status='finalizado'
              AND ppi.preco IS NOT NULL
              AND pp.data_pesquisa >= date('now','-{dias} days')
            GROUP BY pp.data_pesquisa
            ORDER BY pp.data_pesquisa ASC
        """, (pc_id_graf,))

        hist_nosso = query(f"""
            SELECT pp.data_pesquisa, AVG(ppi.preco)
            FROM pesquisa_preco_item ppi
            JOIN pesquisa_preco pp ON ppi.pesquisa_id=pp.pesquisa_id
            WHERE ppi.produto_id=?
              AND ppi.produto_concorrente_id IS NULL
              AND pp.fornecedor_id=?
              AND pp.status='finalizado'
              AND ppi.preco IS NOT NULL
              AND pp.data_pesquisa >= date('now','-{dias} days')
            GROUP BY pp.data_pesquisa
            ORDER BY pp.data_pesquisa ASC
        """, (pid, forn_sel[0]))

        if hist_nosso or hist_conc:
            # Monta séries separadas e combina por merge (evita datas duplicadas)
            series = {}
            if hist_nosso:
                df_n = pd.DataFrame(hist_nosso, columns=["Data", prod_nome[:25]])
                df_n["Data"] = pd.to_datetime(df_n["Data"], format="mixed")
                df_n = df_n.groupby("Data").mean()  # média se ainda restar duplicata
                series[prod_nome[:25]] = df_n[prod_nome[:25]]
            if hist_conc:
                label_c = f"{marca_graf} {desc_graf[:20]}"
                df_c = pd.DataFrame(hist_conc, columns=["Data", label_c])
                df_c["Data"] = pd.to_datetime(df_c["Data"], format="mixed")
                df_c = df_c.groupby("Data").mean()
                series[label_c] = df_c[label_c]

            if series:
                df_graf = pd.DataFrame(series)
                df_graf = df_graf.sort_index()
                st.caption(
                    f"Comparativo com **{marca_graf} — {desc_graf}** "
                    f"({direto_mais_pesquisas[12]} pesquisa(s) no período)"
                )
                st.line_chart(df_graf, height=220)
        else:
            st.caption("Sem histórico suficiente para o gráfico no período selecionado.")
    else:
        st.caption("Adicione pesquisas de preço para ver o gráfico comparativo.")

    # ── Exportação ────────────────────────────────────────────────────────
    st.divider()
    if concorrentes:
        rows_exp = []
        for row in concorrentes:
            (pc_id, marca, desc_c, peso_c, um_c, auditavel,
             tipo_rel, ultimo_preco, data_ult, pdv_ult,
             media_frt, em_oferta, n_pesq) = row
            diff_v = None
            if preco_ref and ultimo_preco:
                diff_v = round((ultimo_preco - preco_ref) / preco_ref * 100, 1)
            rows_exp.append({
                "Produto nosso":    prod_nome,
                "Nosso preço":      preco_ref,
                "Marca conc.":      marca,
                "Produto conc.":    desc_c,
                "Peso conc.":       f"{peso_c}{um_c}" if peso_c else "",
                "Tipo relação":     tipo_rel,
                "Último preço":     ultimo_preco,
                "Data pesquisa":    (data_ult or "")[:10],
                "PDV pesquisado":   pdv_ult,
                "Dif. % vs nosso":  diff_v,
                "Média frentes":    media_frt,
                "Em oferta":        "Sim" if em_oferta else "Não",
                "Nº pesquisas":     n_pesq or 0,
            })

        df_exp = pd.DataFrame(rows_exp)
        buf = io.BytesIO()
        df_exp.to_excel(buf, index=False, sheet_name="Análise Competitiva")
        buf.seek(0)
        st.download_button(
            f"⬇️ Exportar análise — {prod_nome}",
            data=buf,
            file_name=f"competitivo_{prod_nome[:20].replace(' ','_')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )