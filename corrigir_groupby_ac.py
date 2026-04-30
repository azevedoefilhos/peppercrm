#!/usr/bin/env python3
import pathlib, re

CAMINHO = pathlib.Path("analise_competitiva.py")
src = CAMINHO.read_text(encoding="utf-8")
original = src

fixes = [
    # 197: GROUP BY pc.produto_concorrente_id + ORDER BY ... conc.marca_concorrente
    (
        "        GROUP BY pc.produto_concorrente_id\n        ORDER BY pdvs_presentes DESC, conc.marca_concorrente",
        "        GROUP BY pc.produto_concorrente_id, conc.marca_concorrente, pc.descricao_curta, pc.descricao\n        ORDER BY pdvs_presentes DESC, conc.marca_concorrente"
    ),
    # 246: GROUP BY conc.concorrente_id
    (
        "        GROUP BY conc.concorrente_id\n        ORDER BY pdvs_presentes DESC\n    \"\"\", (forn_id,))",
        "        GROUP BY conc.concorrente_id, conc.marca_concorrente\n        ORDER BY pdvs_presentes DESC\n    \"\"\", (forn_id,))"
    ),
    # 392: GROUP BY rel.produto_concorrente_id
    (
        "        GROUP BY rel.produto_concorrente_id\n        ORDER BY rel.tipo_relacao, pdvs_conc DESC",
        "        GROUP BY rel.produto_concorrente_id, rel.tipo_relacao, conc.marca_concorrente, pc.descricao_curta\n        ORDER BY rel.tipo_relacao, pdvs_conc DESC"
    ),
    # 438: GROUP BY ppi.produto_concorrente_id + ORDER BY media_frentes
    (
        "        GROUP BY ppi.produto_concorrente_id\n        ORDER BY media_frentes DESC",
        "        GROUP BY ppi.produto_concorrente_id, conc.marca_concorrente, pc.descricao_curta\n        ORDER BY media_frentes DESC"
    ),
    # 472: GROUP BY ppi.produto_concorrente_id + ORDER BY pct
    (
        "        GROUP BY ppi.produto_concorrente_id\n        ORDER BY pct DESC",
        "        GROUP BY ppi.produto_concorrente_id, conc.marca_concorrente, pc.descricao_curta\n        ORDER BY pct DESC"
    ),
    # 536: GROUP BY COALESCE(pp.pdv_id, pp.cliente_id) - falta cast
    (
        "        GROUP BY COALESCE(pp.pdv_id, pp.cliente_id), p.produto_id, pc.produto_concorrente_id",
        "        GROUP BY COALESCE(pp.pdv_id::TEXT, pp.cliente_id::TEXT), p.produto_id, pc.produto_concorrente_id, p.descricao_curta, conc.marca_concorrente, pc.descricao_curta, pdv.nome_loja, cli.nome_fantasia, pdv.cidade, cli.cidade"
    ),
    # 571: GROUP BY COALESCE pdv - adicionar colunas
    (
        "        GROUP BY COALESCE(pp.pdv_id::TEXT, pp.cliente_id::TEXT||'c')\n        ORDER BY marcas_concorrentes DESC, produtos_concorrentes DESC",
        "        GROUP BY COALESCE(pp.pdv_id::TEXT, pp.cliente_id::TEXT||'c'), pdv.nome_loja, cli.nome_fantasia, pdv.cidade, cli.cidade\n        ORDER BY marcas_concorrentes DESC, produtos_concorrentes DESC"
    ),
    # 630: GROUP BY conc.concorrente_id + HAVING
    (
        "        GROUP BY conc.concorrente_id\n        HAVING pdvs_presentes > 0",
        "        GROUP BY conc.concorrente_id, conc.marca_concorrente\n        HAVING COUNT(DISTINCT COALESCE(pp.pdv_id::TEXT, pp.cliente_id::TEXT||'c')) > 0"
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
print(f"\nTotal: {count} corrigidos")
