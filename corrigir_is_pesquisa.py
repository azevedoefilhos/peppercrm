#!/usr/bin/env python3
"""Corrige 'IS ?' para '=?' em pesquisa.py — IS nao aceita parametros no PostgreSQL."""
import pathlib, sys

CAMINHO = pathlib.Path("pesquisa.py")
texto = CAMINHO.read_text(encoding="utf-8")

ANTIGO = '        WHERE pesquisa_id=? AND produto_id IS ? AND produto_concorrente_id IS ?""",'
NOVO   = '        WHERE pesquisa_id=? AND produto_id=? AND produto_concorrente_id=?""",'

if ANTIGO in texto:
    novo = texto.replace(ANTIGO, NOVO, 1)
    CAMINHO.write_text(novo, encoding="utf-8")
    print("✅ IS ? corrigido para =?")
else:
    # Busca mais flexível
    import re
    padrao = re.compile(r'produto_id\s+IS\s+\?')
    if padrao.search(texto):
        novo = re.sub(r'produto_id\s+IS\s+\?', 'produto_id=?', texto)
        novo = re.sub(r'produto_concorrente_id\s+IS\s+\?', 'produto_concorrente_id=?', novo)
        CAMINHO.write_text(novo, encoding="utf-8")
        print("✅ IS ? corrigido via regex")
    else:
        print("⚠️  Padrão não encontrado — verifique linha 1932")

# Verifica outros IS ? no arquivo
c = CAMINHO.read_text(encoding="utf-8")
import re
outros = [(i+1, l) for i, l in enumerate(c.splitlines()) if re.search(r'\bIS\s+\?', l)]
if outros:
    print(f"⚠️  Ainda há {len(outros)} ocorrência(s) de IS ?:")
    for n, l in outros:
        print(f"  Linha {n}: {l.strip()}")
else:
    print("✅ Nenhum outro IS ? encontrado")
