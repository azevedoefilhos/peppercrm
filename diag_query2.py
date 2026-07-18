from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0, '.')
from database import query

print("=== Teste 1: so usuario ===")
r = query("SELECT usuario_id, nome, tipo FROM usuario WHERE empresa_id=%s", (1,))
print("Resultado:", r)

print("\n=== Teste 2: usuario + vendedor LEFT JOIN ===")
r2 = query("""SELECT u.usuario_id, u.nome, v.vendedor_id
    FROM usuario u
    LEFT JOIN vendedor v ON v.usuario_id=u.usuario_id
    WHERE u.empresa_id=%s""", (1,))
print("Resultado:", r2)

print("\n=== RLS em vendedor ===")
from database import _pg_connect
conn = _pg_connect(); conn.autocommit = True; cur = conn.cursor()
cur.execute("SELECT tablename, rowsecurity FROM pg_tables WHERE tablename='vendedor'")
print("vendedor RLS:", cur.fetchone())
cur.execute("SELECT policyname FROM pg_policies WHERE tablename='vendedor'")
print("policies:", cur.fetchall())
cur.close(); conn.close()
