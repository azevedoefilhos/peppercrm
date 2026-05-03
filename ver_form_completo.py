#!/usr/bin/env python3
import pathlib
src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
lines = src.splitlines()
for i in range(1375, 1460):
    print(i+1, lines[i][:85].encode('ascii','replace').decode())
