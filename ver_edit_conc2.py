#!/usr/bin/env python3
import pathlib
src = pathlib.Path("concorrentes.py").read_text(encoding="utf-8")
lines = src.splitlines()

# Procura "EAN" em text_input no form de edicao
for i, l in enumerate(lines, 1):
    if 'EAN' in l and 'text_input' in l:
        print(f"\n=== Linha {i} ===")
        for j in range(max(0,i-3), min(i+8, len(lines))):
            print(j+1, lines[j][:85].encode('ascii','replace').decode())
