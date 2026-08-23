import ast, subprocess

with open('pesquisa.py', 'r', encoding='utf-8') as f:
    c = f.read()

antigo = ('    where, params = ["1=1"], []\n'
          '    if filtro_status != "Todos":\n'
          '        where.append("pp.status=?"); params.append(filtro_status)')

novo   = ('    from permissoes import get_where_cliente\n'
          '    _w_pq, _p_pq = get_where_cliente("cli")\n'
          '    where, params = ["1=1"], list(_p_pq)\n'
          '    if _w_pq: where.append(_w_pq.lstrip("AND ").strip())\n'
          '    if filtro_status != "Todos":\n'
          '        where.append("pp.status=?"); params.append(filtro_status)')

if antigo in c:
    c = c.replace(antigo, novo, 1)
    print("OK: where listagem pesquisas filtrado por perfil")
else:
    print("AVISO: padrao nao encontrado")

with open('pesquisa.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c)
    print("Sintaxe OK")
    subprocess.run(["git","add","pesquisa.py"])
    r = subprocess.run(["git","commit","-m","fix: listagem pesquisas filtrada por perfil"],
                       capture_output=True, text=True)
    print("Commit:", r.stdout.strip() or r.stderr.strip())
    r2 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r2.stdout.strip() or r2.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
