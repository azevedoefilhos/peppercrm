# d1b_add_whatsapp_usuario.py
# Adiciona campo whatsapp na tabela usuario
from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0, '.')
from database import _pg_connect

conn = _pg_connect()
conn.autocommit = True
cur = conn.cursor()

print("Adicionando whatsapp em usuario...")
cur.execute("""
    SELECT COUNT(*) FROM information_schema.columns
    WHERE table_name='usuario' AND column_name='whatsapp'
""")
if cur.fetchone()[0] == 0:
    cur.execute("ALTER TABLE usuario ADD COLUMN whatsapp TEXT DEFAULT NULL")
    print("OK — coluna whatsapp adicionada")
else:
    print("-- ja existe")

cur.close(); conn.close()
print("Concluido!")
