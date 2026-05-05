#!/usr/bin/env python3
import pathlib
src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
lines = src.splitlines()
for i in range(3380, 3445):
    print(i+1, lines[i][:90].encode('ascii','replace').decode())
