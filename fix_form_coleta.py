#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

# Fix 1: Chave k deve incluir produto_id ou pc_id para ser unica
OLD_K = '    k = f"ean_coleta_{pq_id}_{ean}"'
NEW_K = '''    # Chave unica baseada em produto_id ou pc_id (nao apenas EAN que pode ser vazio)
    _k_id = produto_id if produto_id else f"pc{pc_id}" if pc_id else ean
    k = f"ean_coleta_{pq_id}_{_k_id}"'''

if OLD_K in src:
    src = src.replace(OLD_K, NEW_K, 1)
    print("✅ Fix 1: chave k corrigida")
else:
    print("⚠️  Fix 1: padrão não encontrado")

# Fix 2: Botao "Não, próximo" deve limpar o campo correto
OLD_NAO = '''            st.session_state.pop(f"ean_input_{pq_id}", None)
            st.rerun()'''
NEW_NAO = '''            st.session_state.pop(f"ean_input_{pq_id}", None)
            st.session_state.pop(f"campo_busca_{pq_id}", None)
            st.rerun()'''

if OLD_NAO in src:
    src = src.replace(OLD_NAO, NEW_NAO, 1)
    print("✅ Fix 2: limpar campo_busca ao pular")
else:
    print("⚠️  Fix 2: padrão não encontrado")

# Fix 3: Envolve campos em st.form para evitar rerun ao preencher
OLD_FORM = '''    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            preco = st.number_input(
                "💰 Preço (R$) *",
                min_value=0.0, format="%.2f",
                step=0.01, key=f"{k}_preco")
        with col2:
            frentes = st.number_input(
                "Frentes", min_value=0,
                value=1, step=1, key=f"{k}_frt")
        with col3:
            col_of, col_pe = st.columns(2)
            oferta    = col_of.checkbox("Oferta", key=f"{k}_of")
            ponto_extra = col_pe.checkbox("P.Extra", key=f"{k}_pe")

        ruptura = st.checkbox("⚠️ Ruptura (sem estoque)", key=f"{k}_rup")'''

NEW_FORM = '''    with st.form(key=f"{k}_form", border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            preco = st.number_input(
                "💰 Preço (R$) *",
                min_value=0.0, format="%.2f",
                step=0.01, key=f"{k}_preco")
        with col2:
            frentes = st.number_input(
                "Frentes", min_value=0,
                value=1, step=1, key=f"{k}_frt")
        with col3:
            col_of, col_pe = st.columns(2)
            oferta    = col_of.checkbox("Oferta", key=f"{k}_of")
            ponto_extra = col_pe.checkbox("P.Extra", key=f"{k}_pe")

        ruptura = st.checkbox("⚠️ Ruptura (sem estoque)", key=f"{k}_rup")'''

if OLD_FORM in src:
    src = src.replace(OLD_FORM, NEW_FORM, 1)
    print("✅ Fix 3: container -> form")
else:
    print("⚠️  Fix 3: padrão não encontrado")

# Fix 4: Vinculo e obs precisam ficar dentro do form, e o botao salvar vira submit
OLD_VINC = '''        # Vínculo com produto próprio (só para concorrentes)
        prod_vinc_id = None
        if tipo == "conc":
            # Busca produtos nossos do mesmo fornecedor para vincular
            prods_n = query("""SELECT produto_id, descricao_curta, codigo_produto
                FROM produto WHERE fornecedor_id=(
                    SELECT conc.fornecedor_id FROM produto_concorrente pc
                    JOIN concorrente conc ON pc.concorrente_id=conc.concorrente_id
                    WHERE pc.produto_concorrente_id=?
                ) AND ativo=1 ORDER BY descricao_curta""", (pc_id,)) if pc_id else []
            if prods_n:
                pv_opts = [(None,"— sem vínculo —")] + list(prods_n)
                pv_sel  = st.selectbox(
                    "Vincular ao produto próprio",
                    pv_opts,
                    format_func=lambda x: x[1] if x[0] is None
                                else f"{x[1]} ({x[2]})",
                    key=f"{k}_vinc")
                prod_vinc_id = pv_sel[0] if pv_sel else None

        obs = st.text_input("Observação (opcional)", key=f"{k}_obs",
                            placeholder="Ex: produto em destaque no fim do corredor")

        if st.button(f"💾 Salvar e próximo EAN",
                     type="primary", use_container_width=True,
                     key=f"{k}_salvar"):'''

NEW_VINC = '''        # Vínculo com produto próprio (só para concorrentes)
        prod_vinc_id = None
        if tipo == "conc":
            prods_n = query("""SELECT produto_id, descricao_curta, codigo_produto
                FROM produto WHERE fornecedor_id=(
                    SELECT conc.fornecedor_id FROM produto_concorrente pc
                    JOIN concorrente conc ON pc.concorrente_id=conc.concorrente_id
                    WHERE pc.produto_concorrente_id=?
                ) AND ativo=1 ORDER BY descricao_curta""", (pc_id,)) if pc_id else []
            if prods_n:
                pv_opts = [(None,"— sem vínculo —")] + list(prods_n)
                pv_sel  = st.selectbox(
                    "Vincular ao produto próprio",
                    pv_opts,
                    format_func=lambda x: x[1] if x[0] is None
                                else f"{x[1]} ({x[2]})",
                    key=f"{k}_vinc")
                prod_vinc_id = pv_sel[0] if pv_sel else None

        obs = st.text_input("Observação (opcional)", key=f"{k}_obs",
                            placeholder="Ex: produto em destaque no fim do corredor")

        _salvar = st.form_submit_button(
            f"💾 Salvar e próximo",
            type="primary", use_container_width=True)

        if _salvar:'''

if OLD_VINC in src:
    src = src.replace(OLD_VINC, NEW_VINC, 1)
    print("✅ Fix 4: botao -> form_submit_button")
else:
    print("⚠️  Fix 4: padrão não encontrado")

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("Arquivo salvo")
