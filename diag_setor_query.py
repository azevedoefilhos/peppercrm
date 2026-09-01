from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0,'.')
from database import query

print("=== Teste 1: PDVs com setor_id=1 ===")
r = query("SELECT COUNT(*) FROM pdv WHERE setor_id=1 AND ativo!=0")
print(f"  setor_id=1 ativo: {r[0][0] if r else 'erro'}")

r2 = query("SELECT COUNT(*) FROM pdv WHERE setor_id=1")
print(f"  setor_id=1 total: {r2[0][0] if r2 else 'erro'}")

print("\n=== Teste 2: ativo!=0 vs ativo=true ===")
r3 = query("SELECT COUNT(*) FROM pdv WHERE ativo!=0")
print(f"  ativo!=0: {r3[0][0] if r3 else 'erro'}")
r4 = query("SELECT COUNT(*) FROM pdv WHERE ativo=true")
print(f"  ativo=true: {r4[0][0] if r4 else 'erro'}")
r5 = query("SELECT COUNT(*) FROM pdv WHERE ativo IS NOT FALSE")
print(f"  ativo IS NOT FALSE: {r5[0][0] if r5 else 'erro'}")

print("\n=== Teste 3: valores de ativo ===")
r6 = query("SELECT DISTINCT ativo, COUNT(*) FROM pdv GROUP BY ativo")
for row in (r6 or []):
    print(f"  ativo={row[0]} count={row[1]}")

print("\n=== Teste 4: query sem filtro ativo ===")
r7 = query("""SELECT s.nome, COUNT(p.pdv_id)
    FROM setor s LEFT JOIN pdv p ON p.setor_id=s.setor_id
    WHERE s.empresa_id=1 GROUP BY s.setor_id, s.nome ORDER BY s.codigo""")
for row in (r7 or []):
    print(f"  {row[0]}: {row[1]} PDVs")
