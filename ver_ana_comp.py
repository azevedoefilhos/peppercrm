#!/usr/bin/env python3
import pathlib
src = pathlib.Path("analise_competitiva.py").read_text(encoding="utf-8")
lines = src.splitlines()

# Lista todas as funcoes e subheaders
for i, l in enumerate(lines, 1):
    if 'def _' in l or 'subheader' in l or 'Categoria' in l and 'selectbox' in l:
        print(i, l[:85].encode('ascii','replace').decode())
