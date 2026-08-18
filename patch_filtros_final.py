import ast, subprocess, os

erros = []

# ═══════════════════════════════════════════════════════════
# PESQUISA.PY — linha 203-205
# ═══════════════════════════════════════════════════════════
print("=== pesquisa.py ===")
with open('pesquisa.py', 'r', encoding='utf-8') as f:
    pq = f.read()

antigo_pq = '''    todos_cli  = [("","Todos os clientes")] + [
        (str(r[0]), r[1]) for r in query(
            "SELECT cliente_id, nome_fantasia FROM cliente ORDER BY nome_fantasia")]'''

novo_pq = '''    from permissoes import e_admin, e_master, e_promotor_vendedor, e_vendedor, usuario_id_atual
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

if antigo_pq in pq:
    pq = pq.replace(antigo_pq, novo_pq)
    print("  OK: todos_cli filtrado")
else:
    print("  AVISO: padrao nao encontrado")
    erros.append("pesquisa: todos_cli")

with open('pesquisa.py', 'w', encoding='utf-8') as f:
    f.write(pq)
try:
    ast.parse(pq); print("  Sintaxe OK")
except SyntaxError as e:
    print(f"  ERRO: {e}"); erros.append(f"pesquisa sintaxe: {e}")

# ═══════════════════════════════════════════════════════════
# CONTATOS.PY — troca %s por ? (SQLite) e corrige params
# ═══════════════════════════════════════════════════════════
print("\n=== contatos.py ===")
with open('contatos.py', 'r', encoding='utf-8') as f:
    cc = f.read()

# O filtro usa %s mas o banco local usa ? — corrigir
antigo_cc = '''    where_cli  = ["c.ativo=1"]
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

novo_cc = '''    where_cli  = ["c.ativo=1"]
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

if antigo_cc in cc:
    cc = cc.replace(antigo_cc, novo_cc)
    print("  OK: %s -> ? corrigido")
else:
    print("  AVISO: padrao nao encontrado")
    erros.append("contatos: where_cli")

with open('contatos.py', 'w', encoding='utf-8') as f:
    f.write(cc)
try:
    ast.parse(cc); print("  Sintaxe OK")
except SyntaxError as e:
    print(f"  ERRO: {e}"); erros.append(f"contatos sintaxe: {e}")

# ═══════════════════════════════════════════════════════════
# VISITAS.PY — 3 pontos: lista visitas, nova visita, roteiro
# ═══════════════════════════════════════════════════════════
print("\n=== visitas.py ===")
with open('visitas.py', 'r', encoding='utf-8') as f:
    vv = f.read()

# 1. Lista visitas (linha 131) — adicionar filtro por perfil no where
antigo_v1 = '    where, params = ["1=1"], []'
novo_v1 = '''    where, params = ["1=1"], []
    # Filtro automatico por perfil do usuario logado
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
            SELECT DISTINCT p2.cliente_id FROM supervisor_promotor sp
            JOIN att_promotor ap ON ap.promotor_id=sp.promotor_id
            JOIN pdv p2 ON ap.pdv_id=p2.pdv_id
            WHERE sp.supervisor_id IN (
                SELECT supervisor_id FROM supervisor WHERE usuario_id=?
            ) AND sp.ativo=1 AND ap.ativo!=0)""")
        params.append(_uid_vis)'''

if antigo_v1 in vv:
    vv = vv.replace(antigo_v1, novo_v1, 1)
    print("  OK: filtro lista visitas")
else:
    print("  AVISO: where lista visitas nao encontrado")
    erros.append("visitas: where lista")

# 2. Clientes att_promotor roteiro (linha 981)
antigo_v2 = '    clientes = query("SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo!=0 ORDER BY nome_fantasia")\n    if not clientes:\n        st.info("Cadastre clientes primeiro.")\n        return\n\n    cli_sel = st.selectbox("Cliente", clientes'
if antigo_v2 in vv:
    novo_v2 = '''    from permissoes import e_admin, e_master, e_vendedor, usuario_id_atual
    _uid_att = usuario_id_atual()
    if e_vendedor() and not (e_admin() or e_master()):
        clientes = query("""SELECT cliente_id, nome_fantasia FROM cliente
            WHERE vendedor_id=? AND ativo!=0 ORDER BY nome_fantasia""", (_uid_att,)) or []
    else:
        clientes = query("SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo!=0 ORDER BY nome_fantasia") or []
    if not clientes:
        st.info("Cadastre clientes primeiro.")
        return

    cli_sel = st.selectbox("Cliente", clientes'''
    vv = vv.replace(antigo_v2, novo_v2, 1)
    print("  OK: clientes att_promotor filtrado")

# 3. Segunda ocorrencia de clientes sem filtro (linha 1079) - att_vendedor
antigo_v3 = '    clientes = query("SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo!=0 ORDER BY nome_fantasia")\n'
count_v3 = vv.count(antigo_v3)
print(f"  Ocorrencias de clientes sem filtro: {count_v3}")
if count_v3 > 0:
    novo_v3 = '''    from permissoes import e_admin, e_master, e_vendedor, usuario_id_atual as _uid_att2_fn
    _uid_att2 = _uid_att2_fn()
    if e_vendedor() and not (e_admin() or e_master()):
        clientes = query("""SELECT cliente_id, nome_fantasia FROM cliente
            WHERE vendedor_id=? AND ativo!=0 ORDER BY nome_fantasia""", (_uid_att2,)) or []
    else:
        clientes = query("SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo!=0 ORDER BY nome_fantasia") or []
'''
    vv = vv.replace(antigo_v3, novo_v3, count_v3)
    print(f"  OK: {count_v3} ocorrencia(s) filtrada(s)")

with open('visitas.py', 'w', encoding='utf-8') as f:
    f.write(vv)
try:
    ast.parse(vv); print("  Sintaxe OK")
except SyntaxError as e:
    print(f"  ERRO: {e}"); erros.append(f"visitas sintaxe: {e}")

# ═══════════════════════════════════════════════════════════
# ROTEIROS.PY — vendedor ve apenas seu proprio roteiro
# ═══════════════════════════════════════════════════════════
print("\n=== roteiros.py ===")
with open('roteiros.py', 'r', encoding='utf-8') as f:
    rr = f.read()

# Substitui o selectbox de vendedores para que vendedor veja apenas si mesmo
antigo_rr = '''    vend_sel = st.selectbox("Vendedor", vends, format_func=lambda x: x[1], key="rv_sel")
    vend_id  = vend_sel[0]'''

novo_rr = '''    from permissoes import e_admin, e_master, e_vendedor, usuario_id_atual
    _uid_rv = usuario_id_atual()
    if e_vendedor() and not (e_admin() or e_master()):
        # Vendedor ve apenas seu proprio roteiro
        vend_id = _uid_rv
        vend_nome = next((v[1] for v in vends if v[0] == vend_id), "Meu Roteiro")
        st.info(f"Exibindo roteiro de: **{vend_nome}**")
    else:
        vend_sel = st.selectbox("Vendedor", vends, format_func=lambda x: x[1], key="rv_sel")
        vend_id  = vend_sel[0]'''

if antigo_rr in rr:
    rr = rr.replace(antigo_rr, novo_rr)
    print("  OK: vendedor ve apenas seu roteiro")
else:
    print("  AVISO: selectbox vendedor nao encontrado")
    erros.append("roteiros: selectbox")

with open('roteiros.py', 'w', encoding='utf-8') as f:
    f.write(rr)
try:
    ast.parse(rr); print("  Sintaxe OK")
except SyntaxError as e:
    print(f"  ERRO: {e}"); erros.append(f"roteiros sintaxe: {e}")

# ═══════════════════════════════════════════════════════════
# COMMIT
# ═══════════════════════════════════════════════════════════
print("\n=== Resumo ===")
if erros:
    print("AVISOS:", erros)
else:
    print("Tudo aplicado sem erros!")

subprocess.run(["git","add","pesquisa.py","contatos.py","visitas.py","roteiros.py"])
r = subprocess.run(["git","commit","-m","fix: filtros perfil pesquisa contatos visitas roteiros"],
                   capture_output=True, text=True)
print("Commit:", r.stdout.strip() or r.stderr.strip())
r2 = subprocess.run(["git","push"], capture_output=True, text=True)
print("Push:", r2.stdout.strip() or r2.stderr.strip())
