#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

OLD = '''    # Se ja ha categoria selecionada no filtro global, usa ela diretamente
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

NEW = '''    # Usa categoria do filtro global - nao exibe segundo seletor
    if fil_cat_global and fil_cat_global[0]:
        cat_sel = fil_cat_global
    else:
        st.warning("⚠️ Selecione uma **Categoria** no filtro acima para ver o comparativo.")
        return'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("OK")
else:
    print("NAO ENCONTRADO")
