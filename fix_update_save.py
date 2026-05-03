#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
lines = src.splitlines()

# Mostra linhas 1474-1525 completas
for i in range(1473, 1525):
    print(i+1, lines[i].encode('ascii','replace').decode())
