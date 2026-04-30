#!/usr/bin/env python3
import pathlib

CAMINHO = pathlib.Path("comissoes.py")
src = CAMINHO.read_text(encoding="utf-8")

# Linha 518: "Diferen?a (R$)" deve ser "Diferenca (R$)" para bater com linha 511
# Verifica o que existe
for i, l in enumerate(src.splitlines()[508:522], 509):
    if 'iferen' in l:
        print(f"Linha {i}: {repr(l)}")

# Substitui qualquer variacao de "Diferenca" ou "Diferença" no for col de formatacao
import re
src2 = re.sub(
    r'"Diferen[^\"]+(R\$\)")',
    '"Diferenca (R$)"',
    src
)

if src2 != src:
    CAMINHO.write_text(src2, encoding="utf-8")
    print("OK")
else:
    # Tenta substituicao direta
    for variante in ['Diferen\u00e7a (R$)', 'Diferen?a (R$)', 'Diferenca (R$)']:
        if variante in src:
            print(f"Encontrado: {repr(variante)}")
            break
    print("Verifique manualmente linha 518")
