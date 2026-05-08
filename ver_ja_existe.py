#!/usr/bin/env python3
import pathlib
lines = pathlib.Path("pesquisa.py").read_text(encoding="utf-8").splitlines()
for i in range(1382, 1425):
    print(i+1, lines[i][:90].encode('ascii','replace').decode())
