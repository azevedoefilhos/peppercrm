# listar_tabelas.py
from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0, '.')
from database import _pg_connect

conn = _pg_connect()
cur = conn.cursor()
cur.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
    AND table_type = 'BASE TABLE'
    ORDER BY table_name
""")
tabelas = cur.fetchall()
print(f"Total: {len(tabelas)} tabelas\n")
for r in tabelas:
    print(r[0])
cur.close(); conn.close()
