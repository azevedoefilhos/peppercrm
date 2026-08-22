import ast, subprocess

with open('contatos.py', 'r', encoding='utf-8') as f:
    c = f.read()

cnt = 0

# 1. Aba Novo — substitui _cache_todos_clientes por get_lista_clientes
antigo1 = ('    from database import _cache_todos_clientes\n'
           '    clientes = [(r[0],r[1],None) for r in _cache_todos_clientes()]')
novo1   = ('    from permissoes import get_lista_clientes\n'
           '    clientes = [(r[0],r[1],None) for r in get_lista_clientes(so_ativos=False)]')

if antigo1 in c:
    c = c.replace(antigo1, novo1, 1)
    print("OK: Aba Novo clientes filtrados")
    cnt += 1
else:
    print("AVISO: padrao Novo nao encontrado")

# 2. Follow-ups — adiciona filtro de cliente na query
antigo2 = ('    pendentes = query("""\n'
           '        SELECT cr.contato_id,\n'
           '               cr.data_followup,\n'
           '               cr.via_comunicacao,\n'
           "               COALESCE(c.nome_fantasia, f.nome_fantasia,'—') AS entidade,\n"
           "               COALESCE(cr.contato_pessoa,'—') AS pessoa,\n"
           '               cr.assunto, cr.status, cr.prioridade,\n'
           "               COALESCE(cr.tipo_topico,'Contato') AS tipo,\n"
           '               cr.cliente_id\n'
           '        FROM contato_registro cr\n'
           '        LEFT JOIN cliente    c ON cr.cliente_id    = c.cliente_id\n'
           '        LEFT JOIN fornecedor f ON cr.fornecedor_id = f.fornecedor_id\n'
           '        WHERE cr.ativo!=0\n'
           '          AND cr.data_followup IS NOT NULL\n'
           "          AND cr.status NOT IN ('Concluído','Cancelado')\n"
           '        ORDER BY cr.data_followup ASC\n'
           '    """)')

novo2 = ('    from permissoes import get_where_cliente\n'
         '    _w_fu, _p_fu = get_where_cliente("c")\n'
         '    _where_fu = f"AND {_w_fu.lstrip(\'AND \').strip()}" if _w_fu else ""\n'
         '    pendentes = query(f"""\n'
         '        SELECT cr.contato_id,\n'
         '               cr.data_followup,\n'
         '               cr.via_comunicacao,\n'
         "               COALESCE(c.nome_fantasia, f.nome_fantasia,'—') AS entidade,\n"
         "               COALESCE(cr.contato_pessoa,'—') AS pessoa,\n"
         '               cr.assunto, cr.status, cr.prioridade,\n'
         "               COALESCE(cr.tipo_topico,'Contato') AS tipo,\n"
         '               cr.cliente_id\n'
         '        FROM contato_registro cr\n'
         '        LEFT JOIN cliente    c ON cr.cliente_id    = c.cliente_id\n'
         '        LEFT JOIN fornecedor f ON cr.fornecedor_id = f.fornecedor_id\n'
         '        WHERE cr.ativo!=0\n'
         '          AND cr.data_followup IS NOT NULL\n'
         "          AND cr.status NOT IN ('Concluído','Cancelado')\n"
         '          {_where_fu}\n'
         '        ORDER BY cr.data_followup ASC\n'
         '    """, tuple(_p_fu))')

if antigo2 in c:
    c = c.replace(antigo2, novo2, 1)
    print("OK: Follow-ups filtrados por perfil")
    cnt += 1
else:
    print("AVISO: padrao Follow-ups nao encontrado")

# 3. Por Fornecedor — adiciona filtro de cliente
antigo3 = ('    dados = query("""\n'
           '        SELECT cr.contato_id, cr.assunto, cr.status,\n'
           "               COALESCE(cr.tipo_topico,'Contato'),\n"
           "               COALESCE(c.nome_fantasia, f2.nome_fantasia,'—') AS entidade,\n"
           '               cr.tipo_entidade, cr.data_contato,\n'
           '               (SELECT COUNT(*) FROM contato_interacao ci\n'
           '                WHERE ci.contato_id=cr.contato_id AND ci.ativo!=0)\n'
           '        FROM contato_x_fornecedor cxf\n'
           '        JOIN contato_registro cr ON cxf.contato_id=cr.contato_id\n'
           '        LEFT JOIN cliente    c  ON cr.cliente_id    = c.cliente_id\n'
           '        LEFT JOIN fornecedor f2 ON cr.fornecedor_id = f2.fornecedor_id\n'
           '        WHERE cxf.fornecedor_id=? AND cr.ativo!=0\n'
           '        ORDER BY cr.data_contato DESC\n'
           '    """, (forn_sel[0],))')

novo3 = ('    from permissoes import get_where_cliente\n'
         '    _w_pf, _p_pf = get_where_cliente("c")\n'
         '    _where_pf = f"AND {_w_pf.lstrip(\'AND \').strip()}" if _w_pf else ""\n'
         '    dados = query(f"""\n'
         '        SELECT cr.contato_id, cr.assunto, cr.status,\n'
         "               COALESCE(cr.tipo_topico,'Contato'),\n"
         "               COALESCE(c.nome_fantasia, f2.nome_fantasia,'—') AS entidade,\n"
         '               cr.tipo_entidade, cr.data_contato,\n'
         '               (SELECT COUNT(*) FROM contato_interacao ci\n'
         '                WHERE ci.contato_id=cr.contato_id AND ci.ativo!=0)\n'
         '        FROM contato_x_fornecedor cxf\n'
         '        JOIN contato_registro cr ON cxf.contato_id=cr.contato_id\n'
         '        LEFT JOIN cliente    c  ON cr.cliente_id    = c.cliente_id\n'
         '        LEFT JOIN fornecedor f2 ON cr.fornecedor_id = f2.fornecedor_id\n'
         '        WHERE cxf.fornecedor_id=? AND cr.ativo!=0 {_where_pf}\n'
         '        ORDER BY cr.data_contato DESC\n'
         '    """, tuple([forn_sel[0]] + _p_pf))')

if antigo3 in c:
    c = c.replace(antigo3, novo3, 1)
    print("OK: Por Fornecedor filtrado por perfil")
    cnt += 1
else:
    print("AVISO: padrao Por Fornecedor nao encontrado")

with open('contatos.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c)
    print(f"Sintaxe OK — {cnt} correcoes")
    subprocess.run(["git","add","contatos.py"])
    r = subprocess.run(["git","commit","-m","fix: contatos novo followup por_fornecedor filtrados"],
                       capture_output=True, text=True)
    print("Commit:", r.stdout.strip() or r.stderr.strip())
    r2 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r2.stdout.strip() or r2.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
