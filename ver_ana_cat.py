#!/usr/bin/env python3
import pathlib
src = pathlib.Path("analise_competitiva.py").read_text(encoding="utf-8")
lines = src.splitlines()

# Ver aba de categorias
for i, l in enumerate(lines, 1):
    if 'categoria' in l.lower() and 'selectbox' in l.lower():
        for j in range(max(0,i-2), min(i+5, len(lines))):
            print(j+1, lines[j][:90].encode('ascii','replace').decode())
        print("---")
