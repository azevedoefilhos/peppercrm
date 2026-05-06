#!/usr/bin/env python3
import pathlib
src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
lines = src.splitlines()
for i, l in enumerate(lines, 1):
    if 'def _bloco_coleta_produto' in l:
        print(f"Encontrado na linha {i}")
        for j in range(i-1, min(i+60, len(lines))):
            print(j+1, lines[j][:90].encode('ascii','replace').decode())
        break
