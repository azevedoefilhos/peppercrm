import ast, subprocess

erros = []

def aplicar(fname, antigo, novo, descricao):
    with open(fname, 'r', encoding='utf-8') as f:
        c = f.read()
    if antigo in c:
        c = c.replace(antigo, novo, 1)
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(c)
        try:
            ast.parse(c)
            print(f"  OK: {descricao}")
        except SyntaxError as e:
            print(f"  ERRO sintaxe {fname} linha {e.lineno}: {e.msg}")
            erros.append(f"{fname}: {e}")
    else:
        print(f"  AVISO: padrao nao encontrado — {descricao}")

# ═══════════════════════════════════════════════════════════
print("=== cadastros.py ===")

# 1. PDVs linha 2528 (principal - ja tentamos antes)
aplicar('cadastros.py',
    '    # ── QUERY com todos os filtros ────────────────────────────────────────\n    where_p = ["1=1"]; params_p = []\n    if cli_fil[0]:',
    '    # ── QUERY com todos os filtros ────────────────────────────────────────\n    from permissoes import get_where_cliente\n    _w_pdv, _p_pdv = get_where_cliente("c")\n    where_p = ["1=1"]; params_p = list(_p_pdv)\n    if _w_pdv: where_p.append(_w_pdv.lstrip("AND ").strip())\n    if cli_fil[0]:',
    'PDVs where_p linha 2528')

# 2. Lista clientes linha 1992 (where_q)
aplicar('cadastros.py',
    '    where_q  = []\n    params_q = []',
    '    from permissoes import get_where_cliente\n    _w_q, _p_q = get_where_cliente("c")\n    where_q  = []\n    params_q = list(_p_q)\n    if _w_q: where_q.append(_w_q.lstrip("AND ").strip())',
    'lista clientes where_q linha 1992')

# 3. Central compras linha 3062 (where_c)
aplicar('cadastros.py',
    '    # Aplica filtro\n    where_c = []\n    params_c = []',
    '    # Aplica filtro\n    from permissoes import get_where_cliente\n    _w_c, _p_c = get_where_cliente("c")\n    where_c = []\n    params_c = list(_p_c)\n    if _w_c: where_c.append(_w_c.lstrip("AND ").strip())',
    'central compras where_c linha 3062')

# ═══════════════════════════════════════════════════════════
print("\n=== contatos.py ===")

# Linha 142 — lista de visitas/contatos recentes (usa cliente via JOIN)
# Esta query e de contato_registro, nao de cliente diretamente — nao precisa filtro aqui
# O filtro ja e aplicado em where_cli (linha 2082)
# Linha 142 e para contatos recentes — filtrar por vendedor_id do cliente
aplicar('contatos.py',
    '    # Query\n    hoje  = date.today().isoformat()\n    where = ["cr.ativo!=0"]\n    params = []',
    '    # Query\n    hoje  = date.today().isoformat()\n    from permissoes import get_where_cliente\n    _w_cr, _p_cr = get_where_cliente("c")\n    where = ["cr.ativo!=0"]\n    params = list(_p_cr)\n    if _w_cr: where.append(_w_cr.lstrip("AND ").strip())',
    'contatos recentes where linha 142')

# ═══════════════════════════════════════════════════════════
print("\n=== relatorios.py ===")

# Linha 852 — _rel_nao_apresentados
aplicar('relatorios.py',
    '    # WHERE — usa status (campo correto) em vez de ativo\n    where        = []\n    where_params = []',
    '    # WHERE — usa status (campo correto) em vez de ativo\n    from permissoes import get_where_cliente\n    _w_rel2, _p_rel2 = get_where_cliente("c")\n    where        = []\n    where_params = list(_p_rel2)\n    if _w_rel2: where.append(_w_rel2.lstrip("AND ").strip())',
    'nao_apresentados where linha 852')

# Linha 999 — _rel_cliente (cobertura)
aplicar('relatorios.py',
    '    # ── WHERE dinâmico — usa status (campo correto) sem c.ativo!=0 ──────────\n    # Filtra por perfil do cliente (campo do cadastro) + cidade + status\n    # LEFT JOIN pdv mantido para quem já tem PDV, mas não exclui quem não tem\n    where = []\n    params_base = []',
    '    # ── WHERE dinâmico — usa status (campo correto) sem c.ativo!=0 ──────────\n    # Filtra por perfil do cliente (campo do cadastro) + cidade + status\n    # LEFT JOIN pdv mantido para quem já tem PDV, mas não exclui quem não tem\n    from permissoes import get_where_cliente\n    _w_rel3, _p_rel3 = get_where_cliente("c")\n    where = []\n    params_base = list(_p_rel3)\n    if _w_rel3: where.append(_w_rel3.lstrip("AND ").strip())',
    'cobertura where linha 999')

# ═══════════════════════════════════════════════════════════
print("\n=== despesas.py ===")
# Despesas: filtrar por usuario_id (quem registrou), NAO por carteira de clientes
# Conforme decidido: despesas pertencem ao usuario que as registrou
# Adicionar filtro por d.usuario_id ao inves de cliente
aplicar('despesas.py',
    '    where = ["d.ativo IS NOT FALSE", "d.data_despesa BETWEEN ? AND ?"]\n    params = [d_ini, d_fim]',
    '    from permissoes import e_admin, e_master, usuario_id_atual\n    _uid_desp = usuario_id_atual()\n    where = ["d.ativo IS NOT FALSE", "d.data_despesa BETWEEN ? AND ?"]\n    params = [d_ini, d_fim]\n    if not (e_admin() or e_master()):\n        where.append("d.usuario_id=?")\n        params.append(_uid_desp)',
    'despesas filtro por usuario')

# ═══════════════════════════════════════════════════════════
print("\n=== Commitando ===")
if not erros:
    subprocess.run(["git","add","cadastros.py","contatos.py","relatorios.py","despesas.py"])
    r = subprocess.run(["git","commit","-m","fix: filtros perfil em todos os WHEREs restantes"],
                       capture_output=True, text=True)
    print("Commit:", r.stdout.strip() or r.stderr.strip())
    r2 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r2.stdout.strip() or r2.stderr.strip())
else:
    print("ERROS encontrados — nao commitando:", erros)
