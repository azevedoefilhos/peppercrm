from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0,'.')
from database import _pg_connect

conn = _pg_connect()
conn.autocommit = False
cur = conn.cursor()

try:
    # 1. Migra setores antigos para os novos
    print("=== Migrando setores legados ===")
    
    # 'Setor 3 - Santos Orla' -> Setor 3B (mais proximo)
    cur.execute("""UPDATE pdv SET setor_id = (
        SELECT setor_id FROM setor WHERE codigo='S3B' LIMIT 1)
        WHERE setor = 'Setor 3 - Santos Orla' AND setor_id IS NULL""")
    print(f"  Setor 3 Orla -> S3B: {cur.rowcount} PDVs")

    # 'Setor 7 - Praia Grande' -> Setor 7A
    cur.execute("""UPDATE pdv SET setor_id = (
        SELECT setor_id FROM setor WHERE codigo='S7A' LIMIT 1)
        WHERE setor = 'Setor 7 - Praia Grande' AND setor_id IS NULL""")
    print(f"  Setor 7 PG -> S7A: {cur.rowcount} PDVs")

    conn.commit()
    print("OK: migração concluída")

    # 2. Verifica resultado
    cur.execute("""SELECT s.nome, COUNT(p.pdv_id)
        FROM setor s
        LEFT JOIN pdv p ON p.setor_id=s.setor_id
        WHERE s.empresa_id=1
        GROUP BY s.setor_id, s.nome, s.codigo
        ORDER BY s.codigo""")
    print("\n=== PDVs por setor após migração ===")
    for r in cur.fetchall():
        print(f"  {r[0]}: {r[1]} PDVs")

    cur.execute("SELECT COUNT(*) FROM pdv WHERE setor_id IS NULL AND setor IS NOT NULL")
    print(f"\nPDVs com setor texto mas sem setor_id: {cur.fetchone()[0]}")

except Exception as e:
    conn.rollback()
    print(f"ERRO: {e}")
    import traceback; traceback.print_exc()
finally:
    cur.close()
    conn.close()
