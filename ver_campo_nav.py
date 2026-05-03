#!/usr/bin/env python3
import pathlib
src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
lines = src.splitlines()
for i, l in enumerate(lines, 1):
    if 'def _campo_navegacao' in l:
        for j in range(i-1, min(i+60, len(lines))):
            print(j+1, lines[j][:85].encode('ascii','replace').decode())
        break
