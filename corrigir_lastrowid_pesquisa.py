#!/usr/bin/env python3
"""Corrige cur.lastrowid em _form_novo_concorrente_rapido usando execute_write + RETURNING."""
import pathlib, sys

CAMINHO = pathlib.Path("pesquisa.py")
texto = CAMINHO.read_text(encoding="utf-8")

ANTIGO = '''        cur = conn.cursor()
        cur.execute("""INSERT INTO produto_concorrente
            (concorrente_id, categoria_id, descricao, descricao_curta,
             peso, unidade_medida, ean_concorrente, auditavel, ativo)
            VALUES (?,?,?,?,?,?,?,?,1)""",
            (conc_id,
             cat_sel[0] if cat_sel and cat_sel[0] else None,
             desc.strip(), desc_c.strip() or None,
             peso or None, um,
             ean_conc.strip() or None,
             1 if auditavel else 0))
        pc_id_novo = cur.lastrowid
        conn.commit()'''

NOVO = '''        pc_id_novo = execute_write("""INSERT INTO produto_concorrente
            (concorrente_id, categoria_id, descricao, descricao_curta,
             peso, unidade_medida, ean_concorrente, auditavel, ativo)
            VALUES (?,?,?,?,?,?,?,?,1)
            RETURNING produto_concorrente_id""",
            (conc_id,
             cat_sel[0] if cat_sel and cat_sel[0] else None,
             desc.strip(), desc_c.strip() or None,
             peso or None, um,
             ean_conc.strip() or None,
             1 if auditavel else 0))'''

if ANTIGO in texto:
    novo = texto.replace(ANTIGO, NOVO, 1)
    CAMINHO.write_text(novo, encoding="utf-8")
    print("✅ Corrigido: execute_write com RETURNING produto_concorrente_id")
else:
    print("⚠️  Padrão não encontrado — verifique manualmente linhas 2043-2055.")
    sys.exit(1)

# Verifica import de execute_write
c = CAMINHO.read_text(encoding="utf-8")
if "execute_write" in c[:300]:
    print("✅ execute_write já importado.")
else:
    novo2 = c.replace("from database import", "from database import execute_write,", 1)
    CAMINHO.write_text(novo2, encoding="utf-8")
    print("✅ execute_write adicionado ao import.")
