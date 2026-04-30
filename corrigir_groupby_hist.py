#!/usr/bin/env python3
import pathlib, sys

CAMINHO = pathlib.Path("pesquisa.py")
texto = CAMINHO.read_text(encoding="utf-8")

ANTIGO = "                    GROUP BY pp.pesquisa_id\n                    ORDER BY pp.data_pesquisa DESC\n                    LIMIT 12"
NOVO   = "                    GROUP BY pp.pesquisa_id, pp.data_pesquisa, pi_n.preco\n                    ORDER BY pp.data_pesquisa DESC\n                    LIMIT 12"

if ANTIGO in texto:
    novo = texto.replace(ANTIGO, NOVO, 1)
    CAMINHO.write_text(novo, encoding="utf-8")
    print("✅ GROUP BY historico corrigido.")
else:
    print("⚠️  Padrão não encontrado.")
