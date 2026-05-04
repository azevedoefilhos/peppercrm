#!/usr/bin/env python3
import pathlib
src = pathlib.Path("cadastros.py").read_text(encoding="utf-8")
lines = src.splitlines()

# Ver _tela_pdvs (linhas 2367-2430)
print("=== _tela_pdvs ===")
for i in range(2366, 2430):
    print(i+1, lines[i][:90].encode('ascii','replace').decode())

print("\n=== _form_novo_pdv ===")
for i in range(2570, 2640):
    print(i+1, lines[i][:90].encode('ascii','replace').decode())
