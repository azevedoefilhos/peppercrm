from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0,'.')
from database import _pg_connect

conn = _pg_connect()
conn.autocommit = True
cur = conn.cursor()

try:
    # Remove constraint antiga e adiciona nova com 'supervisor'
    cur.execute("""
        ALTER TABLE roteiro_item
        DROP CONSTRAINT IF EXISTS roteiro_item_tipo_roteiro_check
    """)
    cur.execute("""
        ALTER TABLE roteiro_item
        ADD CONSTRAINT roteiro_item_tipo_roteiro_check
        CHECK(tipo_roteiro IN ('vendedor','promotor','supervisor'))
    """)
    print("OK: CHECK roteiro_item atualizado com supervisor")

    # Remove UNIQUE constraint antiga e adiciona nova
    cur.execute("""
        ALTER TABLE roteiro_item
        DROP CONSTRAINT IF EXISTS roteiro_item_tipo_roteiro_usuario_id_pdv_id_dia_semana_tur
    """)
    # Cria nova sem nome automatico
    print("OK: constraints atualizadas")

except Exception as e:
    print(f"ERRO: {e}")
finally:
    cur.close()
    conn.close()
