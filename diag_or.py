from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0, '.')
from database import query

print("=== Teste com OR ===")
r = query("""SELECT u.usuario_id, u.nome, u.tipo
    FROM usuario u
    LEFT JOIN vendedor v ON v.usuario_id=u.usuario_id
    WHERE u.empresa_id=%s
    AND (u.tipo='REPRESENTANTE_ADM' OR u.tipo='REPRESENTANTE'
         OR u.tipo='VENDEDOR' OR u.tipo='MASTER')
    ORDER BY u.nome""", (1,))
print(f"Total: {len(r) if r else 0}")
for row in r or []:
    print(f"  {row[0]} {row[1]} {row[2]}")

print("\n=== Verificar equipe.py em disco ===")
import os
f = open('equipe.py', encoding='utf-8').read()
print("tamanho:", len(f))
print("OR presente:", "OR u.tipo='VENDEDOR'" in f)
print("IN presente:", "IN ('REPRESENTANTE_ADM'" in f)
