from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0,'.')
from database import _pg_connect

conn = _pg_connect()
cur = conn.cursor()

print("=== Estrutura supervisor_promotor ===")
cur.execute("""SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_name='supervisor_promotor'
    ORDER BY ordinal_position""")
cols = cur.fetchall()
if cols:
    for c in cols:
        print(f"  {c[0]} {c[1]} nullable={c[2]}")
else:
    print("  TABELA NAO EXISTE!")

print("\n=== Tentando INSERT direto ===")
try:
    cur.execute("""INSERT INTO supervisor_promotor
        (supervisor_id, promotor_id, ativo) VALUES (1, 2, 1)
        RETURNING supervisor_promotor_id""")
    conn.commit()
    r = cur.fetchone()
    print(f"  OK: id={r[0]}")
    # Remove o registro de teste
    cur.execute("DELETE FROM supervisor_promotor WHERE supervisor_promotor_id=%s", (r[0],))
    conn.commit()
    print("  Removido apos teste")
except Exception as e:
    conn.rollback()
    print(f"  ERRO: {e}")

cur.close()
conn.close()
