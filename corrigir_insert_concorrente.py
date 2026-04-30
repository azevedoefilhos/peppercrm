#!/usr/bin/env python3
"""Corrige INSERT produto_concorrente: remove obs_nc dos params (nao e coluna do INSERT)."""
import pathlib, sys

CAMINHO = pathlib.Path("pesquisa.py")
texto = CAMINHO.read_text(encoding="utf-8")

ANTIGO = '''        cur.execute("""INSERT INTO produto_concorrente
            (concorrente_id, categoria_id, descricao, descricao_curta,
             peso, unidade_medida, ean_concorrente, auditavel, ativo)
            VALUES (?,?,?,?,?,?,?,?,1)""",
            (conc_id,
             cat_sel[0] if cat_sel and cat_sel[0] else None,
             desc.strip(), desc_c.strip() or None,
             peso or None, um,
             ean_conc.strip() or None,
             1 if auditavel else 0,
             obs_nc.strip() or None))'''

NOVO = '''        cur.execute("""INSERT INTO produto_concorrente
            (concorrente_id, categoria_id, descricao, descricao_curta,
             peso, unidade_medida, ean_concorrente, auditavel, ativo)
            VALUES (?,?,?,?,?,?,?,?,1)""",
            (conc_id,
             cat_sel[0] if cat_sel and cat_sel[0] else None,
             desc.strip(), desc_c.strip() or None,
             peso or None, um,
             ean_conc.strip() or None,
             1 if auditavel else 0))'''

if ANTIGO in texto:
    novo = texto.replace(ANTIGO, NOVO, 1)
    CAMINHO.write_text(novo, encoding="utf-8")
    print("✅ INSERT produto_concorrente corrigido — obs_nc removido dos params.")
else:
    print("⚠️  Padrão não encontrado — verifique manualmente linhas 2044-2054.")
