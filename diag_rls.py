from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0, '.')
from database import _pg_connect

conn = _pg_connect()
conn.autocommit = True
cur = conn.cursor()

print("=== RLS em usuario ===")
cur.execute("SELECT tablename, rowsecurity FROM pg_tables WHERE tablename='usuario'")
print("usuario RLS:", cur.fetchone())

print("\n=== Policies em usuario ===")
cur.execute("SELECT policyname, cmd FROM pg_policies WHERE tablename='usuario'")
for r in cur.fetchall():
    print(" ", r)

print("\n=== Usuarios via conexao direta (sem RLS) ===")
cur.execute("SET app.empresa_id='1'")
cur.execute("SELECT usuario_id, nome, tipo, empresa_id FROM usuario ORDER BY nome")
for r in cur.fetchall():
    print(" ", r)

cur.close(); conn.close()
