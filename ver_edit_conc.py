#!/usr/bin/env python3
import pathlib
src = pathlib.Path("concorrentes.py").read_text(encoding="utf-8")
lines = src.splitlines()

# Procura o form de edicao do produto concorrente
for i, l in enumerate(lines, 1):
    if 'def _form_editar_produto_conc' in l or 'def _form_edit_conc' in l or ('ean_concorrente' in l and 'text_input' in l):
        print(i, l[:85].encode('ascii','replace').decode())

# Ver linhas ao redor de 1442
print("\n=== Contexto linha 1440-1470 ===")
for i in range(1439, 1475):
    print(i+1, lines[i][:85].encode('ascii','replace').decode())
