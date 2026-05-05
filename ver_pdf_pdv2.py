#!/usr/bin/env python3
import pathlib
src = pathlib.Path("relatorios.py").read_text(encoding="utf-8")
lines = src.splitlines()
for i in range(1150, 1240):
    print(i+1, lines[i][:90].encode('ascii','replace').decode())
