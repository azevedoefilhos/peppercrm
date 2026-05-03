#!/usr/bin/env python3
import pathlib
src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
lines = src.splitlines()
for i, l in enumerate(lines, 1):
    if 'where_ex' in l or 'val_ex' in l or 'existente' in l:
        if 1455 < i < 1495:
            print(i, lines[i-1][:85].encode('ascii','replace').decode())
