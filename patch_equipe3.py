with open('equipe.py', 'r', encoding='utf-8') as f:
    c = f.read()

antigo = '''    vends_u = query("""
        SELECT u.usuario_id, u.nome, u.email, u.whatsapp, u.tipo, u.ativo,
               v.vendedor_id, v.fone, v.cidade
        FROM usuario u
        LEFT JOIN vendedor v ON v.usuario_id=u.usuario_id
        WHERE u.empresa_id=%s
          AND (u.tipo='REPRESENTANTE_ADM' OR u.tipo='REPRESENTANTE'
               OR u.tipo='VENDEDOR' OR u.tipo='MASTER')
        ORDER BY u.nome
    """, (eid,)) or []

    vends_leg = query("""
        SELECT v.vendedor_id, v.nome, v.email, v.whatsapp, v.fone, v.cidade
        FROM vendedor v
        WHERE v.empresa_id=%s AND v.usuario_id IS NULL AND v.ativo!=0
        ORDER BY v.nome
    """, (eid,)) or []

    vends = vends_u'''

novo = '''    # Busca usuarios comerciais SEM JOIN (usuario nao tem RLS)
    usu_raw = query("""
        SELECT usuario_id, nome, email, whatsapp, tipo, ativo
        FROM usuario
        WHERE empresa_id=%s
          AND (tipo='REPRESENTANTE_ADM' OR tipo='REPRESENTANTE'
               OR tipo='VENDEDOR' OR tipo='MASTER')
        ORDER BY nome
    """, (eid,)) or []

    # Busca vendedores separadamente (tem RLS — funciona com empresa_id da sessao)
    vend_raw = query("""
        SELECT vendedor_id, usuario_id, fone, cidade FROM vendedor
        WHERE empresa_id=%s AND ativo!=0
    """, (eid,)) or []
    vend_map = {v[1]: v for v in vend_raw if v[1]}

    # Combina em memoria sem JOIN
    vends_u = []
    for u in usu_raw:
        uid, nome, email, wa, tipo, ativo = u[0],u[1],u[2],u[3],u[4],u[5]
        v = vend_map.get(uid)
        vid   = v[0] if v else None
        vfone = v[2] if v else None
        vcid  = v[3] if v else None
        vends_u.append((uid, nome, email, wa, tipo, ativo, vid, vfone, vcid))

    # Vendedores legados sem usuario
    vends_leg = query("""
        SELECT vendedor_id, nome, email, whatsapp, fone, cidade
        FROM vendedor
        WHERE empresa_id=%s AND usuario_id IS NULL AND ativo!=0
        ORDER BY nome
    """, (eid,)) or []

    vends = vends_u'''

if antigo in c:
    c = c.replace(antigo, novo)
    print("OK: query separada aplicada")
else:
    print("ERRO: padrao nao encontrado")
    # Mostra contexto
    idx = c.find('vends_u = query')
    print("Contexto:", repr(c[idx:idx+50]) if idx>=0 else "nao encontrado")

with open('equipe.py', 'w', encoding='utf-8') as f:
    f.write(c)

import ast
try:
    ast.parse(open('equipe.py').read())
    print("Sintaxe OK")
except Exception as e:
    print(f"ERRO sintaxe: {e}")
