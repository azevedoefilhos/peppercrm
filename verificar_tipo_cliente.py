# verificar_tipo_cliente.py
from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0, '.')
from database import query

r = query("SELECT * FROM cliente LIMIT 1")
if r: print("Colunas:", list(r[0].keys()) if hasattr(r[0], 'keys') else "sem keys")

tipos = query("SELECT DISTINCT tipo_pdv FROM cliente WHERE tipo_pdv IS NOT NULL ORDER BY tipo_pdv LIMIT 10")
print("tipos_pdv:", [t[0] for t in (tipos or [])])

tipos2 = query("SELECT DISTINCT status FROM cliente WHERE status IS NOT NULL ORDER BY status LIMIT 10")
print("status:", [t[0] for t in (tipos2 or [])])
