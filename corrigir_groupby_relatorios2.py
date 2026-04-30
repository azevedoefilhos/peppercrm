#!/usr/bin/env python3
"""Corrige GROUP BY em relatorios.py adicionando colunas nao-agregadas."""
import pathlib, re

CAMINHO = pathlib.Path("relatorios.py")
src = CAMINHO.read_text(encoding="utf-8")
original = src
count = 0

substituicoes = [
    # linha 204: GROUP BY f.fornecedor_id — contexto: SELECT f.nome_fantasia
    ("        GROUP BY f.fornecedor_id\n        ORDER BY caixas DESC",
     "        GROUP BY f.fornecedor_id, f.nome_fantasia\n        ORDER BY caixas DESC"),

    # linha 320: GROUP BY cat.categoria_id, f.fornecedor_id
    ("        GROUP BY cat.categoria_id, f.fornecedor_id\n",
     "        GROUP BY cat.categoria_id, cat.nome_categoria, f.fornecedor_id, f.nome_fantasia\n"),

    # linha 378: GROUP BY mes, f.fornecedor_id
    ("        GROUP BY mes, f.fornecedor_id\n",
     "        GROUP BY mes, f.fornecedor_id, f.nome_fantasia\n"),

    # linha 561: GROUP BY c.cliente_id
    ("        GROUP BY c.cliente_id\n        ORDER BY total DESC\n        LIMIT",
     "        GROUP BY c.cliente_id, c.nome_fantasia\n        ORDER BY total DESC\n        LIMIT"),

    # linha 634: GROUP BY p.cliente_id, COALESCE(p.pdv_id, 0)
    ("        GROUP BY p.cliente_id, COALESCE(p.pdv_id, 0)\n",
     "        GROUP BY p.cliente_id, c.nome_fantasia, p.pdv_id, COALESCE(p.pdv_id, 0), pdv.nome_loja, pdv.numero_loja, pdv.cidade\n"),

    # linha 711: GROUP BY pdv.cluster, pdv.tamanho_pdv
    ("        GROUP BY pdv.cluster, pdv.tamanho_pdv\n",
     "        GROUP BY pdv.cluster, pdv.tamanho_pdv, f.nome_fantasia\n"),

    # linha 885: GROUP BY c.cliente_id
    ("        GROUP BY c.cliente_id\n        ORDER BY dias_sem_contato DESC",
     "        GROUP BY c.cliente_id, c.nome_fantasia, c.cidade, c.estado\n        ORDER BY dias_sem_contato DESC"),
]

for old, new in substituicoes:
    if old in src:
        src = src.replace(old, new, 1)
        count += 1
        print(f"✅ {old[:60].strip()}")
    else:
        print(f"⚠️  Nao encontrado: {old[:60].strip()}")

CAMINHO.write_text(src, encoding="utf-8")
print(f"\nTotal corrigidos: {count}")
