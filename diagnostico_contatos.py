import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), "peppercrm.db")
conn = sqlite3.connect(DB)

print("=== TABELAS COM 'contato' ===")
tbls = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%contato%'").fetchall()
for t in tbls:
    print(f"  {t[0]}")
    cols = conn.execute(f"PRAGMA table_info({t[0]})").fetchall()
    for c in cols:
        print(f"    col {c[0]}: {c[1]} ({c[2]})")

print()
print("=== contato_x_fornecedor ===")
try:
    rows = conn.execute("SELECT * FROM contato_x_fornecedor").fetchall()
    print(f"  {len(rows)} registros")
    for r in rows:
        print(f"  {r}")
except Exception as e:
    print(f"  ERRO: {e}")

conn.close()
input("\nEnter para fechar...")
