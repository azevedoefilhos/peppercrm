#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

# Fix 1: Passar fil_cat na chamada
OLD1 = "    elif a==\"cat\": _ac_por_categoria(where_base, params_base, fil_forn[0])"
NEW1 = "    elif a==\"cat\": _ac_por_categoria(where_base, params_base, fil_forn[0], fil_cat)"

if OLD1 in src:
    src = src.replace(OLD1, NEW1, 1)
    print("OK Fix 1")
else:
    print("NAO Fix 1")

# Fix 2: Na funcao, usar fil_cat se ja selecionada e nao mostrar selectbox
OLD2 = '''def _ac_por_categoria(where_base, params_base, forn_id_global):
    st.subheader("Comparativo por categoria")
    st.caption("Share de presenca e posicionamento de preco por marca dentro da categoria.")

    if forn_id_global:
        cats = query("""SELECT DISTINCT cat.categoria_id, cat.nome_categoria
            FROM produto p JOIN categoria cat ON p.categoria_id=cat.categoria_id
            WHERE p.fornecedor_id=? AND p.ativo=1 AND cat.ativo=1
            ORDER BY cat.nome_categoria""", (forn_id_global,))
    else:
        cats = cache_categorias()
    if not cats:
        st.info("Nenhuma categoria encontrada."); return

    cat_sel = st.selectbox("Categoria", cats, format_func=lambda x: x[1], key="ac_c_cat")'''

NEW2 = '''def _ac_por_categoria(where_base, params_base, forn_id_global, fil_cat_global=None):
    st.subheader("Comparativo por categoria")
    st.caption("Share de presenca e posicionamento de preco por marca dentro da categoria.")

    # Se ja ha categoria selecionada no filtro global, usa ela diretamente
    if fil_cat_global and fil_cat_global[0]:
        cat_sel = fil_cat_global
        st.info(f"Categoria: **{fil_cat_global[1]}** (selecionada no filtro global)")
    else:
        if forn_id_global:
            cats = query("""SELECT DISTINCT cat.categoria_id, cat.nome_categoria
                FROM produto p JOIN categoria cat ON p.categoria_id=cat.categoria_id
                WHERE p.fornecedor_id=? AND p.ativo=1 AND cat.ativo=1
                ORDER BY cat.nome_categoria""", (forn_id_global,))
        else:
            cats = cache_categorias()
        if not cats:
            st.info("Nenhuma categoria encontrada."); return
        cat_sel = st.selectbox("Categoria", cats, format_func=lambda x: x[1], key="ac_c_cat")'''

if OLD2 in src:
    src = src.replace(OLD2, NEW2, 1)
    print("OK Fix 2")
else:
    print("NAO Fix 2")

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("Salvo")
