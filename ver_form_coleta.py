#!/usr/bin/env python3
import pathlib
src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
lines = src.splitlines()
# Ver _form_coleta_rapida_ean
for i, l in enumerate(lines, 1):
    if 'def _form_coleta_rapida_ean' in l:
        for j in range(i-1, min(i+80, len(lines))):
            print(j+1, lines[j][:85].encode('ascii','replace').decode())
        break
