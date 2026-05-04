#!/usr/bin/env python3
import pathlib
src = pathlib.Path("concorrentes.py").read_text(encoding="utf-8")
lines = src.splitlines()
for i in range(665, 710):
    print(i+1, lines[i][:90].encode('ascii','replace').decode())
