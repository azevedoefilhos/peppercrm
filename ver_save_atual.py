#!/usr/bin/env python3
import pathlib
src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
lines = src.splitlines()
# Encontra _salvar
for i, l in enumerate(lines, 1):
    if 'if _salvar:' in l:
        for j in range(i-1, min(i+55, len(lines))):
            print(j+1, lines[j][:90].encode('ascii','replace').decode())
        break
