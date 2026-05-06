#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
lines = src.splitlines()

# Ver linhas 2290-2330 para ver obs e save
for i in range(2289, 2330):
    print(i+1, lines[i][:90].encode('ascii','replace').decode())
