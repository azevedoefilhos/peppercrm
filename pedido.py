# pedido.py -- PepperCRM
# Novo pedido: grade com ultimo pedido + mix completo + busca fora do mix

import streamlit as st
import pandas as pd
import io
from datetime import date
from database import conectar, query, get_fornecedores_do_cliente, get_mix_com_preco

STATUS_PEDIDO = ["ABERTO","ENVIADO","CONFIRMADO","FATURADO","ENTREGUE","CANCELADO","RECUSADO"]
STATUS_CORES  = {
    "ABERTO":     "🟡", "ENVIADO":    "📤", "CONFIRMADO": "✅",
    "FATURADO":   "🧾", "ENTREGUE":   "🟢", "CANCELADO":  "🔴", "RECUSADO":   "⛔",
}

def _ir(p):
    st.session_state["pagina"] = p
    st.rerun()

def _brl(v):
    if v is None: return "—"
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")


def tela_novo_pedido():
    st.header("Novo Pedido")
    if st.button("⬅ Voltar"):
        _ir("home")

    # PASSO 1: Cliente
    from database import _cache_todos_clientes
    clientes = [(r[0], r[1], None, None) if len(r)==2 else r
                for r in query("""SELECT cliente_id, nome_fantasia, cidade, estado
        FROM cliente WHERE ativo=1 ORDER BY nome_fantasia""")]
    if not clientes:
        st.warning("Nenhum cliente cadastrado.")
        return

    cli_sel = st.selectbox("Cliente", clientes,
                           format_func=lambda x: f"{x[1]}  ({x[2]}/{x[3]})",
                           key="ped_cli")
    cli_id = cli_sel[0]

    # PASSO 2: Fornecedor
    fornecedores = get_fornecedores_do_cliente(cli_id)
    if not fornecedores:
        st.warning("Este cliente não tem fornecedores vinculados. Vá em Clientes > Vinculos.")
        return

    forn_sel = st.selectbox("Fornecedor", fornecedores,
                            format_func=lambda x: x[2], key="ped_forn")
    forn_id   = forn_sel[1]
    tab_id    = forn_sel[3]
    tab_nome  = forn_sel[4] or "Sem tabela"
    prazo     = forn_sel[6] or "—"
    frete     = forn_sel[7] or "—"

    # Busca pedido mínimo do fornecedor
    _pm_row = query("SELECT pedido_minimo FROM fornecedor WHERE fornecedor_id=?", (forn_id,))
    pedido_minimo = float(_pm_row[0][0]) if _pm_row and _pm_row[0][0] else 0.0

    col1, col2, col3, col4 = st.columns(4)
    col1.info(f"Tabela: **{tab_nome}**")
    col2.info(f"Prazo: **{prazo}**")
    col3.info(f"Frete: **{frete}**")
    if pedido_minimo > 0:
        col4.warning(f"Mín: **{_brl(pedido_minimo)}**")

    # PASSO 3: PDV
    pdvs = query("""SELECT pdv_id, numero_loja, nome_loja, cidade, estado, gerente, horario_recebimento
        FROM pdv WHERE cliente_id=? AND ativo=1 ORDER BY numero_loja, nome_loja""", (cli_id,))

    pdv_id = None
    if pdvs:
        opcoes_pdv = [(None, "— Entrega na matriz / sem PDV")] + [
            (p[0], f"Loja {p[1] or ''} — {p[2]}  ({p[3]}/{p[4]})") for p in pdvs]
        pdv_sel = st.selectbox("Local de entrega (PDV)", opcoes_pdv,
                               format_func=lambda x: x[1], key="ped_pdv")
        pdv_id  = pdv_sel[0]
        if pdv_id:
            pdv_info = next((p for p in pdvs if p[0] == pdv_id), None)
            if pdv_info and pdv_info[5]:
                st.caption(f"Gerente: {pdv_info[5]}  |  Recebimento: {pdv_info[6] or '—'}")

    st.divider()

    # PASSO 4: Dados do pedido
    st.subheader("Dados do pedido")

    # Verifica se cliente tem central de compras
    central_cc = query("""SELECT nome_central, tipo_entrega, contato, fone, email,
                               endereco_cd, cidade_cd
                        FROM central_compras
                        WHERE cliente_id=? AND ativo=1 LIMIT 1""", (cli_id,))
    if central_cc:
        cc = central_cc[0]
        st.info(
            f"🏢 **Central de compras:** {cc[0]}  |  "
            f"Tipo entrega: **{cc[1]}**  |  "
            f"Comprador: {cc[2] or '—'}  |  "
            f"Fone: {cc[3] or '—'}  |  "
            f"Email: {cc[4] or '—'}"
        )
        if cc[1] and 'CD' in cc[1] and cc[5]:
            st.caption(f"📦 Endereco do CD: {cc[5]}, {cc[6] or ''}")

    col1, col2, col3, col4 = st.columns(4)
    with col1: nr_cliente    = st.text_input("Nr. pedido cliente", placeholder="opcional")
    with col2: nr_fornecedor = st.text_input("Nr. pedido fornecedor", placeholder="opcional")
    with col3: data_entrega  = st.date_input("Data de entrega", value=None)
    with col4: desc_geral    = st.number_input("Desconto geral (%)", min_value=0.0,
                                               max_value=100.0, value=0.0, step=0.5)
    col5, col6 = st.columns(2)
    with col5: observacao = st.text_input("Observacao do pedido")
    with col6:
        status_ini = st.selectbox("Status inicial", STATUS_PEDIDO,
                                  index=0, key="ped_status_ini")

    # Garante que observacao_completa sempre existe
    observacao_completa = observacao

    # Endereco de entrega alternativo (CD ou diferente da loja)
    with st.expander("📦 Endereco de entrega diferente do PDV selecionado"):
        st.caption("Preencha apenas se a entrega for em local diferente do PDV — "
                   "ex: Centro de Distribuicao da rede.")
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            end_entrega = st.text_input("Endereco de entrega",
                                        value=central_cc[0][5] if central_cc and central_cc[0][5] else "")
            cidade_ent  = st.text_input("Cidade",
                                        value=central_cc[0][6] if central_cc and central_cc[0][6] else "")
        with col_e2:
            resp_ent    = st.text_input("Responsavel pelo recebimento",
                                        value=central_cc[0][2] if central_cc and central_cc[0][2] else "")
            fone_ent    = st.text_input("Fone do responsavel",
                                        value=central_cc[0][3] if central_cc and central_cc[0][3] else "")
        obs_ent = st.text_input("Observacao de entrega")
        # Monta string de endereço alternativo para gravar na observação
        _end_alt = " | ".join(filter(None,[end_entrega, cidade_ent, resp_ent, fone_ent, obs_ent]))
        if _end_alt:
            observacao_completa = f"Entrega: {_end_alt}" + (f" | {observacao}" if observacao else "")
        else:
            observacao_completa = observacao

    st.divider()

    # PASSO 5: Grade de produtos
    st.subheader("Produtos")
    mix = get_mix_com_preco(cli_id, forn_id, pdv_id)

    chave_grade = f"grade_{cli_id}_{forn_id}_{pdv_id}"

    if not mix:
        st.info("Nenhum produto no mix para este cliente/loja. Use a busca abaixo para adicionar.")
        if chave_grade not in st.session_state:
            st.session_state[chave_grade] = {}
    else:
        mix_ultimo   = [m for m in mix if m[9] is not None]
        mix_restante = [m for m in mix if m[9] is None]
        if chave_grade not in st.session_state:
            st.session_state[chave_grade] = _inicializar_grade(mix_ultimo, mix_restante)
        if mix_ultimo:
            st.caption(f"Os {len(mix_ultimo)} produto(s) do ultimo pedido ja estao pre-preenchidos — ajuste as quantidades")

    grade = st.session_state[chave_grade]

    # Seletor de ordenação
    col_ord1, col_ord2 = st.columns([3, 1])
    with col_ord2:
        ordem = st.selectbox("Ordenar por",
                             ["Descricao (A-Z)", "Codigo do produto"],
                             key=f"ord_{chave_grade}")

    grade_atualizada = _renderizar_grade(grade, ordem) if grade else {}
    st.session_state[chave_grade] = grade_atualizada

    # Busca fora do mix
    st.divider()
    _bloco_busca_produto(cli_id, forn_id, pdv_id, tab_id, chave_grade)

    # Totalizador
    st.divider()
    itens_com_qtd = [(k, v) for k, v in grade_atualizada.items() if v["qtd"] > 0]
    total_bruto   = sum(v["preco"] * v["qtd"] for _, v in itens_com_qtd)
    total_final   = total_bruto * (1 - desc_geral / 100)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Itens no pedido",    len(itens_com_qtd))
    col2.metric("Caixas totais",      sum(v["qtd"] for _, v in itens_com_qtd))
    col3.metric("Total bruto",        _brl(total_bruto))
    col4.metric("Total c/ desconto",  _brl(total_final))

    if not itens_com_qtd:
        st.info("Adicione quantidades para salvar o pedido.")
        return

    # Verifica pedido mínimo
    _abaixo_minimo = pedido_minimo > 0 and total_final < pedido_minimo
    if _abaixo_minimo:
        _falta = pedido_minimo - total_final
        st.warning(
            f"⚠️ **Pedido abaixo do mínimo exigido.**  \n"
            f"Mínimo: **{_brl(pedido_minimo)}**  |  "
            f"Atual: **{_brl(total_final)}**  |  "
            f"Faltam: **{_brl(_falta)}**"
        )

    col_s, col_l = st.columns(2)
    with col_s:
        if st.button("💾 Salvar Pedido", type="primary",
                     use_container_width=True,
                     disabled=_abaixo_minimo):
            pid = _salvar_pedido(cli_id, forn_id, pdv_id, tab_id, prazo, frete,
                                 nr_cliente, nr_fornecedor,
                                 str(data_entrega) if data_entrega else None,
                                 desc_geral,
                                 observacao_completa,
                                 status_ini, itens_com_qtd)
            if pid:
                st.session_state.pop(chave_grade, None)
                st.success(f"Pedido #{pid} salvo com sucesso!")
                st.balloons()
    with col_l:
        # Exportar rascunho
        if itens_com_qtd:
            linhas = []
            for prod_id, item in itens_com_qtd:
                total_item = item["preco"] * item["qtd"] * (1 - item["desc"]/100)
                linhas.append({
                    "Codigo": item["codigo_forn"],
                    "Produto": item["descricao"],
                    "Un/Cx": item["un_cx"],
                    "Preco/Cx": item["preco"],
                    "Qtd (cx)": item["qtd"],
                    "Desc %": item["desc"],
                    "Total": round(total_item, 2),
                })
            buf = io.BytesIO()
            pd.DataFrame(linhas).to_excel(buf, index=False, sheet_name="Pedido")
            buf.seek(0)
            st.download_button("⬇️ Exportar rascunho Excel", data=buf,
                               file_name="pedido_rascunho.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True)


def _inicializar_grade(mix_ultimo, mix_restante):
    grade = {}
    for m in mix_ultimo:
        grade[m[0]] = {
            "codigo_forn": m[1], "codigo_cli": m[8] or "—",
            "descricao": m[3] or m[2], "un_cx": m[4] or 1,
            "um": m[5] or "UN", "preco": m[6] or 0.0,
            "desc_max": m[7] or 0.0, "ultima_qtd": m[9],
            "ultima_data": m[10], "qtd": m[9] or 0,
            "desc": 0.0, "do_ultimo": True,
        }
    for m in mix_restante:
        grade[m[0]] = {
            "codigo_forn": m[1], "codigo_cli": m[8] or "—",
            "descricao": m[3] or m[2], "un_cx": m[4] or 1,
            "um": m[5] or "UN", "preco": m[6] or 0.0,
            "desc_max": m[7] or 0.0, "ultima_qtd": None,
            "ultima_data": None, "qtd": 0,
            "desc": 0.0, "do_ultimo": False,
        }
    return grade


def _renderizar_grade(grade: dict, ordem: str = "Descricao (A-Z)") -> dict:
    cols_h = st.columns([1.2, 3.5, 0.7, 1.2, 1.5, 1.0, 0.8, 1.3])
    for col, h in zip(cols_h, ["Cód.Forn.","Produto","Un/Cx","Preço/Cx","Últ.pedido","Qtd.(cx)","Desc.%","Total"]):
        col.markdown(f"<small><b>{h}</b></small>", unsafe_allow_html=True)

    # Ordena conforme selecao do usuario
    if ordem == "Codigo do produto":
        itens_ord = sorted(grade.items(), key=lambda x: (x[1]["codigo_forn"] or "").upper())
    else:  # Descrição A-Z (padrão)
        itens_ord = sorted(grade.items(), key=lambda x: (x[1]["descricao"] or "").upper())

    # Produtos do ultimo pedido sempre primeiro dentro da ordenacao escolhida
    itens_ord = (
        sorted([i for i in itens_ord if i[1]["do_ultimo"]], key=lambda x: (x[1]["descricao"] or "").upper()
               if ordem != "Código do produto" else (x[1]["codigo_forn"] or "").upper()) +
        sorted([i for i in itens_ord if not i[1]["do_ultimo"]], key=lambda x: (x[1]["descricao"] or "").upper()
               if ordem != "Código do produto" else (x[1]["codigo_forn"] or "").upper())
    )

    grade_nova = dict(grade)
    for prod_id, item in itens_ord:
        marcador = "🟡 " if item["do_ultimo"] else ""
        c = st.columns([1.2, 3.5, 0.7, 1.2, 1.5, 1.0, 0.8, 1.3])
        c[0].caption(item["codigo_forn"])
        c[1].write(f"{marcador}{item['descricao']}")
        c[2].caption(f"{item['un_cx']} {item['um']}")
        c[3].caption(_brl(item["preco"]))
        if item["ultima_qtd"]:
            data_f = item["ultima_data"][:10] if item["ultima_data"] else ""
            c[4].caption(f"{item['ultima_qtd']}cx — {data_f}")
        else:
            c[4].caption("—")
        with c[5]:
            qtd = st.number_input("qtd", min_value=0, value=int(item["qtd"]),
                                  key=f"qtd_{prod_id}", label_visibility="collapsed")
        with c[6]:
            desc_max_v = float(item["desc_max"]) if item["desc_max"] else 100.0
            desc = st.number_input("desc", min_value=0.0, max_value=desc_max_v,
                                   value=float(item["desc"]), step=0.5,
                                   key=f"desc_{prod_id}", label_visibility="collapsed")
        total = qtd * item["preco"] * (1 - desc / 100)
        if qtd > 0:
            c[7].markdown(f"**{_brl(total)}**")
        else:
            c[7].caption(_brl(total))
        grade_nova[prod_id] = {**item, "qtd": qtd, "desc": desc}
    return grade_nova


def _bloco_busca_produto(cli_id, forn_id, pdv_id, tab_id, grade_key):
    with st.expander("🔍 Buscar e adicionar produto fora do mix"):
        busca = st.text_input("Digite codigo ou parte da descricao",
                              key=f"busca_{cli_id}_{forn_id}_{pdv_id}")
        if busca and len(busca) >= 2:
            resultados = query("""
                SELECT p.produto_id, p.codigo_produto, p.descricao_curta,
                       p.unidades_caixa, p.unidade_medida,
                       tpi.preco_caixa, tpi.desconto_maximo
                FROM produto p
                LEFT JOIN tabela_preco_item tpi
                       ON tpi.produto_id=p.produto_id AND tpi.tabela_preco_id=?
                WHERE p.fornecedor_id=? AND p.ativo=1
                  AND (p.codigo_produto LIKE ? OR p.descricao LIKE ? OR p.descricao_curta LIKE ?)
                ORDER BY p.descricao_curta LIMIT 20
            """, (tab_id, forn_id, f"%{busca}%", f"%{busca}%", f"%{busca}%"))

            if resultados:
                prod_add = st.selectbox("Selecione o produto", resultados,
                                        format_func=lambda x: f"{x[1]} — {x[2]}  ({_brl(x[5])}/cx)" if x[5] else f"{x[1]} — {x[2]}",
                                        key=f"prod_add_{cli_id}_{forn_id}_{pdv_id}")
                qtd_busca = st.number_input("Quantidade (cx)", min_value=1, value=1,
                                            key=f"qtd_busca_{prod_add[0]}")
                if st.button("➕ Adicionar ao pedido e ao mix",
                             key=f"btn_add_{cli_id}_{forn_id}_{pdv_id}"):
                    conn = conectar()
                    try:
                        conn.execute("""INSERT OR IGNORE INTO mix_cliente
                            (cliente_id, fornecedor_id, pdv_id, produto_id, ativo)
                            VALUES (?,?,?,?,1)""",
                            (cli_id, forn_id, pdv_id, prod_add[0]))
                        conn.commit()
                        if grade_key in st.session_state:
                            st.session_state[grade_key][prod_add[0]] = {
                                "codigo_forn": prod_add[1], "codigo_cli": "—",
                                "descricao": prod_add[2], "un_cx": prod_add[3] or 1,
                                "um": prod_add[4] or "UN", "preco": prod_add[5] or 0.0,
                                "desc_max": prod_add[6] or 0.0, "ultima_qtd": None,
                                "ultima_data": None, "qtd": qtd_busca,
                                "desc": 0.0, "do_ultimo": False,
                            }
                        st.success(f"'{prod_add[2]}' adicionado!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro: {e}")
                    finally:
                        conn.close()
            else:
                st.info("Nenhum produto encontrado.")


def _salvar_pedido(cli_id, forn_id, pdv_id, tab_id, prazo, frete,
                   nr_cliente, nr_fornecedor, data_entrega,
                   desc_geral, observacao, status_ini, itens):
    try:
        conn = conectar()
        cur  = conn.cursor()
        from datetime import date as _date
        _hoje = _date.today().isoformat()
        cur.execute("""INSERT INTO pedido
            (cliente_id, pdv_id, fornecedor_id, tabela_preco_id,
             prazo_pagamento, frete, nr_pedido_cliente, nr_pedido_fornecedor,
             data_pedido, data_entrega, desconto_geral, observacao, status_pedido)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (cli_id, pdv_id, forn_id, tab_id,
             prazo if prazo != "—" else None,
             frete if frete != "—" else None,
             nr_cliente or None, nr_fornecedor or None,
             _hoje, data_entrega, desc_geral, observacao or None, status_ini))
        pedido_id = cur.lastrowid

        for prod_id, item in itens:
            preco_final = item["preco"] * (1 - item["desc"]/100) * (1 - desc_geral/100)
            cur.execute("""INSERT INTO pedido_item
                (pedido_id, produto_id, preco_tabela, desconto, preco_final, quantidade, status_item)
                VALUES (?,?,?,?,?,?,'NORMAL')""",
                (pedido_id, prod_id, item["preco"], item["desc"],
                 round(preco_final, 4), item["qtd"]))

        conn.commit(); conn.close()
        return pedido_id
    except Exception as e:
        st.error(f"Erro ao salvar pedido: {e}")
        return None