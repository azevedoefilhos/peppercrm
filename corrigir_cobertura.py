#!/usr/bin/env python3
import pathlib

CAMINHO = pathlib.Path("relatorios.py")
src = CAMINHO.read_text(encoding="utf-8")
original = src

fixes = [
    (
        "            GROUP BY c.cliente_id ORDER BY MAX(cr.data_contato) DESC\"\"\",",
        "            GROUP BY c.cliente_id, c.nome_fantasia, c.cidade, c.status, c.perfil, pdv.cluster ORDER BY MAX(cr.data_contato) DESC\"\"\","
    ),
    (
        "            GROUP BY c.cliente_id ORDER BY MAX(p.data_pedido) DESC\"\"\",",
        "            GROUP BY c.cliente_id, c.nome_fantasia, c.cidade, c.status, c.perfil, pdv.cluster ORDER BY MAX(p.data_pedido) DESC\"\"\","
    ),
    # linha 1134
    (
        "            GROUP BY c.cliente_id\n            ORDER BY MAX(cr.data_contato) DESC\"\"\",",
        "            GROUP BY c.cliente_id, c.nome_fantasia, c.cidade, c.status, pdv.tipo_pdv, pdv.cluster\n            ORDER BY MAX(cr.data_contato) DESC\"\"\","
    ),
    # linha 1148
    (
        "            GROUP BY c.cliente_id\n            ORDER BY MAX(p.data_pedido) DESC\"\"\",",
        "            GROUP BY c.cliente_id, c.nome_fantasia, c.cidade, c.status, pdv.tipo_pdv, pdv.cluster\n            ORDER BY MAX(p.data_pedido) DESC\"\"\","
    ),
]

count = 0
for old, new in fixes:
    if old in src:
        src = src.replace(old, new, 1)
        count += 1
        print(f"✅ {old[:60].strip()}")
    else:
        print(f"⚠️  Nao encontrado: {old[:60].strip()}")

CAMINHO.write_text(src, encoding="utf-8")
print(f"\nTotal: {count} corrigidos, alterado: {src != original}")
