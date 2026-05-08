#!/usr/bin/env python3
import pathlib
lines = pathlib.Path("pesquisa.py").read_text(encoding="utf-8").splitlines()
for i in range(1144, 1200):
    print(i+1, lines[i][:85].encode('ascii','replace').decode())
