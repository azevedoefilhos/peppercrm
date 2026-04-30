#!/usr/bin/env python3
import pathlib

CAMINHO = pathlib.Path("comissoes.py")
src = CAMINHO.read_text(encoding="utf-8")
original = src

fixes = [
    # Linha 193 - _tela_por_pedido
    (
        "        GROUP BY p.pedido_id\n        ORDER BY p.data_pedido DESC\n    \"\"\", tuple(params))\n=== Linha 325",
        None  # marcador falso, usar substituicoes separadas
    ),
]

# Fix 1: linha 193
old1 = "        GROUP BY p.pedido_id\n        ORDER BY p.data_pedido DESC\n    \"\"\", tuple(params))\n\n    if not dados:"
new1 = "        GROUP BY p.pedido_id, p.data_pedido, cli.nome_fantasia, f.nome_fantasia, p.status_pedido, p.comissao_percentual, p.desconto_geral, cpag.status_pagamento, cpag.valor_pago, com.percentual\n        ORDER BY p.data_pedido DESC\n    \"\"\", tuple(params))\n\n    if not dados:"

if old1 in src:
    src = src.replace(old1, new1, 1)
    print("✅ Fix 1: GROUP BY linha 193")
else:
    # Tentativa mais simples
    src = src.replace(
        "        GROUP BY p.pedido_id\n        ORDER BY p.data_pedido DESC",
        "        GROUP BY p.pedido_id, p.data_pedido, cli.nome_fantasia, f.nome_fantasia, p.status_pedido, p.comissao_percentual, p.desconto_geral, cpag.status_pagamento, cpag.valor_pago, com.percentual\n        ORDER BY p.data_pedido DESC",
        1
    )
    print("✅ Fix 1 (simples): GROUP BY linha 193")

# Fix 2: linha 325 (segunda ocorrencia de GROUP BY p.pedido_id)
old2 = "        GROUP BY p.pedido_id\n        ORDER BY p.data_pedido DESC\n    \"\"\", tuple(params))\n\n    if not pedidos:"
new2 = "        GROUP BY p.pedido_id, p.data_pedido, cli.nome_fantasia, f.nome_fantasia, p.comissao_percentual, p.desconto_geral, cpag.valor_pago, cpag.data_pagamento, cpag.status_pagamento, cpag.observacao, com.percentual\n        ORDER BY p.data_pedido DESC\n    \"\"\", tuple(params))\n\n    if not pedidos:"

if old2 in src:
    src = src.replace(old2, new2, 1)
    print("✅ Fix 2: GROUP BY linha 325")
else:
    # Substitui segunda ocorrência
    count = src.count("        GROUP BY p.pedido_id\n        ORDER BY p.data_pedido DESC")
    if count >= 1:
        # Já foi substituída a primeira, substitui o que sobrou
        src = src.replace(
            "        GROUP BY p.pedido_id\n        ORDER BY p.data_pedido DESC",
            "        GROUP BY p.pedido_id, p.data_pedido, cli.nome_fantasia, f.nome_fantasia, p.comissao_percentual, p.desconto_geral, cpag.valor_pago, cpag.data_pagamento, cpag.status_pagamento, cpag.observacao, com.percentual\n        ORDER BY p.data_pedido DESC",
            1
        )
        print("✅ Fix 2 (simples): GROUP BY linha 325")
    else:
        print("⚠️  Fix 2 não encontrado")

# Fix 3: linha 491 - por fornecedor
src = src.replace(
    "        GROUP BY f.fornecedor_id\n        ORDER BY previsto DESC",
    "        GROUP BY f.fornecedor_id, f.nome_fantasia, p.comissao_percentual, com.percentual\n        ORDER BY previsto DESC"
)
print("✅ Fix 3: GROUP BY linha 491")

CAMINHO.write_text(src, encoding="utf-8")
print(f"Alterado: {src != original}")
