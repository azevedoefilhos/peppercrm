#!/usr/bin/env python3
import pathlib

src = pathlib.Path("cadastros.py").read_text(encoding="utf-8")
lines = src.splitlines()

# Mostra as linhas exatas que precisam ser corrigidas
print("=== Linha do cli_novo_opts ===")
for i, l in enumerate(lines, 1):
    if 'cli_novo_opts' in l or 'cli_novo_idx' in l or 'pdv_cli_novo' in l:
        if 2555 < i < 2590:
            print(i, repr(l[:90]))

print("\n=== Linha do form editar ===")
for i, l in enumerate(lines, 1):
    if 'pdv_excluir_id' in l or '_form_editar_pdv' in l:
        if 2545 < i < 2565:
            print(i, repr(l[:90]))

print("\n=== INSERT VALUES ===")
for i, l in enumerate(lines, 1):
    if 'VALUES' in l and '?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?' in l:
        if 2650 < i < 2680:
            print(i, repr(l[:90]))
