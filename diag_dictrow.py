from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0, '.')
from database import query

r = query("""SELECT u.usuario_id, u.nome, u.email, u.whatsapp, u.tipo, u.ativo,
               v.vendedor_id, v.fone, v.cidade
    FROM usuario u
    LEFT JOIN vendedor v ON v.usuario_id=u.usuario_id
    WHERE u.empresa_id=%s
    AND u.tipo IN ('REPRESENTANTE_ADM','REPRESENTANTE','VENDEDOR','MASTER')
    ORDER BY u.nome""", (1,))

print(f"Total: {len(r)}")
for row in r:
    print(f"  tipo row: {type(row)}")
    print(f"  row[0]: {row[0]}")
    print(f"  row[1]: {row[1]}")
    print(f"  row[4]: {row[4]}")
    try:
        print(f"  keys: {list(row.keys())}")
    except:
        print("  sem keys()")
    break
