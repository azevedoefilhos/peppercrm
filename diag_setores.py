from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0,'.')
from database import query

print("=== Setores na tabela setor ===")
setores = query("SELECT setor_id, codigo, nome FROM setor ORDER BY codigo")
for s in (setores or []):
    print(f"  {s[0]}: {s[1]} | {s[2]}")

print("\n=== Valores distintos de setor em pdv ===")
vals = query("SELECT DISTINCT setor, COUNT(*) FROM pdv WHERE setor IS NOT NULL GROUP BY setor ORDER BY setor")
for v in (vals or []):
    print(f"  '{v[0]}' — {v[1]} PDVs")

print("\n=== PDVs com setor_id preenchido ===")
r = query("SELECT COUNT(*) FROM pdv WHERE setor_id IS NOT NULL")
print(f"  {r[0][0]} PDVs com setor_id")

print("\n=== PDVs por setor_id ===")
r2 = query("""SELECT s.nome, COUNT(p.pdv_id)
    FROM setor s LEFT JOIN pdv p ON p.setor_id=s.setor_id
    GROUP BY s.setor_id, s.nome ORDER BY s.codigo""")
for r in (r2 or []):
    print(f"  {r[0]}: {r[1]} PDVs")
