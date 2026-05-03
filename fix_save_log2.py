#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

# Adiciona log antes do form
OLD = '    with st.form(key=f"{k}_form", border=True):'
NEW = '''    st.caption(f"DEBUG form key: {k}")
    with st.form(key=f"{k}_form", border=True):'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("OK")
else:
    print("NAO ENCONTRADO")
