#!/usr/bin/env python3
import pathlib
src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
lines = src.splitlines()
for i, l in enumerate(lines, 1):
    if ('rapido' in l.lower() or '_coleta_modo_rapido' in l) and i < 600:
        print(i, l[:85].encode('ascii','replace').decode())
