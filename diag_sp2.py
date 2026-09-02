from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0,'.')
from database import query

print("=== supervisor_promotor atual ===")
r = query("SELECT id, supervisor_id, promotor_id, empresa_id, ativo FROM supervisor_promotor")
for row in (r or []):
    print(f"  id={row[0]} sup_id={row[1]} prom_id={row[2]} eid={row[3]} ativo={row[4]}")

print("\n=== Teste query do roteiro ===")
r2 = query("""SELECT u.usuario_id, u.nome, u.tipo
    FROM supervisor_promotor sp
    JOIN promotor pr ON sp.promotor_id=pr.promotor_id
    JOIN usuario u ON pr.usuario_id=u.usuario_id
    WHERE sp.supervisor_id=1 AND sp.ativo=1 AND u.ativo=1
    ORDER BY u.nome""")
print(f"  Resultado com ativo=1: {len(r2 or [])} promotores")
for row in (r2 or []):
    print(f"  {row}")

print("\n=== Sem filtro ativo ===")
r3 = query("""SELECT u.usuario_id, u.nome, u.tipo
    FROM supervisor_promotor sp
    JOIN promotor pr ON sp.promotor_id=pr.promotor_id
    JOIN usuario u ON pr.usuario_id=u.usuario_id
    WHERE sp.supervisor_id=1 AND u.ativo=1
    ORDER BY u.nome""")
print(f"  Resultado sem filtro ativo: {len(r3 or [])} promotores")
for row in (r3 or []):
    print(f"  {row}")
