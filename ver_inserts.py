#!/usr/bin/env python3
import pathlib

for arq, linhas in [("concorrentes.py", [188, 1032, 1422]), ("pesquisa.py", [1272, 2031])]:
    src = pathlib.Path(arq).read_text(encoding="utf-8")
    lines = src.splitlines()
    for n in linhas:
        print(f"\n=== {arq} linha {n} ===")
        for i in range(max(0,n-5), min(len(lines),n+10)):
            print(i+1, lines[i].encode('ascii','replace').decode())
