from dotenv import load_dotenv; load_dotenv()
from database import conectar, _check_supabase

print('Supabase/PG?', _check_supabase())
conn = conectar()
print('Conn type:', type(conn).__name__)

try:
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO despesa (data_despesa, categoria, valor, ativo) "
        "VALUES (%s,%s,%s,%s) RETURNING despesa_id",
        ('2026-05-29', 'Estacionamento', 24.00, True)
    )
    print('Inserted ID:', cur.fetchone())
    conn.commit()
    conn.close()
    print('✅ OK - salvou no PostgreSQL')
except Exception as e:
    print(f'❌ Erro: {e}')
    try:
        conn.rollback()
        conn.close()
    except:
        pass
