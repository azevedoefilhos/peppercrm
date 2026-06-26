# verificar_pdv.py
from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0, '.')
from database import query

r = query("SELECT * FROM pdv LIMIT 1")
if r:
    print("pdv colunas:", list(r[0].keys()) if hasattr(r[0], 'keys') else "sem keys")
    print("exemplo:", r[0][:8])

tipos = query("SELECT DISTINCT tipo_pdv FROM pdv WHERE tipo_pdv IS NOT NULL ORDER BY tipo_pdv")
print("tipos_pdv:", [t[0] for t in (tipos or [])])

# Relação pdv-cliente
r2 = query("""SELECT p.pdv_id, p.tipo_pdv, p.nome_fantasia, p.cliente_id
    FROM pdv p LIMIT 3""")
for row in (r2 or []):
    print(f"  pdv_id={row[0]} tipo={row[1]} nome={row[2]} cliente_id={row[3]}")
