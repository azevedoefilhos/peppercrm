import sqlite3, os
DB = os.path.join(os.path.dirname(__file__), "peppercrm.db")
conn = sqlite3.connect(DB)

print("=== TABELA LINHA (todas) ===")
rows = conn.execute("SELECT linha_id, nome_linha, categoria_id, ativo FROM linha ORDER BY nome_linha").fetchall()
for r in rows:
    print(f"  id={r[0]} nome='{r[1]}' cat_id={r[2]} ativo={r[3]}")

print(f"\nTotal: {len(rows)} linhas")
conn.close()
input("\nEnter para fechar...")
