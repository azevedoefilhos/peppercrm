#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
lines = src.splitlines()

# Remove linha 2306 (index 2305) que está duplicada
del lines[2305]

pathlib.Path("pesquisa.py").write_text('\n'.join(lines), encoding="utf-8")
print("OK")
