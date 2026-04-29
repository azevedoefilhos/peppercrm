# comissoes.py — PepperCRM
# Configuração de percentuais, cálculo, pagamento e relatório de comissões

import streamlit as st
import pandas as pd
import io
from database import conectar, query, get_percentual_comissao


def _ir(p):
    st.session_state["pagina"] = p
    st.rerun()


def _fmt_brl(v):
    if v is None: return "R$ 0,00"
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")


def _fmt_pct(v):
    if v is None: return "0,00%"
    return f"{v:.2f}%".replace(".",",")


STATUS_PAG = ["PENDENTE", "PAGO_PARCIAL", "PAGO", "DIVERGENTE"]
ICONE_PAG  = {
    "PENDENTE":     "⏳",
    "PAGO_PARCIAL": "🔵",
    "PAGO":         "✅",
    "DIVERGENTE":   "⚠️",
}


# ═══════════════════════════════════════════════════════
# ENTRADA PRINCIPAL
# ═══════════════════════════════════════════════════════

def tela_comissoes():
    st.header("Comissões")
    if st.button("⬅ Voltar"):
        _ir("home")

    ABAS_COM = {"cfg":"Configurar %","ped":"Comissões","pag":"Pagamentos","rel":"Relatório"}
    if "com_aba" not in st.session_state: st.session_state["com_aba"] = "cfg"
    cols = st.columns(4)
    for col,(k,v) in zip(cols, ABAS_COM.items()):
        ativa = st.session_state["com_aba"] == k
        if col.button(v, key=f"comnav_{k}", use_container_width=True,
                      type="primary" if ativa else "secondary"):
            st.session_state["com_aba"] = k; st.rerun()
    st.divider()
    a = st.session_state["com_aba"]
    if a=="cfg":  _tela_configurar()
    elif a=="ped":_tela_por_pedido()
    elif a=="pag":_tela_pagamentos()
    elif a=="rel":_tela_relatorio()


# ═══════════════════════════════════════════════════════
# 1. CONFIGURAR PERCENTUAIS
# ═══════════════════════════════════════════════════════

def _tela_configurar():
    st.subheader("Percentual de comissão por fornecedor")

    forns = query(
        "SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia"
    )
    if not forns:
        st.warning("Nenhum fornecedor cadastrado.")
        return

    dados = query("""
        SELECT f.nome_fantasia,
               COALESCE(com.percentual,0) AS perc,
               COALESCE(com.observacao,'—') AS obs,
               COALESCE(com.ativo,0) AS ativo
        FROM fornecedor f
        LEFT JOIN comissao com ON f.fornecedor_id=com.fornecedor_id
        WHERE f.ativo=1 ORDER BY f.nome_fantasia
    """)
    if dados:
        df = pd.DataFrame(dados, columns=["Fornecedor","% Comissao","Observacao","Ativo"])
        df["Ativo"] = df["Ativo"].map({1:"✅",0:"❌"})
        df["% Comissao"] = df["% Comissao"].apply(lambda v: f"{v:.2f}%".replace(".",","))
        st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Cadastrar / atualizar comissao")

    # Exibe banner de sucesso persistente (antes do form, sobrevive ao rerun)
    msg_com = st.session_state.pop("com_salvo_msg", None)
    if msg_com:
        st.success(msg_com)

    # Selectbox FORA do form para que a mudanca de fornecedor seja reativa
    forn_sel = st.selectbox("Fornecedor", forns, format_func=lambda x: x[1],
                            key="com_forn_sel")

    # Busca percentual e observacao atuais do fornecedor selecionado
    com_atual = query("""SELECT percentual, observacao FROM comissao
                         WHERE fornecedor_id=? AND ativo=1 LIMIT 1""",
                      (forn_sel[0],))
    perc_atual = float(com_atual[0][0]) if com_atual else 0.0
    obs_atual  = com_atual[0][1] if com_atual and com_atual[0][1] else ""

    st.caption(f"Percentual atual cadastrado: **{perc_atual:.2f}%**")

    with st.form("form_com_forn", clear_on_submit=True):
        percentual = st.number_input("Novo percentual (%)",
                                     min_value=0.0, max_value=100.0,
                                     value=perc_atual, step=0.5, format="%.2f")
        obs        = st.text_input("Observacao", value=obs_atual)
        salvar     = st.form_submit_button("💾 Salvar comissao", type="primary")

    if salvar:
        conn = conectar()
        conn.execute("""
            INSERT INTO comissao (fornecedor_id, percentual, observacao, ativo)
            VALUES (?,?,?,1)
            ON CONFLICT(fornecedor_id)
            DO UPDATE SET percentual=excluded.percentual,
                          observacao=excluded.observacao, ativo=1
        """, (forn_sel[0], percentual, obs or None))
        conn.commit()
        conn.close()
        st.session_state["com_salvo_msg"] = (
            f"✅ Comissao de **{percentual:.2f}%** salva para **{forn_sel[1]}**!"
        )
        st.rerun()


# ═══════════════════════════════════════════════════════
# 2. COMISSÕES POR PEDIDO
# ═══════════════════════════════════════════════════════

def _tela_por_pedido():
    st.subheader("Comissão por pedido")
    st.caption("Pedidos ENTREGUE têm comissão calculada automaticamente. "
               "Ajuste o percentual individualmente quando necessário.")

    col1, col2, col3 = st.columns(3)
    forns = [(None,"Todos")] + query(
        "SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia"
    )
    with col1:
        forn_f  = st.selectbox("Fornecedor", forns, format_func=lambda x: x[1], key="cf_forn")
    with col2:
        status_f = st.selectbox("Status",
                                ["ENTREGUE","Confirmados + Entregues","Todos"],
                                key="cf_stat")
    with col3:
        periodo = st.selectbox("Período",
                               ["Mês atual","Mês anterior","Trimestre","Ano atual","Todos"],
                               key="cf_per")

    where, params = ["p.status_pedido NOT IN ('CANCELADO','RECUSADO')"], []
    if forn_f and forn_f[0]:
        where.append("p.fornecedor_id=?"); params.append(forn_f[0])
    if status_f == "ENTREGUE":
        where.append("p.status_pedido='ENTREGUE'")
    elif status_f == "Confirmados + Entregues":
        where.append("p.status_pedido IN ('ENTREGUE','CONFIRMADO')")
    for op, sql in {
        "Mês atual":    "p.data_pedido >= date('now','start of month')",
        "Mês anterior": "p.data_pedido BETWEEN date('now','start of month','-1 month') AND date('now','start of month','-1 day')",
        "Trimestre":    "p.data_pedido >= date('now','-3 months')",
        "Ano atual":    "p.data_pedido >= date('now','start of year')",
    }.items():
        if periodo == op: where.append(sql)

    dados = query(f"""
        SELECT p.pedido_id, p.data_pedido,
               cli.nome_fantasia,
               f.nome_fantasia,
               p.status_pedido,
               ROUND(SUM(pi.quantidade*pi.preco_final
                         *(1-COALESCE(p.desconto_geral,0)/100.0)),2) AS base,
               COALESCE(p.comissao_percentual, COALESCE(com.percentual,0)) AS perc,
               ROUND(SUM(pi.quantidade*pi.preco_final
                         *(1-COALESCE(p.desconto_geral,0)/100.0))
                     * COALESCE(p.comissao_percentual,COALESCE(com.percentual,0))/100.0,2) AS valor_com,
               COALESCE(cpag.status_pagamento,'PENDENTE') AS st_pag,
               COALESCE(cpag.valor_pago, 0) AS valor_pago
        FROM pedido p
        JOIN cliente cli  ON p.cliente_id=cli.cliente_id
        JOIN fornecedor f ON p.fornecedor_id=f.fornecedor_id
        LEFT JOIN pedido_item pi ON p.pedido_id=pi.pedido_id
            AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
        LEFT JOIN comissao com ON p.fornecedor_id=com.fornecedor_id AND com.ativo=1
        LEFT JOIN comissao_pagamento cpag ON p.pedido_id=cpag.pedido_id
        WHERE {' AND '.join(where)}
        GROUP BY p.pedido_id, p.data_pedido, cli.nome_fantasia, f.nome_fantasia, p.status_pedido, p.comissao_percentual, p.desconto_geral, cpag.status_pagamento, cpag.valor_pago, com.percentual
        ORDER BY p.data_pedido DESC
    """, tuple(params))

    if not dados:
        st.info("Nenhum pedido encontrado.")
        return

    df = pd.DataFrame(dados, columns=[
        "Pedido","Data","Cliente","Fornecedor","Status",
        "Base","% Com.","Comissao","St. Pagto","Valor pago"
    ])

    # Separa recusados — exibe mas nao soma
    df_validos   = df[~df["Status"].isin(["RECUSADO","CANCELADO"])]
    df_recusados = df[df["Status"].isin(["RECUSADO","CANCELADO"])]

    total_base = df_validos["Base"].sum()
    total_com  = df_validos["Comissao"].sum()
    total_pago = df_validos["Valor pago"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total faturado", _fmt_brl(total_base))
    col2.metric("Total comissao", _fmt_brl(total_com))
    col3.metric("Total pago",     _fmt_brl(total_pago))

    def _fmt_df(d):
        d = d.copy()
        d["Base"]       = d["Base"].apply(_fmt_brl)
        d["% Com."]     = d["% Com."].apply(_fmt_pct)
        d["Comissao"]   = d["Comissao"].apply(_fmt_brl)
        d["Valor pago"] = d["Valor pago"].apply(_fmt_brl)
        d["St. Pagto"]  = d["St. Pagto"].apply(
            lambda s: f"{ICONE_PAG.get(s,'')} {s}")
        return d

    st.dataframe(_fmt_df(df_validos), use_container_width=True, hide_index=True)

    if not df_recusados.empty:
        with st.expander(f"Pedidos recusados/cancelados ({len(df_recusados)}) — nao somados"):
            st.caption("Estes pedidos aparecem como referencia mas NAO entram nos totais acima.")
            st.dataframe(_fmt_df(df_recusados), use_container_width=True, hide_index=True)

    # Ajuste de percentual
    st.divider()
    st.subheader("Ajustar percentual de um pedido")
    ids = [(r[0], f"#{r[0]} — {r[2]} / {r[3]} — {r[1]}") for r in dados]
    ped_sel = st.selectbox("Pedido", ids, format_func=lambda x: x[1], key="adj_ped")
    if ped_sel:
        perc_at = next((r[6] for r in dados if r[0]==ped_sel[0]), 0.0)
        col1, col2 = st.columns(2)
        with col1:
            novo_perc = st.number_input("Novo %", min_value=0.0, max_value=100.0,
                                        value=float(perc_at), step=0.25, format="%.2f",
                                        key="np_ped")
        with col2:
            obs_adj = st.text_input("Motivo", key="obs_adj")
        if st.button("Aplicar ajuste"):
            from database import registrar_historico
            conn = conectar()
            registrar_historico(conn, ped_sel[0], "comissao_percentual",
                                 perc_at, novo_perc, obs_adj or "Ajuste manual")
            conn.execute("UPDATE pedido SET comissao_percentual=? WHERE pedido_id=?",
                         (novo_perc, ped_sel[0]))
            conn.commit(); conn.close()
            st.success(f"Percentual atualizado para {novo_perc:.2f}%!")
            st.rerun()

    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df.to_excel(w, index=False, sheet_name="Comissoes")
    buf.seek(0)
    st.download_button("⬇️ Exportar Excel", data=buf,
                       file_name="comissoes_por_pedido.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ═══════════════════════════════════════════════════════
# 3. CONTROLE DE PAGAMENTOS
# ═══════════════════════════════════════════════════════

def _tela_pagamentos():
    st.subheader("Controle de pagamento de comissões")
    st.caption(
        "Registre o pagamento de cada comissão — incluindo valores divergentes "
        "por itens não entregues ou pendentes."
    )

    # Pedidos ENTREGUE pendentes de pagamento ou com divergência
    col1, col2 = st.columns(2)
    forns = [(None,"Todos")] + query(
        "SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia"
    )
    with col1:
        forn_f = st.selectbox("Fornecedor", forns, format_func=lambda x: x[1], key="pag_forn")
    with col2:
        st_pag_f = st.selectbox("Status pagamento",
                                ["Todos","PENDENTE","PAGO_PARCIAL","DIVERGENTE","PAGO"],
                                key="pag_stat")

    where  = ["p.status_pedido='ENTREGUE'"]
    params = []
    if forn_f and forn_f[0]:
        where.append("p.fornecedor_id=?"); params.append(forn_f[0])
    if st_pag_f != "Todos":
        if st_pag_f == "PENDENTE":
            where.append("(cpag.status_pagamento IS NULL OR cpag.status_pagamento='PENDENTE')")
        else:
            where.append("cpag.status_pagamento=?"); params.append(st_pag_f)

    pedidos = query(f"""
        SELECT p.pedido_id, p.data_pedido,
               cli.nome_fantasia,
               f.nome_fantasia,
               ROUND(SUM(pi.quantidade*pi.preco_final
                         *(1-COALESCE(p.desconto_geral,0)/100.0)),2) AS base,
               COALESCE(p.comissao_percentual,COALESCE(com.percentual,0)) AS perc,
               ROUND(SUM(pi.quantidade*pi.preco_final
                         *(1-COALESCE(p.desconto_geral,0)/100.0))
                     * COALESCE(p.comissao_percentual,COALESCE(com.percentual,0))/100.0,2) AS previsto,
               COALESCE(cpag.valor_pago, 0)            AS pago,
               COALESCE(cpag.data_pagamento,'—')        AS dt_pag,
               COALESCE(cpag.status_pagamento,'PENDENTE') AS st_pag,
               COALESCE(cpag.observacao,'')             AS obs_pag
        FROM pedido p
        JOIN cliente cli  ON p.cliente_id=cli.cliente_id
        JOIN fornecedor f ON p.fornecedor_id=f.fornecedor_id
        LEFT JOIN pedido_item pi ON p.pedido_id=pi.pedido_id
            AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
        LEFT JOIN comissao com ON p.fornecedor_id=com.fornecedor_id AND com.ativo=1
        LEFT JOIN comissao_pagamento cpag ON p.pedido_id=cpag.pedido_id
        WHERE {' AND '.join(where)}
        GROUP BY p.pedido_id, p.data_pedido, cli.nome_fantasia, f.nome_fantasia, p.comissao_percentual, p.desconto_geral, cpag.valor_pago, cpag.data_pagamento, cpag.status_pagamento, cpag.observacao, com.percentual
        ORDER BY p.data_pedido DESC
    """, tuple(params))

    if not pedidos:
        st.info("Nenhum pedido encontrado.")
        return

    # Métricas
    total_prev = sum(r[6] for r in pedidos if r[6])
    total_pago = sum(r[7] for r in pedidos if r[7])
    pendente   = total_prev - total_pago

    col1, col2, col3 = st.columns(3)
    col1.metric("Total previsto", _fmt_brl(total_prev))
    col2.metric("Total pago",     _fmt_brl(total_pago))
    col3.metric("A receber",      _fmt_brl(pendente))

    # Lista de pedidos
    for ped in pedidos:
        (ped_id, data, cliente, forn, base, perc,
         previsto, pago, dt_pag, st_pag, obs_pag) = ped

        icone = ICONE_PAG.get(st_pag, "⏳")
        label = (f"{icone} Pedido #{ped_id} — {cliente} / {forn} — {data}"
                 f"  |  Previsto: {_fmt_brl(previsto)}"
                 f"  |  Pago: {_fmt_brl(pago) if pago else '—'}")

        with st.expander(label):
            col1, col2, col3 = st.columns(3)
            col1.metric("Base cálculo",   _fmt_brl(base))
            col2.metric("% Comissão",     _fmt_pct(perc))
            col3.metric("Valor previsto", _fmt_brl(previsto))

            # Status atual do pagamento
            if pago and pago > 0:
                divergencia = round(previsto - pago, 2) if previsto else 0
                col1, col2, col3 = st.columns(3)
                col1.metric("Valor pago", _fmt_brl(pago))
                col2.metric("Data pagamento", dt_pag[:10] if dt_pag and dt_pag != "—" else "—")
                if divergencia and divergencia != 0:
                    sinal = f"-{_fmt_brl(abs(divergencia))}" if divergencia > 0 else f"+{_fmt_brl(abs(divergencia))}"
                    col3.metric("Divergencia", sinal,
                                delta_color="inverse" if divergencia > 0 else "normal")
                else:
                    col3.metric("Divergencia", "Sem divergencia")
                if obs_pag:
                    st.info(f"Obs. registrada: {obs_pag}")

            st.divider()
            st.caption("Registrar ou atualizar pagamento:")
            with st.form(f"pag_{ped_id}"):
                col1, col2 = st.columns(2)
                with col1:
                    novo_status = st.selectbox(
                        "Status do pagamento",
                        STATUS_PAG,
                        index=STATUS_PAG.index(st_pag) if st_pag in STATUS_PAG else 0,
                        key=f"st_pag_{ped_id}"
                    )
                    valor_pago_n = st.number_input(
                        "Valor pago (R$)",
                        min_value=0.0,
                        value=float(pago or previsto or 0),
                        step=0.01, format="%.2f",
                        key=f"vp_{ped_id}",
                        help="Se divergente do previsto, informe o valor efetivamente recebido"
                    )
                with col2:
                    from datetime import date as _date
                    dt_pag_n = st.date_input(
                        "Data do pagamento",
                        value=_date.today(),
                        key=f"dp_{ped_id}"
                    )
                    obs_n = st.text_input(
                        "Observacao / motivo da divergencia",
                        value=obs_pag or "",
                        placeholder="Ex: Item 3 nao entregue, desconto de R$45,00",
                        key=f"op_{ped_id}"
                    )
                    # Calcula divergencia em tempo real para mostrar no form
                    if previsto and valor_pago_n != previsto:
                        dif_form = round(previsto - valor_pago_n, 2)
                        if dif_form > 0:
                            st.caption(f"Divergencia: -{_fmt_brl(dif_form)} vs previsto")
                        elif dif_form < 0:
                            st.caption(f"Divergencia: +{_fmt_brl(abs(dif_form))} vs previsto")

                salvar_pag = st.form_submit_button("Registrar pagamento", type="primary")

            if salvar_pag:
                conn = conectar()
                conn.execute("""
                    INSERT INTO comissao_pagamento
                    (pedido_id, data_pagamento, valor_previsto, valor_pago,
                     status_pagamento, observacao)
                    VALUES (?,?,?,?,?,?)
                    ON CONFLICT(pedido_id)
                    DO UPDATE SET
                        data_pagamento=excluded.data_pagamento,
                        valor_previsto=excluded.valor_previsto,
                        valor_pago=excluded.valor_pago,
                        status_pagamento=excluded.status_pagamento,
                        observacao=excluded.observacao
                """, (ped_id, str(dt_pag_n), previsto,
                      valor_pago_n, novo_status, obs_n or None))
                conn.commit()
                conn.close()
                st.success(f"Pagamento do Pedido #{ped_id} registrado!")
                st.rerun()


# ═══════════════════════════════════════════════════════
# 4. RELATÓRIO CONSOLIDADO
# ═══════════════════════════════════════════════════════

def _tela_relatorio():
    st.subheader("Relatório consolidado de comissões")

    col1, col2 = st.columns(2)
    with col1:
        periodo = st.selectbox(
            "Período",
            ["Mês atual","Mês anterior","Trimestre","Ano atual","Personalizado"],
            key="rel_com_per"
        )
    with col2:
        apenas_entregues = st.checkbox("Apenas pedidos ENTREGUE", value=True)

    periodos_sql = {
        "Mês atual":    ("date('now','start of month')",  "date('now')"),
        "Mês anterior": ("date('now','start of month','-1 month')",
                         "date('now','start of month','-1 day')"),
        "Trimestre":    ("date('now','-3 months')",       "date('now')"),
        "Ano atual":    ("date('now','start of year')",   "date('now')"),
    }
    if periodo == "Personalizado":
        col1, col2 = st.columns(2)
        with col1: d_ini = str(st.date_input("De", key="rcp_ini"))
        with col2: d_fim = str(st.date_input("Até", key="rcp_fim"))
        d_ini_sql, d_fim_sql = f"'{d_ini}'", f"'{d_fim}'"
    else:
        d_ini_sql, d_fim_sql = periodos_sql.get(periodo,
            ("date('now','start of month')", "date('now')"))

    status_filter = "='ENTREGUE'" if apenas_entregues \
                    else "IN ('ENTREGUE','CONFIRMADO')"

    por_forn = query(f"""
        SELECT f.nome_fantasia,
               COUNT(DISTINCT p.pedido_id)                    AS pedidos,
               ROUND(SUM(pi.quantidade*pi.preco_final
                         *(1-COALESCE(p.desconto_geral,0)/100.0)),2) AS base,
               ROUND(SUM(pi.quantidade*pi.preco_final
                         *(1-COALESCE(p.desconto_geral,0)/100.0))
                     * COALESCE(p.comissao_percentual,COALESCE(com.percentual,0))/100.0,2) AS previsto,
               ROUND(COALESCE(SUM(cpag.valor_pago),0),2)      AS pago
        FROM pedido p
        JOIN fornecedor f ON p.fornecedor_id=f.fornecedor_id
        LEFT JOIN pedido_item pi ON p.pedido_id=pi.pedido_id
            AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
        LEFT JOIN comissao com ON p.fornecedor_id=com.fornecedor_id AND com.ativo=1
        LEFT JOIN comissao_pagamento cpag ON p.pedido_id=cpag.pedido_id
        WHERE p.status_pedido {status_filter}
          AND p.data_pedido BETWEEN {d_ini_sql} AND {d_fim_sql}
        GROUP BY f.fornecedor_id, f.nome_fantasia, p.comissao_percentual, com.percentual
        ORDER BY previsto DESC
    """)

    if not por_forn:
        st.info("Nenhum dado encontrado.")
        return

    total_base = sum(r[2] for r in por_forn if r[2])
    total_prev = sum(r[3] for r in por_forn if r[3])
    total_pago = sum(r[4] for r in por_forn if r[4])

    col1, col2, col3 = st.columns(3)
    col1.metric("Total faturado", _fmt_brl(total_base))
    col2.metric("Comissão prevista", _fmt_brl(total_prev))
    col3.metric("Comissão paga",     _fmt_brl(total_pago))

    df_f = pd.DataFrame(por_forn,
                        columns=["Fornecedor","Pedidos","Base (R$)",
                                 "Previsto (R$)","Pago (R$)"])
    df_f["Diferenca (R$)"] = df_f["Previsto (R$)"] - df_f["Pago (R$)"]
    df_f["% efetivo"] = df_f.apply(
        lambda r: _fmt_pct(r["Previsto (R$)"]/r["Base (R$)"]*100)
                  if r["Base (R$)"] else "—", axis=1
    )

    df_show = df_f.copy()
    for col in ["Base (R$)","Previsto (R$)","Pago (R$)","Diferença (R$)"]:
        df_show[col] = df_show[col].apply(_fmt_brl)
    st.dataframe(df_show, use_container_width=True, hide_index=True)

    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df_f.to_excel(w, index=False, sheet_name="Comissoes")
    buf.seek(0)
    st.download_button("⬇️ Exportar Excel", data=buf,
                       file_name="relatorio_comissoes.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")