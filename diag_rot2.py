from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0,'.')
from database import query

print("=== Vendedores e carteiras ===")
r = query("""SELECT u.usuario_id, u.nome, u.tipo,
    COUNT(c.cliente_id) as total_clientes
    FROM usuario u
    LEFT JOIN cliente c ON c.vendedor_id=u.usuario_id
    WHERE u.empresa_id=1 AND u.ativo=1
    AND u.tipo IN ('MASTER','REPRESENTANTE','VENDEDOR','SUPERVISOR','ADM')
    GROUP BY u.usuario_id, u.nome, u.tipo
    ORDER BY u.nome""")
for row in (r or []):
    print(f"  id={row[0]} {row[1]} ({row[2]}) — {row[3]} clientes")

print("\n=== Clientes de Isabela (id=6) ===")
r2 = query("""SELECT cliente_id, nome_fantasia, vendedor_id, status
    FROM cliente WHERE vendedor_id=6 ORDER BY nome_fantasia LIMIT 5""")
for row in (r2 or []):
    print(f"  {row}")

print("\n=== Clientes sem vendedor_id ===")
r3 = query("SELECT COUNT(*) FROM cliente WHERE vendedor_id IS NULL AND empresa_id=1")
print(f"  {r3[0][0]} clientes sem vendedor")

print("\n=== Setores: query direta ===")
r4 = query("""SELECT s.nome, COUNT(p.pdv_id) as total
    FROM setor s
    LEFT JOIN pdv p ON p.setor_id=s.setor_id AND p.ativo!=0
    WHERE s.empresa_id=1
    GROUP BY s.setor_id, s.nome
    ORDER BY s.codigo""")
for row in (r4 or []):
    print(f"  {row[0]}: {row[1]} PDVs")
