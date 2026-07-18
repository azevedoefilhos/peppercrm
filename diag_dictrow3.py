from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0, '.')
from database import query

print("=== Teste sem filtro tipo ===")
r = query("""SELECT u.usuario_id, u.nome, u.tipo
    FROM usuario u
    LEFT JOIN vendedor v ON v.usuario_id=u.usuario_id
    WHERE u.empresa_id=%s
    ORDER BY u.nome""", (1,))
print(f"Total: {len(r) if r else 0}")
for row in r or []:
    print(f"  {row[0]} {row[1]} {row[2]}")

print("\n=== Teste com filtro tipo simples ===")
r2 = query("""SELECT u.usuario_id, u.nome, u.tipo
    FROM usuario u
    LEFT JOIN vendedor v ON v.usuario_id=u.usuario_id
    WHERE u.empresa_id=%s AND u.tipo='VENDEDOR'
    ORDER BY u.nome""", (1,))
print(f"Total: {len(r2) if r2 else 0}")
for row in r2 or []:
    print(f"  {row[0]} {row[1]} {row[2]}")

print("\n=== Teste IN com lista ===")
r3 = query("""SELECT u.usuario_id, u.nome, u.tipo
    FROM usuario u
    LEFT JOIN vendedor v ON v.usuario_id=u.usuario_id
    WHERE u.empresa_id=%s
    AND u.tipo IN ('REPRESENTANTE_ADM','REPRESENTANTE','VENDEDOR','MASTER')
    ORDER BY u.nome""", (1,))
print(f"Total: {len(r3) if r3 else 0}")
