# d1b_verificar_banco.py
# Verifica estado atual das tabelas relevantes para o D1b
from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0, '.')
from database import _pg_connect

conn = _pg_connect()
cur = conn.cursor()

print("=== 1. Colunas da tabela usuario ===")
cur.execute("""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name='usuario' ORDER BY ordinal_position
""")
for r in cur.fetchall():
    print(f"  {r[0]} — {r[1]}")

print("\n=== 2. Tipos existentes em usuario.tipo ===")
cur.execute("SELECT DISTINCT tipo, COUNT(*) FROM usuario GROUP BY tipo")
for r in cur.fetchall():
    print(f"  '{r[0]}' — {r[1]} usuario(s)")

print("\n=== 3. Colunas da tabela cliente ===")
cur.execute("""
    SELECT column_name FROM information_schema.columns
    WHERE table_name='cliente' ORDER BY ordinal_position
""")
cols = [r[0] for r in cur.fetchall()]
print(f"  {', '.join(cols)}")
print(f"  vendedor_id existe: {'vendedor_id' in cols}")

print("\n=== 4. Colunas da tabela promotor ===")
cur.execute("""
    SELECT column_name FROM information_schema.columns
    WHERE table_name='promotor' ORDER BY ordinal_position
""")
cols = [r[0] for r in cur.fetchall()]
print(f"  {', '.join(cols)}")
print(f"  usuario_id existe: {'usuario_id' in cols}")
print(f"  supervisor_id existe: {'supervisor_id' in cols}")

print("\n=== 5. Tabela supervisor_promotor existe? ===")
cur.execute("""
    SELECT COUNT(*) FROM information_schema.tables
    WHERE table_name='supervisor_promotor'
""")
print(f"  {'SIM' if cur.fetchone()[0] else 'NAO'}")

print("\n=== 6. Tabela vendedor (para referencia) ===")
cur.execute("""
    SELECT column_name FROM information_schema.columns
    WHERE table_name='vendedor' ORDER BY ordinal_position
""")
cols = [r[0] for r in cur.fetchall()]
print(f"  {', '.join(cols)}")

print("\n=== 7. Usuarios cadastrados ===")
cur.execute("SELECT usuario_id, nome, email, tipo, empresa_id, ativo FROM usuario")
for r in cur.fetchall():
    print(f"  id={r[0]} nome={r[1]} email={r[2]} tipo={r[3]} empresa_id={r[4]} ativo={r[5]}")

cur.close()
conn.close()
print("\nOK")
