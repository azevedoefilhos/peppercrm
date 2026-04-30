#!/usr/bin/env python3
import pathlib

CAMINHO = pathlib.Path("relatorios.py")
src = CAMINHO.read_text(encoding="utf-8")

ANTIGO = '''        ORDER BY pcr.tipo_relacao ASC,
                 CASE WHEN ultimo_preco IS NULL THEN 1 ELSE 0 END,
                 ultimo_preco ASC'''

NOVO = '''        ORDER BY pcr.tipo_relacao ASC,
                 CASE WHEN (SELECT ppi2.preco FROM pesquisa_preco_item ppi2
                            JOIN pesquisa_preco pp2 ON ppi2.pesquisa_id=pp2.pesquisa_id
                            WHERE ppi2.produto_concorrente_id=pc.produto_concorrente_id
                              AND pp2.status='finalizado' AND ppi2.preco IS NOT NULL
                            ORDER BY pp2.data_pesquisa DESC LIMIT 1) IS NULL THEN 1 ELSE 0 END,
                 (SELECT ppi2.preco FROM pesquisa_preco_item ppi2
                  JOIN pesquisa_preco pp2 ON ppi2.pesquisa_id=pp2.pesquisa_id
                  WHERE ppi2.produto_concorrente_id=pc.produto_concorrente_id
                    AND pp2.status='finalizado' AND ppi2.preco IS NOT NULL
                  ORDER BY pp2.data_pesquisa DESC LIMIT 1) ASC'''

if ANTIGO in src:
    src2 = src.replace(ANTIGO, NOVO, 1)
    CAMINHO.write_text(src2, encoding="utf-8")
    print("✅ Corrigido")
else:
    print("⚠️  Padrão não encontrado")
