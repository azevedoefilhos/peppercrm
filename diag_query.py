from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0, '.')
from database import query

print("=== Teste query com empresa_id=1 ===")
r = query("""
    SELECT u.usuario_id, u.nome, u.email, u.tipo, u.ativo,
           v.vendedor_id, v.fone, v.cidade
    FROM usuario u
    LEFT JOIN vendedor v ON v.usuario_id=u.usuario_id
    WHERE u.empresa_id=%s
      AND u.tipo IN ('REPRESENTANTE_ADM','REPRESENTANTE','VENDEDOR','MASTER')
    ORDER BY u.nome
""", (1,))
print("Resultado:", r)
print("Total:", len(r) if r else 0)
