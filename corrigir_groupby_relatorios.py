#!/usr/bin/env python3
import pathlib, re

CAMINHO = pathlib.Path("relatorios.py")
src = CAMINHO.read_text(encoding="utf-8")
original = src

# Fix 1: _rel_produto GROUP BY
src = src.replace(
    "        GROUP BY pr.produto_id\n        ORDER BY caixas DESC",
    "        GROUP BY pr.produto_id, pr.codigo_produto, pr.descricao_curta, f.nome_fantasia, cat.nome_categoria\n        ORDER BY caixas DESC"
)

# Busca e corrige outros GROUP BY simples em relatorios.py
# Padrao: GROUP BY <tabela>.<coluna_id> seguido de ORDER BY
fixes = [
    ("        GROUP BY c.cliente_id, f.fornecedor_id\n        ORDER BY total DESC",
     "        GROUP BY c.cliente_id, c.nome_fantasia, f.fornecedor_id, f.nome_fantasia\n        ORDER BY total DESC"),
]
for old, new in fixes:
    if old in src:
        src = src.replace(old, new, 1)
        print(f"✅ Corrigido: {old[:50]}")

CAMINHO.write_text(src, encoding="utf-8")
print(f"Alterações: {'SIM' if src != original else 'NENHUMA'}")
