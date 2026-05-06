#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

OLD = '        # Coleta por Kg\n        _col_un, _col_peso, _col_pkg = st.columns([1, 1.5, 1.5])'
NEW = '        # Coleta por Kg\n        st.write("DEBUG: chegou aqui")\n        _col_un, _col_peso, _col_pkg = st.columns([1, 1.5, 1.5])'

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("OK")
else:
    print("NAO ENCONTRADO")
