#!/usr/bin/env python3
import pathlib

lines = pathlib.Path("pesquisa.py").read_text(encoding="utf-8").splitlines()

novo_onsave = [
    '                    on_save((preco or None, 1 if em_oferta else 0,',
    '                             frentes or None, 1 if ruptura else 0,',
    '                             1 if pe else 0, tpe if pe else None, obs or None,',
    '                             unidade_coleta, peso_coleta, preco_kg))',
]

# Fix primeira instancia (linhas 2321-2323, indices 2320-2322)
lines = lines[:2320] + novo_onsave + lines[2323:]
print("OK Fix 1: on_save primeira instancia")

# Fix segunda instancia (agora deslocada por +1 linha)
# Encontra novamente
for i, l in enumerate(lines):
    if i > 4200 and 'on_save((preco or None' in l:
        start = i
        end = i + 3
        lines = lines[:start] + novo_onsave + lines[end:]
        print(f"OK Fix 2: on_save segunda instancia (linha {i+1})")
        break

pathlib.Path("pesquisa.py").write_text('\n'.join(lines), encoding="utf-8")
print("Salvo!")
