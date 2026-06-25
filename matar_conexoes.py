# matar_conexoes.py
from dotenv import load_dotenv
load_dotenv()
import sys
sys.path.insert(0, '.')
from database import _pg_connect

conn = _pg_connect()
conn.autocommit = True
cur = conn.cursor()

print("=== Conexões ativas ===")
cur.execute("""
    SELECT pid, state, query_start, left(query, 60) as query
    FROM pg_stat_activity
    WHERE datname = current_database()
    AND pid != pg_backend_pid()
    ORDER BY query_start
""")
rows = cur.fetchall()
for r in rows:
    print(f"  pid={r[0]} state={r[1]} query={r[3]}")

print(f"\n=== Matando {len(rows)} conexões pendentes ===")
cur.execute("""
    SELECT pg_terminate_backend(pid)
    FROM pg_stat_activity
    WHERE datname = current_database()
    AND pid != pg_backend_pid()
    AND state != 'active'
""")
print(f"✅ Conexões idle terminadas")

cur.execute("""
    SELECT pg_cancel_backend(pid)
    FROM pg_stat_activity
    WHERE datname = current_database()
    AND pid != pg_backend_pid()
""")
print(f"✅ Queries canceladas")

cur.close()
conn.close()
print("OK")
