# resultado_operacional.py — PepperCRM
# Painel de confronto: Comissões × Despesas
# Queries bifurcadas: SQLite local / PostgreSQL Railway

import streamlit as st
import pandas as pd
from datetime import date, timedelta
from database import query, execute_write, _check_supabase


# ── Garante tabela despesa ────────────────────────────────────────────────────

def _garantir_tabela_despesa():
    try:
        if _check_supabase():
            execute_write("""
                CREATE TABLE IF NOT EXISTS despesa (
                    despesa_id        SERIAL PRIMARY KEY,
                    data_despesa      DATE NOT NULL,
                    categoria         TEXT NOT NULL,
                    descricao         TEXT,
                    cliente_id        INTEGER,
                    fornecedor_id     INTEGER,
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
    except Exception:
        pass


def _q(sql_sqlite, sql_pg, params=()):
    """Executa a query correta conforme o banco ativo. Retorna [] em caso de erro."""
    try:
        if _check_supabase():
            return query(sql_pg, params) or []
        else:
            return query(sql_sqlite, params) or []
    except Exception:
        return []


# ── Formatação ────────────────────────────────────────────────────────────────

def _fmt_brl(v):
    if v is None or v == 0:
        return "R$ 0,00"
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ── Geração de meses ──────────────────────────────────────────────────────────

def _gerar_meses(n=12):
    hoje = date.today()
    meses = []
    for i in range(n - 1, -1, -1):
        primeiro = (hoje.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
        if primeiro.month == 12:
            ultimo = primeiro.replace(year=primeiro.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            ultimo = primeiro.replace(month=primeiro.month + 1, day=1) - timedelta(days=1)
        meses.append((primeiro.year, primeiro.month,
                      primeiro.strftime("%m/%Y"),
                      primeiro.isoformat(), ultimo.isoformat()))
    return meses


# ── Queries de comissões ──────────────────────────────────────────────────────

def _get_filtro_vendedor():
    """Retorna (sql_where, params) para filtrar pedidos pelo representante logado."""
    try:
        from permissoes import e_admin, e_master, usuario_id_atual, perfil_atual
        p = perfil_atual()
        uid = usuario_id_atual()
        if p in ("MASTER","ADM","REPRESENTANTE_ADM"):
            return "", []
        elif p in ("REPRESENTANTE","VENDEDOR"):
            return "AND p.vendedor_id=?", [uid]
        return "", []
    except Exception:
        return "", []

def _buscar_totais_periodo(visao, d_ini, d_fim):
    _fv_sql, _fv_params = _get_filtro_vendedor()
    if visao == "previsto":
        # SQLite: sem GROUP BY problema pois SUM envolve tudo
        # PG: comissao_percentual deve ser agregado — usamos MAX() pois é igual por pedido
        r_com = _q(
            # SQLite
            """SELECT ROUND(SUM(
                    pi.quantidade * pi.preco_final
                    * (1 - COALESCE(p.desconto_geral, 0) / 100.0)
                ) * COALESCE(p.comissao_percentual, COALESCE(com.percentual, 0)) / 100.0, 2)
                FROM pedido p
                JOIN pedido_item pi ON p.pedido_id = pi.pedido_id
                    AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
                LEFT JOIN comissao com ON p.fornecedor_id = com.fornecedor_id AND com.ativo = 1
                LEFT JOIN comissao_pagamento cpag ON p.pedido_id = cpag.pedido_id
                WHERE p.status_pedido = 'ENTREGUE'
                  AND COALESCE(cpag.status_pagamento, 'PENDENTE') IN ('PENDENTE','PAGO_PARCIAL')
                  AND COALESCE(p.data_entrega_realizada, p.data_pedido) BETWEEN ? AND ?""",
            # PostgreSQL
            """SELECT ROUND(SUM(sub.base * sub.perc / 100.0)::NUMERIC, 2)
                FROM (
                    SELECT
                        SUM(pi.quantidade * pi.preco_final
                            * (1 - COALESCE(p.desconto_geral, 0) / 100.0)) AS base,
                        COALESCE(MAX(p.comissao_percentual), MAX(com.percentual), 0) AS perc
                    FROM pedido p
                    JOIN pedido_item pi ON p.pedido_id = pi.pedido_id
                        AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
                    LEFT JOIN comissao com ON p.fornecedor_id = com.fornecedor_id AND com.ativo = 1
                    LEFT JOIN comissao_pagamento cpag ON p.pedido_id = cpag.pedido_id
                    WHERE p.status_pedido = 'ENTREGUE'
                      AND COALESCE(cpag.status_pagamento, 'PENDENTE') IN ('PENDENTE','PAGO_PARCIAL')
                      AND COALESCE(p.data_entrega_realizada, p.data_pedido) BETWEEN %s AND %s
                    GROUP BY p.pedido_id
                ) sub""",
            tuple([d_ini, d_fim] + _fv_params)
        )
    else:
        r_com = _q(
            """SELECT ROUND(SUM(valor_pago), 2) FROM comissao_pagamento
               WHERE status_pagamento IN ('PAGO','PAGO_PARCIAL')
                 AND data_pagamento BETWEEN ? AND ?""",
            """SELECT ROUND(SUM(valor_pago)::NUMERIC, 2) FROM comissao_pagamento
               WHERE status_pagamento IN ('PAGO','PAGO_PARCIAL')
                 AND data_pagamento BETWEEN %s AND %s""",
            (d_ini, d_fim)
        )

    r_desp = _q(
        f"""SELECT ROUND(SUM(valor), 2) FROM despesa
           WHERE ativo IS NOT FALSE AND data_despesa BETWEEN ? AND ?
           {"AND usuario_id=?" if _fv_params else ""}""",
        f"""SELECT ROUND(SUM(valor)::NUMERIC, 2) FROM despesa
           WHERE ativo IS NOT FALSE AND data_despesa BETWEEN %s AND %s
           {"AND usuario_id=%s" if _fv_params else ""}""",
        tuple([d_ini, d_fim] + _fv_params)
    )

    total_com  = float((r_com  or [[0]])[0][0] or 0)
    total_desp = float((r_desp or [[0]])[0][0] or 0)
    return total_com, total_desp


def _buscar_comissoes_por_mes(visao, meses):
    resultado = {(a, m): 0.0 for a, m, _, _, _ in meses}

    if visao == "previsto":
        rows = _q(
            # SQLite
            """SELECT
                CAST(strftime('%Y', COALESCE(p.data_entrega_realizada, p.data_pedido)) AS INTEGER) AS ano,
                CAST(strftime('%m', COALESCE(p.data_entrega_realizada, p.data_pedido)) AS INTEGER) AS mes,
                ROUND(SUM(pi.quantidade * pi.preco_final
                    * (1 - COALESCE(p.desconto_geral, 0) / 100.0)
                ) * COALESCE(p.comissao_percentual, COALESCE(com.percentual, 0)) / 100.0, 2) AS valor_com
               FROM pedido p
               JOIN pedido_item pi ON p.pedido_id = pi.pedido_id
                   AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
               LEFT JOIN comissao com ON p.fornecedor_id = com.fornecedor_id AND com.ativo = 1
               LEFT JOIN comissao_pagamento cpag ON p.pedido_id = cpag.pedido_id
               WHERE p.status_pedido = 'ENTREGUE'
                 AND COALESCE(cpag.status_pagamento, 'PENDENTE') IN ('PENDENTE','PAGO_PARCIAL')
               GROUP BY ano, mes""",
            # PostgreSQL — subquery por pedido, depois agrupa por mês
            """SELECT
                EXTRACT(YEAR  FROM competencia)::int AS ano,
                EXTRACT(MONTH FROM competencia)::int AS mes,
                ROUND(SUM(base * perc / 100.0)::NUMERIC, 2) AS valor_com
               FROM (
                   SELECT
                       COALESCE(p.data_entrega_realizada, p.data_pedido)::date AS competencia,
                       SUM(pi.quantidade * pi.preco_final
                           * (1 - COALESCE(p.desconto_geral, 0) / 100.0)) AS base,
                       COALESCE(MAX(p.comissao_percentual), MAX(com.percentual), 0) AS perc
                   FROM pedido p
                   JOIN pedido_item pi ON p.pedido_id = pi.pedido_id
                       AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
                   LEFT JOIN comissao com ON p.fornecedor_id = com.fornecedor_id AND com.ativo = 1
                   LEFT JOIN comissao_pagamento cpag ON p.pedido_id = cpag.pedido_id
                   WHERE p.status_pedido = 'ENTREGUE'
                     AND COALESCE(cpag.status_pagamento, 'PENDENTE') IN ('PENDENTE','PAGO_PARCIAL')
                   GROUP BY p.pedido_id, competencia
               ) sub
               GROUP BY ano, mes"""
        )
    else:
        rows = _q(
            """SELECT CAST(strftime('%Y', data_pagamento) AS INTEGER) AS ano,
                      CAST(strftime('%m', data_pagamento) AS INTEGER) AS mes,
                      ROUND(SUM(valor_pago), 2) AS valor_com
               FROM comissao_pagamento
               WHERE status_pagamento IN ('PAGO','PAGO_PARCIAL')
                 AND data_pagamento IS NOT NULL
               GROUP BY ano, mes""",
            """SELECT EXTRACT(YEAR  FROM data_pagamento::date)::int AS ano,
                      EXTRACT(MONTH FROM data_pagamento::date)::int AS mes,
                      ROUND(SUM(valor_pago)::NUMERIC, 2) AS valor_com
               FROM comissao_pagamento
               WHERE status_pagamento IN ('PAGO','PAGO_PARCIAL')
                 AND data_pagamento IS NOT NULL
               GROUP BY ano, mes"""
        )

    for row in (rows or []):
        chave = (int(row[0]), int(row[1]))
        if chave in resultado:
            resultado[chave] = float(row[2] or 0)
    return resultado


def _buscar_despesas_por_mes(meses):
    resultado = {(a, m): 0.0 for a, m, _, _, _ in meses}
    rows = _q(
        """SELECT CAST(strftime('%Y', data_despesa) AS INTEGER) AS ano,
                  CAST(strftime('%m', data_despesa) AS INTEGER) AS mes,
                  ROUND(SUM(valor), 2) AS total
           FROM despesa WHERE ativo IS NOT FALSE GROUP BY ano, mes""",
        """SELECT EXTRACT(YEAR  FROM data_despesa::date)::int AS ano,
                  EXTRACT(MONTH FROM data_despesa::date)::int AS mes,
                  ROUND(SUM(valor)::NUMERIC, 2) AS total
           FROM despesa WHERE ativo IS NOT FALSE GROUP BY ano, mes"""
    )
    for row in (rows or []):
        chave = (int(row[0]), int(row[1]))
        if chave in resultado:
            resultado[chave] = float(row[2] or 0)
    return resultado


def _buscar_despesas_por_categoria(d_ini, d_fim):
    return _q(
        """SELECT categoria, ROUND(SUM(valor), 2) AS total
           FROM despesa WHERE ativo IS NOT FALSE AND data_despesa BETWEEN ? AND ?
           GROUP BY categoria ORDER BY total DESC""",
        """SELECT categoria, ROUND(SUM(valor)::NUMERIC, 2) AS total
           FROM despesa WHERE ativo IS NOT FALSE AND data_despesa BETWEEN %s AND %s
           GROUP BY categoria ORDER BY total DESC""",
        (d_ini, d_fim)
    )


def _buscar_por_fornecedor(visao, d_ini, d_fim):
    if visao == "previsto":
        return _q(
            # SQLite
            """SELECT f.nome_fantasia,
                   ROUND(SUM(pi.quantidade * pi.preco_final
                       * (1 - COALESCE(p.desconto_geral, 0) / 100.0)
                   ) * COALESCE(p.comissao_percentual, COALESCE(com.percentual, 0)) / 100.0, 2) AS comissao,
                   ROUND(COALESCE((SELECT SUM(d.valor) FROM despesa d
                       WHERE d.fornecedor_id = f.fornecedor_id AND d.ativo IS NOT FALSE
                         AND d.data_despesa BETWEEN ? AND ?), 0), 2) AS despesas
               FROM pedido p
               JOIN fornecedor f ON p.fornecedor_id = f.fornecedor_id
               JOIN pedido_item pi ON p.pedido_id = pi.pedido_id
                   AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
               LEFT JOIN comissao com ON p.fornecedor_id = com.fornecedor_id AND com.ativo = 1
               LEFT JOIN comissao_pagamento cpag ON p.pedido_id = cpag.pedido_id
               WHERE p.status_pedido = 'ENTREGUE'
                 AND COALESCE(cpag.status_pagamento, 'PENDENTE') IN ('PENDENTE','PAGO_PARCIAL')
                 AND COALESCE(p.data_entrega_realizada, p.data_pedido) BETWEEN ? AND ?
               GROUP BY f.fornecedor_id, f.nome_fantasia
               ORDER BY comissao DESC""",
            # PostgreSQL
            """SELECT f.nome_fantasia,
                   ROUND(SUM(sub.base * sub.perc / 100.0)::NUMERIC, 2) AS comissao,
                   ROUND(COALESCE((SELECT SUM(d.valor) FROM despesa d
                       WHERE d.fornecedor_id = f.fornecedor_id AND d.ativo IS NOT FALSE
                         AND d.data_despesa BETWEEN %s AND %s), 0)::NUMERIC, 2) AS despesas
               FROM (
                   SELECT p.fornecedor_id,
                       SUM(pi.quantidade * pi.preco_final
                           * (1 - COALESCE(p.desconto_geral, 0) / 100.0)) AS base,
                       COALESCE(MAX(p.comissao_percentual), MAX(com.percentual), 0) AS perc
                   FROM pedido p
                   JOIN pedido_item pi ON p.pedido_id = pi.pedido_id
                       AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
                   LEFT JOIN comissao com ON p.fornecedor_id = com.fornecedor_id AND com.ativo = 1
                   LEFT JOIN comissao_pagamento cpag ON p.pedido_id = cpag.pedido_id
                   WHERE p.status_pedido = 'ENTREGUE'
                     AND COALESCE(cpag.status_pagamento, 'PENDENTE') IN ('PENDENTE','PAGO_PARCIAL')
                     AND COALESCE(p.data_entrega_realizada, p.data_pedido) BETWEEN %s AND %s
                   GROUP BY p.pedido_id, p.fornecedor_id
               ) sub
               JOIN fornecedor f ON sub.fornecedor_id = f.fornecedor_id
               GROUP BY f.fornecedor_id, f.nome_fantasia
               ORDER BY comissao DESC""",
            (d_ini, d_fim, d_ini, d_fim)
        )
    else:
        return _q(
            """SELECT f.nome_fantasia,
                   ROUND(SUM(cpag.valor_pago), 2) AS comissao,
                   ROUND(COALESCE((SELECT SUM(d.valor) FROM despesa d
                       WHERE d.fornecedor_id = f.fornecedor_id AND d.ativo IS NOT FALSE
                         AND d.data_despesa BETWEEN ? AND ?), 0), 2) AS despesas
               FROM comissao_pagamento cpag
               JOIN pedido p ON cpag.pedido_id = p.pedido_id
               JOIN fornecedor f ON p.fornecedor_id = f.fornecedor_id
               WHERE cpag.status_pagamento IN ('PAGO','PAGO_PARCIAL')
                 AND cpag.data_pagamento BETWEEN ? AND ?
               GROUP BY f.fornecedor_id, f.nome_fantasia ORDER BY comissao DESC""",
            """SELECT f.nome_fantasia,
                   ROUND(SUM(cpag.valor_pago)::NUMERIC, 2) AS comissao,
                   ROUND(COALESCE((SELECT SUM(d.valor) FROM despesa d
                       WHERE d.fornecedor_id = f.fornecedor_id AND d.ativo IS NOT FALSE
                         AND d.data_despesa BETWEEN %s AND %s), 0)::NUMERIC, 2) AS despesas
               FROM comissao_pagamento cpag
               JOIN pedido p ON cpag.pedido_id = p.pedido_id
               JOIN fornecedor f ON p.fornecedor_id = f.fornecedor_id
               WHERE cpag.status_pagamento IN ('PAGO','PAGO_PARCIAL')
                 AND cpag.data_pagamento BETWEEN %s AND %s
               GROUP BY f.fornecedor_id, f.nome_fantasia ORDER BY comissao DESC""",
            (d_ini, d_fim, d_ini, d_fim)
        )


# ═══════════════════════════════════════════════════════════════════════════════
# TELA PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

def tela_resultado_operacional():
    _garantir_tabela_despesa()

    st.subheader("📊 Resultado Operacional")
    st.caption(
        "Confronto entre receita de comissões e despesas operacionais. "
        "Use para avaliar a lucratividade real do período."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        visao = st.radio(
            "Visão das comissões",
            ["previsto", "realizado"],
            format_func=lambda x: (
                "⏳ A receber (pedidos entregues, pagto pendente)"
                if x == "previsto"
                else "✅ Efetivamente recebidas (pagas)"
            ),
            key="ro_visao",
        )
    with col2:
        hoje = date.today()
        periodo = st.selectbox(
            "Período",
            ["Mês atual", "Mês anterior", "Trimestre", "Semestre", "Ano atual", "Personalizado"],
            key="ro_periodo"
        )

    if periodo == "Mês atual":
        d_ini = hoje.replace(day=1); d_fim = hoje
    elif periodo == "Mês anterior":
        primeiro = hoje.replace(day=1); ul = primeiro - timedelta(days=1)
        d_ini = ul.replace(day=1); d_fim = ul
    elif periodo == "Trimestre":
        d_ini = (hoje - timedelta(days=90)).replace(day=1); d_fim = hoje
    elif periodo == "Semestre":
        d_ini = (hoje - timedelta(days=180)).replace(day=1); d_fim = hoje
    elif periodo == "Ano atual":
        d_ini = hoje.replace(month=1, day=1); d_fim = hoje
    else:
        with col3:
            d_ini = st.date_input("De",  value=hoje.replace(day=1), key="ro_ini")
            d_fim = st.date_input("Até", value=hoje,                 key="ro_fim")

    d_ini_str = d_ini.isoformat() if hasattr(d_ini, "isoformat") else str(d_ini)
    d_fim_str = d_fim.isoformat() if hasattr(d_fim, "isoformat") else str(d_fim)

    st.divider()

    # ── Cards ─────────────────────────────────────────────────────────────────
    total_com, total_desp = _buscar_totais_periodo(visao, d_ini_str, d_fim_str)
    saldo  = total_com - total_desp
    margem = (saldo / total_com * 100) if total_com > 0 else 0.0

    label_com = "⏳ A receber" if visao == "previsto" else "✅ Comissões recebidas"
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(label_com,     _fmt_brl(total_com))
    c2.metric("💸 Despesas", _fmt_brl(total_desp))
    c3.metric("💰 Saldo líquido", _fmt_brl(saldo),
              delta="positivo" if saldo >= 0 else "negativo",
              delta_color="normal" if saldo >= 0 else "inverse")
    c4.metric("📈 Margem líquida",
              f"{margem:.1f}%".replace(".", ","),
              delta=("saudável" if margem >= 30 else ("atenção" if margem >= 0 else "negativa")),
              delta_color=("normal" if margem >= 30 else ("off" if margem >= 0 else "inverse")))

    if saldo < 0:
        st.error(f"⚠️ Despesas superam comissões em **{_fmt_brl(abs(saldo))}** no período.")
    elif 0 <= margem < 30 and total_com > 0:
        st.warning(f"⚠️ Margem de **{margem:.1f}%** — despesas consumindo boa parte das comissões.")

    st.divider()

    # ── Gráfico mensal ────────────────────────────────────────────────────────
    st.markdown("#### Evolução mensal — últimos 12 meses")
    meses     = _gerar_meses(12)
    com_mes   = _buscar_comissoes_por_mes(visao, meses)
    desp_mes  = _buscar_despesas_por_mes(meses)
    labels     = [lb for _, _, lb, _, _ in meses]
    vals_com   = [com_mes.get((a, m), 0.0) for a, m, _, _, _ in meses]
    vals_desp  = [desp_mes.get((a, m), 0.0) for a, m, _, _, _ in meses]
    vals_saldo = [c - d for c, d in zip(vals_com, vals_desp)]

    try:
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Comissões" if visao == "realizado" else "A receber",
            x=labels, y=vals_com, marker_color="#2E7D32", opacity=0.85,
            text=[_fmt_brl(v) if v > 0 else "" for v in vals_com],
            textposition="outside", textfont=dict(size=9)
        ))
        fig.add_trace(go.Bar(
            name="Despesas", x=labels, y=vals_desp,
            marker_color="#C62828", opacity=0.85,
            text=[_fmt_brl(v) if v > 0 else "" for v in vals_desp],
            textposition="outside", textfont=dict(size=9)
        ))
        cores_saldo = ["#1565C0" if s >= 0 else "#E65100" for s in vals_saldo]
        fig.add_trace(go.Scatter(
            name="Saldo", x=labels, y=vals_saldo, mode="lines+markers",
            line=dict(color="#1565C0", width=2, dash="dot"),
            marker=dict(color=cores_saldo, size=8)
        ))
        fig.update_layout(
            barmode="group", height=380,
            margin=dict(t=20, b=20, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(tickprefix="R$ ", separatethousands=True),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(size=11), xaxis=dict(tickangle=-30)
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Gráfico indisponível: {e}")

    # ── Tabela mensal ─────────────────────────────────────────────────────────
    with st.expander("📋 Tabela mensal detalhada"):
        df_meses = pd.DataFrame([{
            "Mês":       labels[i],
            "Comissões": _fmt_brl(vals_com[i]),
            "Despesas":  _fmt_brl(vals_desp[i]),
            "Saldo":     _fmt_brl(vals_saldo[i]),
            "Margem %":  f"{(vals_saldo[i]/vals_com[i]*100):.1f}%".replace(".",",")
                         if vals_com[i] > 0 else "—",
        } for i in range(len(meses))])
        st.dataframe(df_meses, width="stretch", hide_index=True)

    st.divider()

    # ── Por fornecedor ────────────────────────────────────────────────────────
    st.markdown("#### Por fornecedor")
    rows_forn = _buscar_por_fornecedor(visao, d_ini_str, d_fim_str)
    if rows_forn:
        df_forn = pd.DataFrame([{
            "Fornecedor": r[0],
            "Comissões":  _fmt_brl(float(r[1] or 0)),
            "Despesas":   _fmt_brl(float(r[2] or 0)),
            "Saldo":      _fmt_brl(float(r[1] or 0) - float(r[2] or 0)),
            "Margem %":   f"{(float(r[1] or 0) - float(r[2] or 0)) / float(r[1] or 1) * 100:.1f}%".replace(".",",")
                          if float(r[1] or 0) > 0 else "—",
        } for r in rows_forn])
        st.dataframe(df_forn, width="stretch", hide_index=True)
    else:
        st.info("Nenhum dado de fornecedor no período.")

    st.divider()

    # ── Despesas por categoria ────────────────────────────────────────────────
    st.markdown("#### Despesas por categoria")
    cats = _buscar_despesas_por_categoria(d_ini_str, d_fim_str)
    if cats:
        total_cat = sum(float(r[1] or 0) for r in cats)
        df_cat = pd.DataFrame([{
            "Categoria":  r[0],
            "Total":      _fmt_brl(float(r[1] or 0)),
            "% do total": f"{float(r[1] or 0)/total_cat*100:.1f}%".replace(".",",")
                          if total_cat > 0 else "—",
        } for r in cats])
        st.dataframe(df_cat, width="stretch", hide_index=True)
        try:
            import plotly.express as px
            fig_cat = px.pie(
                names=[r[0] for r in cats], values=[float(r[1] or 0) for r in cats],
                hole=0.45, color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_cat.update_traces(textposition="inside", textinfo="percent+label")
            fig_cat.update_layout(height=300, showlegend=False,
                                  margin=dict(t=10,b=10,l=10,r=10),
                                  paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_cat, use_container_width=True)
        except Exception:
            pass
    else:
        st.info("Nenhuma despesa no período.")
