#!/usr/bin/env python3
import pathlib
src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
lines = src.splitlines()
# Ver _coleta_modo_classico linha 3602
for i in range(3601, 3680):
    print(i+1, lines[i][:90].encode('ascii','replace').decode())
