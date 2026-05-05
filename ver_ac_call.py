#!/usr/bin/env python3
import pathlib
src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
lines = src.splitlines()
for i, l in enumerate(lines, 1):
    if '_ac_por_categoria' in l or 'cat_id_global' in l or ('categoria' in l.lower() and 'selectbox' in l and 3400 < i < 3430):
        print(i, l[:85].encode('ascii','replace').decode())
