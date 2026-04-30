#!/usr/bin/env python3
import pathlib

CAMINHO = pathlib.Path("pesquisa.py")
src = CAMINHO.read_text(encoding="utf-8")

fixes = [
    (
        "        GROUP BY pp.pdv_id, ppi.produto_concorrente_id\n        ORDER BY marca, preco_medio",
        "        GROUP BY pp.pdv_id, ppi.produto_concorrente_id, cli.nome_fantasia, pdv.nome_loja, pdv.tipo_pdv, conc.marca_concorrente, pc.descricao_curta, rel.tipo_relacao\n        ORDER BY marca, preco_medio"
    ),
    (
        "        GROUP BY conc.concorrente_id\n",
        "        GROUP BY conc.concorrente_id, conc.marca_concorrente\n"
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
print(f"Total: {count}")
