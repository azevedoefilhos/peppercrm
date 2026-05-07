#!/usr/bin/env python3
import pathlib
src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
lines = src.splitlines()

print("=== MODO RAPIDO (segunda instancia) ===")
for i in range(3319, 3380):
    print(i+1, lines[i][:90].encode('ascii','replace').decode())

print("\n=== MODO CLASSICO ===")
for i in range(2269, 2320):
    print(i+1, lines[i][:90].encode('ascii','replace').decode())
