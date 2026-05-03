#!/usr/bin/env python3
import pathlib
src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
lines = src.splitlines()
for i, l in enumerate(lines, 1):
    if '_confirmar_key' in l or '_ja_existe' in l:
        print(i, lines[i-1][:85].encode('ascii','replace').decode())
