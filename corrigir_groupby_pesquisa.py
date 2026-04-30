#!/usr/bin/env python3
"""Corrige GROUP BY na query _tela_lista de pesquisa.py"""
import pathlib, sys

CAMINHO = pathlib.Path("pesquisa.py")
if not CAMINHO.exists():
    print("ERRO: pesquisa.py nao encontrado.")
    sys.exit(1)

texto = CAMINHO.read_text(encoding="utf-8")

ANTIGO = "        GROUP BY pp.pesquisa_id\n        ORDER BY pp.data_pesquisa DESC"
NOVO   = "        GROUP BY pp.pesquisa_id, pp.data_pesquisa, cli.nome_fantasia, pdv.nome_loja, f.nome_fantasia, pp.status\n        ORDER BY pp.data_pesquisa DESC"

if ANTIGO in texto:
    novo = texto.replace(ANTIGO, NOVO, 1)
    CAMINHO.write_text(novo, encoding="utf-8")
    print("✅ GROUP BY corrigido em pesquisa.py")
else:
    print("⚠️  Padrão não encontrado — verifique manualmente a linha com GROUP BY pp.pesquisa_id")
