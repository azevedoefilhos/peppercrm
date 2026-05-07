#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

# Fix: buscar itens ja pesquisados e incluir status no label do produto
OLD = '''    lista_prods = _buscar_produtos_rapido(cat_id, marca_id, marca_tipo)

    if not lista_prods:
        st.info("Nenhum produto encontrado para os filtros selecionados.")
        return

    prod_opts = [(None, None, None, "? Selecione um produto")] + lista_prods
    prod_sel_r = st.selectbox("3. Produto", prod_opts,
                              format_func=lambda x: x[3], key=f"rp_prod_{pq_id}")

    if not prod_sel_r or prod_sel_r[0] is None:
        return

    tipo_sel, id_sel, _, label_sel = prod_sel_r

    st.divider()

    # ?? Resolu??o do produto selecionado ?????????????
    # Fun??o central: futuramente receber? EAN do leitor de c?mera
    _resolver_e_coletar(pq_id, forn_id, tipo_sel, id_sel, label_sel)'''

NEW = '''    lista_prods = _buscar_produtos_rapido(cat_id, marca_id, marca_tipo)

    if not lista_prods:
        st.info("Nenhum produto encontrado para os filtros selecionados.")
        return

    # Busca itens ja pesquisados nesta pesquisa para indicar status
    _pesquisados = query("""
        SELECT produto_id, produto_concorrente_id, preco, em_oferta, ponto_extra, ruptura
        FROM pesquisa_preco_item WHERE pesquisa_id=?
    """, (pq_id,))
    _map_pesq = {}
    for _row in _pesquisados:
        _pid, _pcid, _preco, _of, _pe, _rup = _row
        if _pid:   _map_pesq[("nosso", _pid)] = (_preco, _of, _pe, _rup)
        if _pcid:  _map_pesq[("conc", _pcid)] = (_preco, _of, _pe, _rup)

    def _label_com_status(tipo, id_, label_base):
        dados = _map_pesq.get((tipo, id_))
        if not dados:
            return label_base
        preco, of, pe, rup = dados
        badges = ""
        if rup:   return f"\u2705 {label_base}  \u2014  \u26a0\ufe0f Ruptura"
        preco_s = f"R$ {preco:,.2f}".replace(",","X").replace(".",",").replace("X",".") if preco else "?"
        if of: badges += " \U0001f3f7\ufe0f"
        if pe: badges += " \U0001f4cc"
        return f"\u2705 {label_base}  \u2014  {preco_s}{badges}"

    prod_opts = [(None, None, None, "\U0001f4cb Selecione um produto")] + [
        (tipo, id_, ean, _label_com_status(tipo, id_, lbl))
        for tipo, id_, ean, lbl in lista_prods
    ]
    prod_sel_r = st.selectbox("3. Produto", prod_opts,
                              format_func=lambda x: x[3], key=f"rp_prod_{pq_id}")

    if not prod_sel_r or prod_sel_r[0] is None:
        return

    tipo_sel, id_sel, _, label_sel = prod_sel_r

    # Mostra status do produto selecionado
    dados_sel = _map_pesq.get((tipo_sel, id_sel))
    if dados_sel:
        preco_s2, of2, pe2, rup2 = dados_sel
        if rup2:
            st.warning(f"\u26a0\ufe0f **{label_sel.split('\u2014')[0].strip()}** \u2014 Ruptura j\u00e1 registrada. Deseja atualizar?")
        else:
            preco_fmt = f"R$ {preco_s2:,.2f}".replace(",","X").replace(".",",").replace("X",".") if preco_s2 else "?"
            badges2 = ("\U0001f3f7\ufe0f " if of2 else "") + ("\U0001f4cc" if pe2 else "")
            st.info(f"\u2705 J\u00e1 pesquisado: **{preco_fmt}** {badges2} \u2014 Edite abaixo se quiser atualizar.")

    st.divider()

    # Resolucao do produto selecionado
    _resolver_e_coletar(pq_id, forn_id, tipo_sel, id_sel, label_sel)'''

# Aplica apenas na segunda instancia (modo rapido correto)
count = src.count(OLD)
print(f"Ocorrencias: {count}")
if count >= 1:
    src = src.replace(OLD, NEW)
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("OK")
else:
    print("NAO ENCONTRADO")
