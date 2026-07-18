with open('roteiros.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Corrige query de vendedores - IN -> OR, e inclui MASTER
antigo = """    vends = query(\"\"\"SELECT u.usuario_id, u.nome FROM usuario u
        WHERE u.empresa_id=%s
        AND u.tipo IN ('REPRESENTANTE_ADM','REPRESENTANTE','VENDEDOR','PROMOTOR_VENDEDOR')
        AND u.ativo=1 ORDER BY u.nome\"\"\", (eid,)) or []"""

novo = """    vends = query(\"\"\"SELECT u.usuario_id, u.nome FROM usuario u
        WHERE u.empresa_id=%s
        AND (u.tipo='REPRESENTANTE_ADM' OR u.tipo='REPRESENTANTE'
             OR u.tipo='VENDEDOR' OR u.tipo='PROMOTOR_VENDEDOR' OR u.tipo='MASTER')
        AND u.ativo=1 ORDER BY u.nome\"\"\", (eid,)) or []"""

if antigo in c:
    c = c.replace(antigo, novo)
    print("OK: query vendedores corrigida")
else:
    print("ERRO: padrao nao encontrado")

with open('roteiros.py', 'w', encoding='utf-8') as f:
    f.write(c)

import ast
try:
    ast.parse(open('roteiros.py').read())
    print("Sintaxe OK")
except Exception as e:
    print(f"ERRO: {e}")
