import ast, subprocess

with open('pesquisa.py', 'r', encoding='utf-8') as f:
    c = f.read()

cnt = 0

# Linha 4069 — PDVs com pesquisas finalizadas sem filtro de cliente
antigo = ('    pdvs_c = query("""\n'
          '        SELECT DISTINCT cli.cliente_id, cli.nome_fantasia,\n'
          '               pdv.pdv_id, COALESCE(pdv.nome_loja,\'Matriz\') AS pdv_nome\n'
          '        FROM pesquisa_preco pp\n'
          '        JOIN cliente cli ON pp.cliente_id=cli.cliente_id\n'
          '        LEFT JOIN pdv ON pp.pdv_id=pdv.pdv_id\n'
          '        WHERE pp.fornecedor_id=? AND pp.status=\'finalizado\'\n'
          '        ORDER BY cli.nome_fantasia, pdv_nome\n'
          '    """, (forn_p[0],))')

novo = ('    from permissoes import get_where_cliente\n'
        '    _w_ac, _p_ac = get_where_cliente("cli")\n'
        '    _where_ac = f"AND {_w_ac.lstrip(\'AND \').strip()}" if _w_ac else ""\n'
        '    pdvs_c = query(f"""\n'
        '        SELECT DISTINCT cli.cliente_id, cli.nome_fantasia,\n'
        '               pdv.pdv_id, COALESCE(pdv.nome_loja,\'Matriz\') AS pdv_nome\n'
        '        FROM pesquisa_preco pp\n'
        '        JOIN cliente cli ON pp.cliente_id=cli.cliente_id\n'
        '        LEFT JOIN pdv ON pp.pdv_id=pdv.pdv_id\n'
        '        WHERE pp.fornecedor_id=? AND pp.status=\'finalizado\' {_where_ac}\n'
        '        ORDER BY cli.nome_fantasia, pdv_nome\n'
        '    """, tuple([forn_p[0]] + _p_ac))')

if antigo in c:
    c = c.replace(antigo, novo, 1)
    print("OK: PDVs pesquisas finalizadas filtrado por perfil")
    cnt += 1
else:
    print("AVISO: padrao nao encontrado")
    idx = c.find("pdvs_c = query")
    if idx > 0:
        print(f"Contexto: {repr(c[idx:idx+150])}")

with open('pesquisa.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c)
    print(f"Sintaxe OK — {cnt} correcoes")
    subprocess.run(["git","add","pesquisa.py"])
    r = subprocess.run(["git","commit","-m","fix: pesquisa PDVs analise competitiva filtrado por perfil"],
                       capture_output=True, text=True)
    print("Commit:", r.stdout.strip() or r.stderr.strip())
    r2 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r2.stdout.strip() or r2.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
