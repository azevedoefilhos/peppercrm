#!/usr/bin/env python3
import pathlib

CAMINHO = pathlib.Path("relatorios.py")
src = CAMINHO.read_text(encoding="utf-8")

idx = src.find('_VALOR_ITEM')
print("Trecho atual:")
print(repr(src[idx:idx+150]))

# Localiza e substitui
import re
padrao = re.compile(r'_VALOR_ITEM\s*=\s*"""\s*\n\s*ROUND\(pi\.quantidade \* pi\.preco_final\s*\n\s*\* \(1 - COALESCE\(p\.desconto_geral,0\)/100\.0\), 2\)\s*\n"""')
novo = '_VALOR_ITEM = """\n    pi.quantidade * pi.preco_final\n          * (1 - COALESCE(p.desconto_geral,0)/100.0)\n"""'

if padrao.search(src):
    src2 = padrao.sub(novo, src, count=1)
    CAMINHO.write_text(src2, encoding="utf-8")
    print("OK")
else:
    # Tentativa mais simples
    old = src[idx:idx+150]
    print("Nao encontrado pelo regex — edite manualmente")
