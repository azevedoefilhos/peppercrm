# ver_usuario.py
from dotenv import load_dotenv
load_dotenv()
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import _pg_connect, query

conn = _pg_connect()
cur = conn.cursor()

print("=== Estrutura da tabela usuario ===")
cur.execute("""
    SELECT column_name, data_type, character_maximum_length
    FROM information_schema.columns
    WHERE table_name = 'usuario'
    ORDER BY ordinal_position
""")
for r in cur.fetchall():
    print(f"  {r[0]} — {r[1]}")

print("\n=== Dados existentes ===")
cur.execute("SELECT * FROM usuario LIMIT 5")
rows = cur.fetchall()
if rows:
    for r in rows:
        print(f"  {r}")
else:
    print("  (vazia)")

cur.close()
conn.close()
