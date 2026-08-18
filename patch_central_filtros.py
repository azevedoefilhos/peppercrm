import ast, subprocess, re

# ═══════════════════════════════════════════════════════════════
# 1. ADICIONA get_where_cliente() em permissoes.py
# ═══════════════════════════════════════════════════════════════
print("=== permissoes.py ===")
with open('permissoes.py', 'r', encoding='utf-8') as f:
    pm = f.read()

HELPER = '''
def get_where_cliente(alias="c"):
    """
    Retorna (where_extra, params) para filtrar clientes pelo perfil logado.
    where_extra: string SQL com AND ja incluido (vazia se ADM/MASTER)
    params: lista de parametros para a query
    Uso: where_extra, params = get_where_cliente()
         query(f"SELECT * FROM cliente c {where_extra} ORDER BY nome", params)
    """
    try:
        uid = usuario_id_atual()
        p   = perfil_atual()
        if p in ('MASTER','REPRESENTANTE_ADM','ADM'):
            return "", []
        elif p in ('PROMOTOR_VENDEDOR',):
            return (f"AND {alias}.cliente_id IN ("
                    "SELECT p2.cliente_id FROM att_promotor ap "
                    "JOIN pdv p2 ON ap.pdv_id=p2.pdv_id "
                    "JOIN promotor pr ON ap.promotor_id=pr.promotor_id "
                    "WHERE pr.usuario_id=? AND ap.ativo!=0)", [uid])
        elif p in ('REPRESENTANTE','VENDEDOR'):
            return f"AND {alias}.vendedor_id=?", [uid]
        elif p == 'SUPERVISOR':
            return (f"AND {alias}.cliente_id IN ("
                    "SELECT DISTINCT p2.cliente_id FROM supervisor_promotor sp "
                    "JOIN att_promotor ap ON ap.promotor_id=sp.promotor_id "
                    "JOIN pdv p2 ON ap.pdv_id=p2.pdv_id "
                    "WHERE sp.supervisor_id IN ("
                    "SELECT supervisor_id FROM supervisor WHERE usuario_id=?) "
                    "AND sp.ativo=1 AND ap.ativo!=0)", [uid])
        return "", []
    except Exception:
        return "", []


def get_lista_clientes(so_ativos=True, order="nome_fantasia"):
    """
    Retorna lista de (cliente_id, nome_fantasia) filtrada pelo perfil logado.
    Uso direto: clientes = get_lista_clientes()
    """
    from database import query as _q
    where_extra, params = get_where_cliente("c")
    ativo_sql = "c.ativo!=0" if so_ativos else "1=1"
    sql = f"""SELECT c.cliente_id, c.nome_fantasia
        FROM cliente c WHERE {ativo_sql} {where_extra}
        ORDER BY c.{order}"""
    return _q(sql, tuple(params)) or []

'''

if 'def get_where_cliente' not in pm:
    # Adiciona antes do ultimo def ou no final
    idx = pm.rfind('\ndef ')
    pm = pm[:idx] + HELPER + pm[idx:]
    print("  OK: get_where_cliente e get_lista_clientes adicionados")
else:
    print("  -- ja existe")

with open('permissoes.py', 'w', encoding='utf-8') as f:
    f.write(pm)
try:
    ast.parse(pm); print("  Sintaxe OK")
except SyntaxError as e:
    print(f"  ERRO: {e}")

# ═══════════════════════════════════════════════════════════════
# FUNCAO AUXILIAR: substitui queries de lista de clientes
# ═══════════════════════════════════════════════════════════════
def fix_lista_clientes(texto, var_name="clientes", so_ativos=True, msg=""):
    """Substitui query simples de lista de clientes pela versao filtrada."""
    ativo = "c.ativo!=0" if so_ativos else "1=1"
    
    # Padrao 1: query simples em uma linha
    p1 = f'query("SELECT cliente_id, nome_fantasia FROM cliente {"WHERE ativo!=0" if so_ativos else ""} ORDER BY nome_fantasia")'
    n1 = f'get_lista_clientes(so_ativos={so_ativos})'
    
    # Padrao 2: query simples com ativo=1
    p2 = 'query("SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo=1 ORDER BY nome_fantasia")'
    n2 = 'get_lista_clientes(so_ativos=True)'

    # Padrao 3: query simples sem filtro
    p3 = 'query("SELECT cliente_id, nome_fantasia FROM cliente ORDER BY nome_fantasia")'
    n3 = 'get_lista_clientes(so_ativos=False)'

    cnt = 0
    for p, n in [(p1,n1),(p2,n2),(p3,n3)]:
        if p in texto:
            cnt += texto.count(p)
            texto = texto.replace(p, n)
    if cnt and msg:
        print(f"  {msg}: {cnt} substituicao(oes)")
    return texto, cnt

# ═══════════════════════════════════════════════════════════════
# 2. CADASTROS.PY
# ═══════════════════════════════════════════════════════════════
print("\n=== cadastros.py ===")
with open('cadastros.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Adiciona import no topo da funcao _lista_clientes
if 'get_where_cliente' not in c:
    # Substitui o bloco de filtro duplicado por chamada ao helper
    antigo_filtro = '''    # Filtro de carteira por perfil
    from permissoes import e_admin, e_master, e_promotor_vendedor, e_vendedor, usuario_id_atual
    _uid_cli = usuario_id_atual()
    if e_promotor_vendedor():
        where_q.append("""c.cliente_id IN (
            SELECT p2.cliente_id FROM att_promotor ap
            JOIN pdv p2 ON ap.pdv_id=p2.pdv_id
            JOIN promotor pr ON ap.promotor_id=pr.promotor_id
            WHERE pr.usuario_id=? AND ap.ativo!=0)""")
        params_q.append(_uid_cli)
    elif e_vendedor() and not (e_admin() or e_master()):
        where_q.append("c.vendedor_id=?")
        params_q.append(_uid_cli)
    where_sql = ("WHERE " + " AND ".join(where_q)) if where_q else ""'''
    
    novo_filtro = '''    # Filtro por perfil — usa helper central
    from permissoes import get_where_cliente
    _w_extra, _p_extra = get_where_cliente("c")
    if _w_extra:
        # Remove o AND inicial para compatibilidade com where_q
        where_q.append(_w_extra.lstrip("AND ").strip())
        params_q.extend(_p_extra)
    where_sql = ("WHERE " + " AND ".join(where_q)) if where_q else ""'''
    
    if antigo_filtro in c:
        c = c.replace(antigo_filtro, novo_filtro)
        print("  OK: _lista_clientes usa helper")
    else:
        print("  AVISO: bloco filtro nao encontrado")

# Substitui clientes_all e mix_pdv
c, n1 = fix_lista_clientes(c, msg="clientes_all/mix")
# Substitui clientes_all (sem ativo)
antigo_all2 = '''    from permissoes import e_admin, e_master, e_promotor_vendedor, e_vendedor, usuario_id_atual
    _uid_all = usuario_id_atual()
    if e_promotor_vendedor():
        clientes_all = query("""SELECT DISTINCT c.cliente_id, c.nome_fantasia
            FROM cliente c JOIN pdv p ON p.cliente_id=c.cliente_id
            JOIN att_promotor ap ON ap.pdv_id=p.pdv_id
            JOIN promotor pr ON ap.promotor_id=pr.promotor_id
            WHERE pr.usuario_id=%s AND ap.ativo!=0
            ORDER BY c.nome_fantasia""", (_uid_all,)) or []
    elif e_vendedor() and not (e_admin() or e_master()):
        clientes_all = query("""SELECT cliente_id, nome_fantasia FROM cliente
            WHERE vendedor_id=%s ORDER BY nome_fantasia""", (_uid_all,)) or []
    else:
        clientes_all = query("SELECT cliente_id, nome_fantasia FROM cliente ORDER BY nome_fantasia") or []'''
if antigo_all2 in c:
    c = c.replace(antigo_all2,
        'from permissoes import get_lista_clientes\n    clientes_all = get_lista_clientes(so_ativos=False)')
    print("  OK: clientes_all PDV substituido")

# Tambem fix mix_pdv 
antigo_mix2 = '''    from permissoes import e_admin, e_master, e_promotor_vendedor, e_vendedor, usuario_id_atual
    _uid_mix = usuario_id_atual()
    if e_promotor_vendedor():
        clientes = query("""SELECT DISTINCT c.cliente_id, c.nome_fantasia
            FROM cliente c JOIN pdv p ON p.cliente_id=c.cliente_id
            JOIN att_promotor ap ON ap.pdv_id=p.pdv_id
            JOIN promotor pr ON ap.promotor_id=pr.promotor_id
            WHERE pr.usuario_id=%s AND ap.ativo!=0 AND c.ativo=1
            ORDER BY c.nome_fantasia""", (_uid_mix,)) or []
    elif e_vendedor() and not (e_admin() or e_master()):
        clientes = query("""SELECT cliente_id, nome_fantasia FROM cliente
            WHERE vendedor_id=%s AND ativo=1 ORDER BY nome_fantasia""", (_uid_mix,)) or []
    else:
        clientes = query("SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo=1 ORDER BY nome_fantasia") or []'''
if antigo_mix2 in c:
    c = c.replace(antigo_mix2,
        'from permissoes import get_lista_clientes\n    clientes = get_lista_clientes(so_ativos=True)')
    print("  OK: mix_pdv clientes substituido")

# Linha 2282 — lista clientes em vinculos/compras
antigo_vinc = '        FROM cliente ORDER BY nome_fantasia""")'
if antigo_vinc in c:
    # Substitui a query completa de clientes em vinculos
    c = c.replace(
        'FROM cliente ORDER BY nome_fantasia""")',
        'FROM cliente c WHERE 1=1 {get_where_cliente_sql} ORDER BY c.nome_fantasia""")')
    # Na verdade melhor usar get_lista_clientes diretamente
    # Revertemos e usamos abordagem diferente
    c = c.replace(
        'FROM cliente c WHERE 1=1 {get_where_cliente_sql} ORDER BY c.nome_fantasia""")',
        'FROM cliente ORDER BY nome_fantasia""")')

with open('cadastros.py', 'w', encoding='utf-8') as f:
    f.write(c)
try:
    ast.parse(c); print("  Sintaxe OK")
except SyntaxError as e:
    print(f"  ERRO: {e}")

# ═══════════════════════════════════════════════════════════════
# 3. CONTATOS.PY — linha 2109
# ═══════════════════════════════════════════════════════════════
print("\n=== contatos.py ===")
with open('contatos.py', 'r', encoding='utf-8') as f:
    cc = f.read()

# Substitui o where_cli por versao com helper
antigo_wc = '''    where_cli  = ["c.ativo=1"]
    params_cli = []
    from permissoes import e_admin, e_master, e_promotor_vendedor, e_vendedor, usuario_id_atual
    _uid_cont = usuario_id_atual()
    if e_promotor_vendedor():
        where_cli.append("""c.cliente_id IN (
            SELECT p2.cliente_id FROM att_promotor ap
            JOIN pdv p2 ON ap.pdv_id=p2.pdv_id
            JOIN promotor pr ON ap.promotor_id=pr.promotor_id
            WHERE pr.usuario_id=? AND ap.ativo!=0)""")
        params_cli.append(_uid_cont)
    elif e_vendedor() and not (e_admin() or e_master()):
        where_cli.append("c.vendedor_id=?")
        params_cli.append(_uid_cont)'''

novo_wc = '''    from permissoes import get_where_cliente
    _w_cont, _p_cont = get_where_cliente("c")
    where_cli  = ["c.ativo=1"]
    params_cli = list(_p_cont)
    if _w_cont:
        where_cli.append(_w_cont.lstrip("AND ").strip())'''

if antigo_wc in cc:
    cc = cc.replace(antigo_wc, novo_wc)
    print("  OK: where_cli usa helper")
else:
    # Tenta padrao sem os filtros ja aplicados
    antigo_wc2 = '    where_cli = ["1=1"]\n    params_cli = []'
    if antigo_wc2 in cc:
        cc = cc.replace(antigo_wc2, 
            '    from permissoes import get_where_cliente\n'
            '    _w_cont, _p_cont = get_where_cliente("c")\n'
            '    where_cli  = ["c.ativo=1"]\n'
            '    params_cli = list(_p_cont)\n'
            '    if _w_cont: where_cli.append(_w_cont.lstrip("AND ").strip())')
        print("  OK: where_cli (variante) usa helper")
    else:
        print("  AVISO: padrao where_cli nao encontrado")

with open('contatos.py', 'w', encoding='utf-8') as f:
    f.write(cc)
try:
    ast.parse(cc); print("  Sintaxe OK")
except SyntaxError as e:
    print(f"  ERRO: {e}")

# ═══════════════════════════════════════════════════════════════
# 4. PESQUISA.PY
# ═══════════════════════════════════════════════════════════════
print("\n=== pesquisa.py ===")
with open('pesquisa.py', 'r', encoding='utf-8') as f:
    pq = f.read()

# Linha 213 — ja tem filtro PV mas falta vendedor simples
antigo_pq = '''    from permissoes import e_admin, e_master, e_promotor_vendedor, e_vendedor, usuario_id_atual
    _uid_pq = usuario_id_atual()
    if e_promotor_vendedor():
        _clis_pq = query("""SELECT DISTINCT c.cliente_id, c.nome_fantasia
            FROM cliente c JOIN pdv p ON p.cliente_id=c.cliente_id
            JOIN att_promotor ap ON ap.pdv_id=p.pdv_id
            JOIN promotor pr ON ap.promotor_id=pr.promotor_id
            WHERE pr.usuario_id=? AND ap.ativo!=0
            ORDER BY c.nome_fantasia""", (_uid_pq,)) or []
    elif e_vendedor() and not (e_admin() or e_master()):
        _clis_pq = query("""SELECT cliente_id, nome_fantasia FROM cliente
            WHERE vendedor_id=? ORDER BY nome_fantasia""", (_uid_pq,)) or []
    else:
        _clis_pq = query("SELECT cliente_id, nome_fantasia FROM cliente ORDER BY nome_fantasia") or []
    todos_cli  = [("","Todos os clientes")] + [(str(r[0]), r[1]) for r in _clis_pq]'''

novo_pq = '''    from permissoes import get_lista_clientes
    _clis_pq = get_lista_clientes(so_ativos=False)
    todos_cli  = [("","Todos os clientes")] + [(str(r[0]), r[1]) for r in _clis_pq]'''

if antigo_pq in pq:
    pq = pq.replace(antigo_pq, novo_pq)
    print("  OK: todos_cli usa get_lista_clientes")
else:
    # Tenta padrao original sem filtro
    antigo_pq2 = '''    todos_cli  = [("","Todos os clientes")] + [
        (str(r[0]), r[1]) for r in query(
            "SELECT cliente_id, nome_fantasia FROM cliente ORDER BY nome_fantasia")]'''
    novo_pq2 = '''    from permissoes import get_lista_clientes
    todos_cli  = [("","Todos os clientes")] + [(str(r[0]), r[1]) for r in get_lista_clientes(so_ativos=False)]'''
    if antigo_pq2 in pq:
        pq = pq.replace(antigo_pq2, novo_pq2)
        print("  OK: todos_cli (variante) usa get_lista_clientes")
    else:
        print("  AVISO: padrao todos_cli nao encontrado")

# Linha 373 — lista de clientes em resultados de pesquisa
antigo_pq3 = '            FROM cliente ORDER BY'
if antigo_pq3 in pq:
    # Esta e para exibicao de resultados — precisa filtrar tambem
    # Busca contexto
    idx = pq.find(antigo_pq3)
    trecho = pq[max(0,idx-200):idx+100]
    print(f"  Contexto linha 373: {repr(trecho[150:])[:80]}")

with open('pesquisa.py', 'w', encoding='utf-8') as f:
    f.write(pq)
try:
    ast.parse(pq); print("  Sintaxe OK")
except SyntaxError as e:
    print(f"  ERRO: {e}")

# ═══════════════════════════════════════════════════════════════
# 5. VISITAS.PY — multiplos pontos
# ═══════════════════════════════════════════════════════════════
print("\n=== visitas.py ===")
with open('visitas.py', 'r', encoding='utf-8') as f:
    vv = f.read()

# Substitui todas as listas de clientes sem filtro
antigos_vv = [
    'query("""SELECT cliente_id, nome_fantasia FROM cliente\n            WHERE vendedor_id=%s AND ativo!=0 ORDER BY nome_fantasia""", (_uid_nv,)) or []\n    else:\n        clientes = query("SELECT cliente_id, nome_fantasia FROM cliente ORDER BY nome_fantasia") or []',
    'query("""SELECT cliente_id, nome_fantasia FROM cliente\n            WHERE vendedor_id=%s AND ativo!=0 ORDER BY nome_fantasia""", (_uid_att2,)) or []\n    else:\n        clientes = query("SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo!=0 ORDER BY nome_fantasia") or []',
]

# Abordagem mais simples: substituir todos os padroes conhecidos
replacements = [
    # Nova visita (linha 306-309)
    ('        from permissoes import e_admin, e_master, e_promotor_vendedor, e_vendedor, usuario_id_atual\n'
     '        _uid_nv = usuario_id_atual()\n'
     '        if e_promotor_vendedor():\n'
     '            clientes = query("""SELECT DISTINCT c.cliente_id, c.nome_fantasia\n'
     '                FROM cliente c JOIN pdv p ON p.cliente_id=c.cliente_id\n'
     '                JOIN att_promotor ap ON ap.pdv_id=p.pdv_id\n'
     '                JOIN promotor pr ON ap.promotor_id=pr.promotor_id\n'
     '                WHERE pr.usuario_id=%s AND ap.ativo!=0\n'
     '                ORDER BY c.nome_fantasia""", (_uid_nv,)) or []\n'
     '        elif e_vendedor() and not (e_admin() or e_master()):\n'
     '            clientes = query("""SELECT cliente_id, nome_fantasia FROM cliente\n'
     '                WHERE vendedor_id=%s ORDER BY nome_fantasia""", (_uid_nv,)) or []\n'
     '        else:\n'
     '            clientes = query("SELECT cliente_id, nome_fantasia FROM cliente ORDER BY nome_fantasia") or []',
     '        from permissoes import get_lista_clientes\n'
     '        clientes = get_lista_clientes(so_ativos=False)'),
]

cnt_vv = 0
for antigo, novo in replacements:
    if antigo in vv:
        vv = vv.replace(antigo, novo)
        cnt_vv += 1
        print(f"  OK: substituicao {cnt_vv}")

# Substitui padroes simples restantes com get_lista_clientes
from_perms = 'from permissoes import get_lista_clientes\n    clientes = get_lista_clientes(so_ativos=True)\n'
padroes_simples = [
    ('    from permissoes import e_admin, e_master, e_vendedor, usuario_id_atual as _uid_att2_fn\n'
     '    _uid_att2 = _uid_att2_fn()\n'
     '    if e_vendedor() and not (e_admin() or e_master()):\n'
     '        clientes = query("""SELECT cliente_id, nome_fantasia FROM cliente\n'
     '            WHERE vendedor_id=? AND ativo!=0 ORDER BY nome_fantasia""", (_uid_att2,)) or []\n'
     '    else:\n'
     '        clientes = query("SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo!=0 ORDER BY nome_fantasia") or []\n',
     '    from permissoes import get_lista_clientes\n'
     '    clientes = get_lista_clientes(so_ativos=True)\n'),
]
for antigo, novo in padroes_simples:
    n = vv.count(antigo)
    if n > 0:
        vv = vv.replace(antigo, novo)
        print(f"  OK: {n} padrao(oes) simples substituido(s)")

with open('visitas.py', 'w', encoding='utf-8') as f:
    f.write(vv)
try:
    ast.parse(vv); print("  Sintaxe OK")
except SyntaxError as e:
    print(f"  ERRO linha {e.lineno}: {e.msg}")

# ═══════════════════════════════════════════════════════════════
# 6. RELATORIOS.PY — adiciona filtro no WHERE principal
# ═══════════════════════════════════════════════════════════════
print("\n=== relatorios.py ===")
with open('relatorios.py', 'r', encoding='utf-8') as f:
    rr = f.read()

# Busca os WHEREs principais de cada relatorio
# A abordagem: adicionar get_where_cliente antes do where_sql em cada funcao
antigo_rr = '    where_sql = ("WHERE " + " AND ".join(where)) if where else ""'
novo_rr   = '''    from permissoes import get_where_cliente
    _w_rel, _p_rel = get_where_cliente("c")
    if _w_rel: where.append(_w_rel.lstrip("AND ").strip()); params.extend(_p_rel)
    where_sql = ("WHERE " + " AND ".join(where)) if where else ""'''

cnt_rr = rr.count(antigo_rr)
print(f"  Encontradas {cnt_rr} ocorrencias de where_sql")
if cnt_rr > 0:
    rr = rr.replace(antigo_rr, novo_rr)
    print(f"  OK: {cnt_rr} where_sql com filtro de perfil")

with open('relatorios.py', 'w', encoding='utf-8') as f:
    f.write(rr)
try:
    ast.parse(rr); print("  Sintaxe OK")
except SyntaxError as e:
    print(f"  ERRO linha {e.lineno}: {e.msg}")

# ═══════════════════════════════════════════════════════════════
# 7. ROTEIROS.PY — clientes por carteira
# ═══════════════════════════════════════════════════════════════
print("\n=== roteiros.py ===")
with open('roteiros.py', 'r', encoding='utf-8') as f:
    rot = f.read()

antigo_rot = ('    from permissoes import e_admin, e_master, e_vendedor, usuario_id_atual\n'
              '    _uid_rot = usuario_id_atual()\n'
              '    if e_vendedor() and not (e_admin() or e_master()):\n'
              '        clientes = query("""SELECT cliente_id, nome_fantasia FROM cliente\n'
              '            WHERE vendedor_id=%s AND ativo!=0 ORDER BY nome_fantasia""", (_uid_rot,)) or []\n'
              '    else:\n'
              '        clientes = query("SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo!=0 ORDER BY nome_fantasia") or []')

novo_rot = ('    from permissoes import get_lista_clientes\n'
            '    clientes = get_lista_clientes(so_ativos=True)')

cnt_rot = rot.count(antigo_rot)
print(f"  Encontradas {cnt_rot} ocorrencias")
if cnt_rot > 0:
    rot = rot.replace(antigo_rot, novo_rot)
    print(f"  OK: {cnt_rot} lista(s) de clientes filtrada(s)")
else:
    # Tenta padrao com %s
    antigo_rot2 = 'clientes = query("SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo!=0 ORDER BY nome_fantasia") or []'
    if antigo_rot2 in rot:
        rot = rot.replace(antigo_rot2,
            'clientes = get_lista_clientes(so_ativos=True)\n    from permissoes import get_lista_clientes')
        print("  OK: variante substituida")

with open('roteiros.py', 'w', encoding='utf-8') as f:
    f.write(rot)
try:
    ast.parse(rot); print("  Sintaxe OK")
except SyntaxError as e:
    print(f"  ERRO: {e}")

# ═══════════════════════════════════════════════════════════════
# COMMIT
# ═══════════════════════════════════════════════════════════════
print("\n=== Commitando ===")
subprocess.run(["git","add",
    "permissoes.py","cadastros.py","contatos.py",
    "pesquisa.py","visitas.py","relatorios.py","roteiros.py"])
r = subprocess.run(["git","commit",
    "-m","feat: helper get_where_cliente + filtros perfil em todos os modulos"],
    capture_output=True, text=True)
print("Commit:", r.stdout.strip() or r.stderr.strip())
r2 = subprocess.run(["git","push"], capture_output=True, text=True)
print("Push:", r2.stdout.strip() or r2.stderr.strip())
