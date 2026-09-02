from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0,'.')
from database import _pg_connect

conn = _pg_connect()
conn.autocommit = False
cur = conn.cursor()

try:
    print("=== Etapa 2: promotor_id em roteiro_item ===\n")

    # 1. Adiciona coluna promotor_id em roteiro_item
    cur.execute("""SELECT COUNT(*) FROM information_schema.columns
        WHERE table_name='roteiro_item' AND column_name='promotor_id'""")
    if cur.fetchone()[0] == 0:
        cur.execute("""ALTER TABLE roteiro_item
            ADD COLUMN promotor_id INTEGER REFERENCES promotor(promotor_id)""")
        print("OK: promotor_id adicionado em roteiro_item")
    else:
        print("-- promotor_id ja existe")

    # 2. Torna usuario_id opcional (NULL permitido)
    cur.execute("""ALTER TABLE roteiro_item
        ALTER COLUMN usuario_id DROP NOT NULL""")
    print("OK: usuario_id agora opcional em roteiro_item")

    # 3. Remove UNIQUE constraint antiga e recria com ambos os campos
    cur.execute("""SELECT constraint_name FROM information_schema.table_constraints
        WHERE table_name='roteiro_item' AND constraint_type='UNIQUE'""")
    constraints = [r[0] for r in cur.fetchall()]
    for cn in constraints:
        cur.execute(f"ALTER TABLE roteiro_item DROP CONSTRAINT IF EXISTS {cn}")
        print(f"OK: constraint {cn} removida")

    # 4. Adiciona nova UNIQUE que aceita usuario_id OU promotor_id
    cur.execute("""ALTER TABLE roteiro_item
        ADD CONSTRAINT roteiro_item_unique_vend
        UNIQUE NULLS NOT DISTINCT (tipo_roteiro, usuario_id, pdv_id, dia_semana, turno)""")
    cur.execute("""ALTER TABLE roteiro_item
        ADD CONSTRAINT roteiro_item_unique_prom
        UNIQUE NULLS NOT DISTINCT (tipo_roteiro, promotor_id, pdv_id, dia_semana, turno)""")
    print("OK: constraints UNIQUE separadas para usuario e promotor")

    # 5. CHECK: usuario_id XOR promotor_id
    cur.execute("""ALTER TABLE roteiro_item
        DROP CONSTRAINT IF EXISTS roteiro_item_xor_check""")
    cur.execute("""ALTER TABLE roteiro_item
        ADD CONSTRAINT roteiro_item_xor_check CHECK (
            (usuario_id IS NOT NULL AND promotor_id IS NULL) OR
            (usuario_id IS NULL AND promotor_id IS NOT NULL)
        )""")
    print("OK: CHECK XOR usuario_id/promotor_id adicionado")

    # 6. Atualiza tipo_roteiro CHECK para incluir supervisor
    cur.execute("""ALTER TABLE roteiro_item
        DROP CONSTRAINT IF EXISTS roteiro_item_tipo_roteiro_check""")
    cur.execute("""ALTER TABLE roteiro_item
        ADD CONSTRAINT roteiro_item_tipo_roteiro_check
        CHECK(tipo_roteiro IN ('vendedor','promotor','supervisor'))""")
    print("OK: tipo_roteiro CHECK atualizado")

    conn.commit()
    print("\n✅ Etapa 2 concluída!")

    # Verifica estrutura final
    cur.execute("""SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name='roteiro_item'
        ORDER BY ordinal_position""")
    print("\n=== Estrutura roteiro_item ===")
    for r in cur.fetchall():
        print(f"  {r[0]} ({r[1]}) nullable={r[2]}")

except Exception as e:
    conn.rollback()
    print(f"\nERRO: {e}")
    import traceback; traceback.print_exc()
finally:
    cur.close()
    conn.close()
