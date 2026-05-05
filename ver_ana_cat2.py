#!/usr/bin/env python3
import pathlib
src = pathlib.Path("analise_competitiva.py").read_text(encoding="utf-8")
lines = src.splitlines()

# Ver a funcao principal e os filtros globais
for i in range(60, 110):
    print(i+1, lines[i][:90].encode('ascii','replace').decode())
