#!/usr/bin/env python3
import pathlib
src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
lines = src.splitlines()

for n, label in [(2790, "por_produto cw_base"), (2856, "por_marca cw"), (2912, "por_categoria cw")]:
    print(f"\n=== {label} (linha {n}) ===")
    for i in range(n-1, min(len(lines), n+10)):
        print(i+1, lines[i].encode('ascii','replace').decode())
