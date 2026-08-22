import ast, subprocess

with open('contatos.py', 'r', encoding='utf-8') as f:
    c = f.read()

cnt = 0

# 1. Histórico — linha 1883: clientes com contatos sem filtro de perfil
antigo1 = ('        if tipo_h == "Cliente":\n'
           '            ents = query("""SELECT DISTINCT c.cliente_id, c.nome_fantasia\n'
           '                FROM cliente c JOIN contato_registro cr ON cr.cliente_id=c.cliente_id\n'
           '                WHERE cr.ativo!=0 ORDER BY c.nome_fantasia""")')

novo1 = ('        if tipo_h == "Cliente":\n'
         '            from permissoes import get_where_cliente\n'
         '            _w_he, _p_he = get_where_cliente("c")\n'
         '            _where_he = f"AND {_w_he.lstrip(\'AND \').strip()}" if _w_he else ""\n'
         '            ents = query(f"""SELECT DISTINCT c.cliente_id, c.nome_fantasia\n'
         '                FROM cliente c JOIN contato_registro cr ON cr.cliente_id=c.cliente_id\n'
         '                WHERE cr.ativo!=0 {_where_he} ORDER BY c.nome_fantasia""",\n'
         '                tuple(_p_he))')

if antigo1 in c:
    c = c.replace(antigo1, novo1)
    print("OK: historico clientes filtrado")
    cnt += 1
else:
    print("AVISO: padrao historico nao encontrado")

# 2. Cidades — linha 2066: filtra apenas cidades dos clientes do vendedor
antigo2 = ('        cidades = query("""SELECT DISTINCT cidade FROM cliente\n'
           "            WHERE cidade IS NOT NULL AND cidade != '' ORDER BY cidade\"\"\")")

novo2 = ('        from permissoes import get_where_cliente\n'
         '        _w_cid, _p_cid = get_where_cliente("c")\n'
         '        _where_cid = f"AND {_w_cid.lstrip(\'AND \').strip()}" if _w_cid else ""\n'
         '        cidades = query(f"""SELECT DISTINCT c.cidade FROM cliente c\n'
         "            WHERE c.cidade IS NOT NULL AND c.cidade != '' {_where_cid}\n"
         '            ORDER BY c.cidade""", tuple(_p_cid))')

if antigo2 in c:
    c = c.replace(antigo2, novo2)
    print("OK: cidades filtradas por perfil")
    cnt += 1
else:
    print("AVISO: padrao cidades nao encontrado")

with open('contatos.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c)
    print(f"Sintaxe OK — {cnt} correcoes")
    subprocess.run(["git","add","contatos.py"])
    r = subprocess.run(["git","commit","-m","fix: contatos historico e cidades filtrados por perfil"],
                       capture_output=True, text=True)
    print("Commit:", r.stdout.strip() or r.stderr.strip())
    r2 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r2.stdout.strip() or r2.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
