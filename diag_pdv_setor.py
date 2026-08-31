from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0,'.')
from database import query

print("=== PDVs com setor_id no Railway ===")
r = query("SELECT COUNT(*) FROM pdv WHERE setor_id IS NOT NULL")
print(f"  PDVs com setor_id: {r[0][0] if r else 'erro'}")

r2 = query("SELECT COUNT(*) FROM pdv WHERE setor_id IS NULL AND setor IS NOT NULL")
print(f"  PDVs com setor texto mas sem setor_id: {r2[0][0] if r2 else 'erro'}")

print("\n=== Amostra de PDVs com setor ===")
r3 = query("SELECT pdv_id, nome_loja, setor, setor_id FROM pdv WHERE setor IS NOT NULL LIMIT 5")
for row in (r3 or []):
    print(f"  pdv_id={row[0]} loja={row[1]} setor='{row[2]}' setor_id={row[3]}")

print("\n=== Setores existentes ===")
r4 = query("SELECT setor_id, codigo, nome FROM setor ORDER BY codigo")
for row in (r4 or []):
    print(f"  {row[0]}: {row[1]} | {row[2]}")
