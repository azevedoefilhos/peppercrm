from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0, '.')
from database import _pg_connect

conn = _pg_connect()
conn.autocommit = False
cur = conn.cursor()

try:
    print("=== Adicionando subtipo em promotor ===")

    # 1. Adicionar coluna subtipo
    cur.execute("""SELECT COUNT(*) FROM information_schema.columns
        WHERE table_name='promotor' AND column_name='subtipo'""")
    if cur.fetchone()[0] == 0:
        cur.execute("ALTER TABLE promotor ADD COLUMN subtipo TEXT DEFAULT 'PROMOTOR'")
        print("OK: coluna subtipo adicionada")
    else:
        print("-- ja existe")

    # 2. Marcar "Sem promotor" com subtipo especial
    cur.execute("UPDATE promotor SET subtipo='SEM_PROMOTOR' WHERE nome='Sem promotor'")
    print("OK: 'Sem promotor' marcado como SEM_PROMOTOR")

    # 3. Vincular usuarios PROMOTOR_VENDEDOR aos seus promotores
    # Se o promotor tem usuario_id de um usuario tipo PROMOTOR_VENDEDOR -> subtipo PROMOTOR_VENDEDOR
    cur.execute("""
        UPDATE promotor p SET subtipo='PROMOTOR_VENDEDOR'
        WHERE p.usuario_id IN (
            SELECT usuario_id FROM usuario WHERE tipo='PROMOTOR_VENDEDOR'
        )
    """)
    print("OK: promotores vinculados a PROMOTOR_VENDEDOR marcados")

    conn.commit()

    # Verificacao
    cur.execute("SELECT subtipo, COUNT(*) FROM promotor GROUP BY subtipo ORDER BY subtipo")
    print("\n=== Distribuicao por subtipo ===")
    for r in cur.fetchall():
        print(f"  {r[0]}: {r[1]}")

    print("\nConcluido!")

except Exception as e:
    conn.rollback()
    print(f"ERRO: {e}")
    raise
finally:
    cur.close()
    conn.close()
