#!/usr/bin/env python3
import pathlib

src = pathlib.Path("contatos.py").read_text(encoding="utf-8")
lines = src.splitlines()

# Ver linha 564
for i in range(560, 585):
    print(i+1, lines[i][:90].encode('ascii','replace').decode())
