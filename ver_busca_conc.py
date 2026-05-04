#!/usr/bin/env python3
import pathlib
src = pathlib.Path("concorrentes.py").read_text(encoding="utf-8")
lines = src.splitlines()
for i, l in enumerate(lines, 1):
    if 'LIKE' in l and ('descricao' in l.lower() or 'marca' in l.lower()):
        for j in range(max(0,i-2), min(i+3, len(lines))):
            print(j+1, lines[j][:90].encode('ascii','replace').decode())
        print("---")
        break
