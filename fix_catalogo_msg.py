import ast, subprocess

with open('catalogo.py', 'r', encoding='utf-8') as f:
    c = f.read()

antigo = ('    clientes_todos = query("SELECT cliente_id, nome_fantasia, status, perfil FROM cliente ORDER BY nome_fantasia") or []')

novo = ('    from permissoes import get_where_cliente\n'
        '    _w_msg, _p_msg = get_where_cliente("c")\n'
        '    _where_msg = f"WHERE {_w_msg.lstrip(\'AND \').strip()}" if _w_msg else ""\n'
        '    clientes_todos = query(f"SELECT c.cliente_id, c.nome_fantasia, c.status, c.perfil FROM cliente c {_where_msg} ORDER BY c.nome_fantasia", tuple(_p_msg)) or []')

if antigo in c:
    c = c.replace(antigo, novo, 1)
    print("OK: clientes_todos filtrado em _tela_enviar_mensagem")
else:
    print("AVISO: padrao nao encontrado")
    idx = c.find('clientes_todos = query')
    if idx > 0:
        print(f"Contexto: {repr(c[idx:idx+100])}")

with open('catalogo.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c)
    print("Sintaxe OK")
    subprocess.run(["git","add","catalogo.py"])
    r = subprocess.run(["git","commit","-m","fix: mensagens clientes filtrados por perfil"],
                       capture_output=True, text=True)
    print("Commit:", r.stdout.strip() or r.stderr.strip())
    r2 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r2.stdout.strip() or r2.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
