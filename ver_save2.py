#!/usr/bin/env python3
import pathlib
src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
lines = src.splitlines()
for i, l in enumerate(lines, 1):
    if 'UPDATE pesquisa_preco_item SET' in l:
        for j in range(max(0,i-5), min(i+25, len(lines))):
            print(j+1, lines[j][:85].encode('ascii','replace').decode())
        print("---")
