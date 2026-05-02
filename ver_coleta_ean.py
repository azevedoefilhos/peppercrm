#!/usr/bin/env python3
import pathlib
src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
lines = src.splitlines()

# Ver a funcao _coleta_ean_produto_encontrado completa
start = None
for i, l in enumerate(lines, 1):
    if 'def _coleta_ean_produto_encontrado' in l:
        start = i
        break

if start:
    for i in range(start-1, min(start+40, len(lines))):
        print(i+1, lines[i][:85])
