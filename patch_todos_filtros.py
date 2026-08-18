import ast, subprocess

FILTRO_IMPORT = """from permissoes import e_admin, e_master, e_promotor_vendedor, e_vendedor, usuario_id_atual
    _uid = usuario_id_atual()
    if e_promotor_vendedor():
        _extra = [_uid]
        _where_perfil = \"\"\"c.cliente_id IN (
            SELECT p2.cliente_id FROM att_promotor ap
            JOIN pdv p2 ON ap.pdv_id=p2.pdv_id
            JOIN promotor pr ON ap.promotor_id=pr.promotor_id
            WHERE pr.usuario_id=? AND ap.ativo!=0)\"\"\"
    elif e_vendedor() and not (e_admin() or e_master()):
        _extra = [_uid]
        _where_perfil = \"c.vendedor_id=?\"
    else:
        _extra = []
        _where_perfil = \"\"
    """

def get_clientes_filtrado():
    return """from permissoes import e_admin, e_master, e_promotor_vendedor, e_vendedor, usuario_id_atual
    _uid_f = usuario_id_atual()
    if e_promotor_vendedor():
        _clis = query(\"\"\"SELECT DISTINCT c.cliente_id, c.nome_fantasia
            FROM cliente c JOIN pdv p ON p.cliente_id=c.cliente_id
            JOIN att_promotor ap ON ap.pdv_id=p.pdv_id
            JOIN promotor pr ON ap.promotor_id=pr.promotor_id
            WHERE pr.usuario_id=%s AND ap.ativo!=0
            ORDER BY c.nome_fantasia\"\"\", (_uid_f,)) or []
    elif e_vendedor() and not (e_admin() or e_master()):
        _clis = query(\"SELECT cliente_id, nome_fantasia FROM cliente WHERE vendedor_id=%s ORDER BY nome_fantasia\",
                      (_uid_f,)) or []
    else:
        _clis = query(\"SELECT cliente_id, nome_fantasia FROM cliente ORDER BY nome_fantasia\") or []
    """

# ═══════════════════════════════════════════════════════════
# CADASTROS.PY
# ═══════════════════════════════════════════════════════════
print("=== cadastros.py ===")
with open('cadastros.py', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Duplicata no filtro de clientes — remover o primeiro bloco antigo
antigo_dup = """    from permissoes import e_admin, e_master, usuario_id_atual, e_vendedor\r\n    if e_vendedor():\r\n        where_q.append(\"c.vendedor_id=?\")\r\n        params_q.append(usuario_id_atual())\r\n\r\n    # Filtro de carteira por perfil"""
novo_dup   = """    # Filtro de carteira por perfil"""
if antigo_dup in c:
    c = c.replace(antigo_dup, novo_dup)
    print("  OK: duplicata removida em _lista_clientes")
else:
    print("  -- duplicata nao encontrada (ok)")

# 2. clientes_all para PDVs
antigo_all = '    clientes_all = query("SELECT cliente_id, nome_fantasia FROM cliente ORDER BY nome_fantasia")'
novo_all = '''    from permissoes import e_admin, e_master, e_promotor_vendedor, e_vendedor, usuario_id_atual
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
if antigo_all in c:
    c = c.replace(antigo_all, novo_all)
    print("  OK: clientes_all PDV filtrado")
else:
    print("  AVISO: clientes_all nao encontrado")

# 3. clientes em _tela_mix_pdv
antigo_mix = '    clientes = query("SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo=1 ORDER BY nome_fantasia")\r\n    if not clientes:\r\n        st.info("Cadastre um cliente primeiro."); return'
novo_mix = '''    from permissoes import e_admin, e_master, e_promotor_vendedor, e_vendedor, usuario_id_atual
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
        clientes = query("SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo=1 ORDER BY nome_fantasia") or []
    if not clientes:
        st.info("Cadastre um cliente primeiro."); return'''
if antigo_mix in c:
    c = c.replace(antigo_mix, novo_mix)
    print("  OK: clientes mix_pdv filtrado")
else:
    # Tenta sem \r\n
    antigo_mix2 = '    clientes = query("SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo=1 ORDER BY nome_fantasia")\n    if not clientes:\n        st.info("Cadastre um cliente primeiro."); return'
    if antigo_mix2 in c:
        c = c.replace(antigo_mix2, novo_mix.replace('\r\n','\n'))
        print("  OK: clientes mix_pdv filtrado (variante)")
    else:
        print("  AVISO: mix_pdv nao encontrado")

with open('cadastros.py', 'w', encoding='utf-8') as f:
    f.write(c)
try:
    ast.parse(c); print("  Sintaxe OK")
except SyntaxError as e:
    print(f"  ERRO: {e}")

# ═══════════════════════════════════════════════════════════
# CONTATOS.PY
# ═══════════════════════════════════════════════════════════
print("\n=== contatos.py ===")
with open('contatos.py', 'r', encoding='utf-8') as f:
    cc = f.read()

antigo_cont = '    where_cli = ["1=1"]\r\n    params_cli = []'
novo_cont = '''    where_cli  = ["c.ativo=1"]
    params_cli = []
    from permissoes import e_admin, e_master, e_promotor_vendedor, e_vendedor, usuario_id_atual
    _uid_cont = usuario_id_atual()
    if e_promotor_vendedor():
        where_cli.append("""c.cliente_id IN (
            SELECT p2.cliente_id FROM att_promotor ap
            JOIN pdv p2 ON ap.pdv_id=p2.pdv_id
            JOIN promotor pr ON ap.promotor_id=pr.promotor_id
            WHERE pr.usuario_id=%s AND ap.ativo!=0)""")
        params_cli.append(_uid_cont)
    elif e_vendedor() and not (e_admin() or e_master()):
        where_cli.append("c.vendedor_id=%s")
        params_cli.append(_uid_cont)'''

if antigo_cont in cc:
    cc = cc.replace(antigo_cont, novo_cont)
    print("  OK: where_cli com filtro perfil")
else:
    # Tenta sem \r\n
    antigo_cont2 = '    where_cli = ["1=1"]\n    params_cli = []'
    if antigo_cont2 in cc:
        cc = cc.replace(antigo_cont2, novo_cont)
        print("  OK: where_cli filtrado (variante)")
    else:
        print("  AVISO: where_cli nao encontrado")
        # Mostra contexto
        idx = cc.find('where_cli')
        print(f"  Contexto: {repr(cc[idx:idx+100])}")

# Corrige _extra_cli_params que pode nao existir
if '_extra_cli_params' in cc and '_uid_cont' in cc:
    # Remove referencia antiga a _extra_cli_params
    cc = cc.replace('tuple(_extra_cli_params + list(params_cli))', 'tuple(params_cli)')
    print("  OK: params_cli unificado")

with open('contatos.py', 'w', encoding='utf-8') as f:
    f.write(cc)
try:
    ast.parse(cc); print("  Sintaxe OK")
except SyntaxError as e:
    print(f"  ERRO: {e}")

# ═══════════════════════════════════════════════════════════
# VISITAS.PY — nova visita e lista de visitas
# ═══════════════════════════════════════════════════════════
print("\n=== visitas.py ===")
with open('visitas.py', 'r', encoding='utf-8') as f:
    vv = f.read()

# 1. Filtro na lista de visitas (WHERE da query principal)
antigo_vis_where = '    where = ["v.empresa_id IS NOT NULL"]'
if antigo_vis_where not in vv:
    antigo_vis_where = '    where, params = [], []'

# Busca o WHERE da lista de visitas
idx_where = vv.find('WHERE {\'  AND \'.join(where)}')
if idx_where < 0:
    idx_where = vv.find("WHERE {' AND '.join(where)}")

# Encontra inicio do bloco where da _lista_visitas
idx_lista = vv.find('def _lista_visitas():')
idx_where_bloco = vv.find('    where = [', idx_lista)
if idx_where_bloco > 0:
    linha_where = vv[idx_where_bloco:idx_where_bloco+50]
    print(f"  where encontrado: {repr(linha_where[:40])}")

    antigo_vw = vv[idx_where_bloco:idx_where_bloco+len('    where = []')+1]
    # Adiciona filtro por perfil apos inicializar where
    antigo_vw2 = '    where = []\n    params = []'
    novo_vw2 = '''    where  = []
    params = []
    # Filtro automatico por perfil
    from permissoes import e_admin, e_master, e_promotor_vendedor, e_vendedor, e_supervisor, usuario_id_atual
    _uid_vis = usuario_id_atual()
    if e_promotor_vendedor():
        where.append("""v.cliente_id IN (
            SELECT p2.cliente_id FROM att_promotor ap
            JOIN pdv p2 ON ap.pdv_id=p2.pdv_id
            JOIN promotor pr ON ap.promotor_id=pr.promotor_id
            WHERE pr.usuario_id=? AND ap.ativo!=0)""")
        params.append(_uid_vis)
    elif e_vendedor() and not (e_admin() or e_master()):
        where.append("v.cliente_id IN (SELECT cliente_id FROM cliente WHERE vendedor_id=?)")
        params.append(_uid_vis)
    elif e_supervisor():
        where.append("""v.cliente_id IN (
            SELECT p2.cliente_id FROM supervisor_promotor sp
            JOIN att_promotor ap ON ap.promotor_id=sp.promotor_id
            JOIN pdv p2 ON ap.pdv_id=p2.pdv_id
            JOIN supervisor s ON s.supervisor_id=sp.supervisor_id
            WHERE s.usuario_id=? AND sp.ativo=1 AND ap.ativo!=0)""")
        params.append(_uid_vis)'''
    if antigo_vw2 in vv:
        vv = vv.replace(antigo_vw2, novo_vw2, 1)
        print("  OK: filtro lista visitas por perfil")
    else:
        print("  AVISO: where visitas nao encontrado no padrao esperado")

# 2. Filtro na nova visita — selecao de clientes
antigo_v2 = '        clientes = query("SELECT cliente_id, nome_fantasia FROM cliente ORDER BY nome_fantasia")'
novo_v2 = '''        from permissoes import e_admin, e_master, e_promotor_vendedor, e_vendedor, usuario_id_atual
        _uid_nv = usuario_id_atual()
        if e_promotor_vendedor():
            clientes = query("""SELECT DISTINCT c.cliente_id, c.nome_fantasia
                FROM cliente c JOIN pdv p ON p.cliente_id=c.cliente_id
                JOIN att_promotor ap ON ap.pdv_id=p.pdv_id
                JOIN promotor pr ON ap.promotor_id=pr.promotor_id
                WHERE pr.usuario_id=%s AND ap.ativo!=0
                ORDER BY c.nome_fantasia""", (_uid_nv,)) or []
        elif e_vendedor() and not (e_admin() or e_master()):
            clientes = query("""SELECT cliente_id, nome_fantasia FROM cliente
                WHERE vendedor_id=%s ORDER BY nome_fantasia""", (_uid_nv,)) or []
        else:
            clientes = query("SELECT cliente_id, nome_fantasia FROM cliente ORDER BY nome_fantasia") or []'''
if antigo_v2 in vv:
    vv = vv.replace(antigo_v2, novo_v2)
    print("  OK: clientes nova visita filtrado")
else:
    print("  AVISO: clientes nova visita nao encontrado")

# 3. Filtro no seletor de clientes em nova pesquisa dentro de visitas (linha 538)
antigo_v3 = '                "SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo!=0 ORDER BY nome_fantasia")]'
novo_v3   = '''                "SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo!=0 ORDER BY nome_fantasia") or []]'''
# Nao muda — esse e para pesquisa dentro de visita, deixar como esta

with open('visitas.py', 'w', encoding='utf-8') as f:
    f.write(vv)
try:
    ast.parse(vv); print("  Sintaxe OK")
except SyntaxError as e:
    print(f"  ERRO: {e}")

# ═══════════════════════════════════════════════════════════
# ROTEIROS.PY — clientes no roteiro do vendedor
# ═══════════════════════════════════════════════════════════
print("\n=== roteiros.py ===")
import os
if os.path.exists('roteiros.py'):
    with open('roteiros.py', 'r', encoding='utf-8') as f:
        rr = f.read()
    
    antigo_rot = '    clientes = query("SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo!=0 ORDER BY nome_fantasia", ()) or []'
    novo_rot = '''    from permissoes import e_admin, e_master, e_promotor_vendedor, e_vendedor, usuario_id_atual
    _uid_rot = usuario_id_atual()
    if e_vendedor() and not (e_admin() or e_master()):
        clientes = query("""SELECT cliente_id, nome_fantasia FROM cliente
            WHERE vendedor_id=%s AND ativo!=0 ORDER BY nome_fantasia""", (_uid_rot,)) or []
    else:
        clientes = query("SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo!=0 ORDER BY nome_fantasia") or []'''
    
    if antigo_rot in rr:
        rr = rr.replace(antigo_rot, novo_rot)
        print("  OK: clientes roteiro filtrado")
    else:
        print("  AVISO: padrao roteiros nao encontrado")
    
    with open('roteiros.py', 'w', encoding='utf-8') as f:
        f.write(rr)
    try:
        ast.parse(rr); print("  Sintaxe OK")
    except SyntaxError as e:
        print(f"  ERRO: {e}")
else:
    print("  roteiros.py nao encontrado em disco")

# ═══════════════════════════════════════════════════════════
# COMMIT
# ═══════════════════════════════════════════════════════════
print("\n=== Commitando todos ===")
arquivos = ["cadastros.py","contatos.py","visitas.py"]
if os.path.exists('roteiros.py'): arquivos.append("roteiros.py")
subprocess.run(["git","add"] + arquivos)
r = subprocess.run(["git","commit","-m","fix: filtros carteira por perfil em cadastros contatos visitas roteiros"],
                   capture_output=True, text=True)
print("Commit:", r.stdout.strip() or r.stderr.strip())
r2 = subprocess.run(["git","push"], capture_output=True, text=True)
print("Push:", r2.stdout.strip() or r2.stderr.strip())
