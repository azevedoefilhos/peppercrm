import ast, subprocess

with open('visitas.py', 'r', encoding='utf-8') as f:
    c = f.read()

antigo = ('    where, params = ["p.ativo!=0"], []\n'
          '    if fil_dia != "Todos":\n'
          '        where.append("p.dia_visita=?"); params.append(fil_dia)\n'
          '    if fil_freq != "Todas":\n'
          '        where.append("p.frequencia_visita=?"); params.append(fil_freq)\n'
          '    if fil_cli[0]:\n'
          '        where.append("p.cliente_id=?"); params.append(fil_cli[0])')

novo   = ('    from permissoes import get_where_cliente\n'
          '    _w_rot, _p_rot = get_where_cliente("c")\n'
          '    where, params = ["p.ativo!=0"], list(_p_rot)\n'
          '    if _w_rot: where.append(_w_rot.lstrip("AND ").strip())\n'
          '    if fil_dia != "Todos":\n'
          '        where.append("p.dia_visita=?"); params.append(fil_dia)\n'
          '    if fil_freq != "Todas":\n'
          '        where.append("p.frequencia_visita=?"); params.append(fil_freq)\n'
          '    if fil_cli[0]:\n'
          '        where.append("p.cliente_id=?"); params.append(fil_cli[0])')

if antigo in c:
    c = c.replace(antigo, novo)
    print("OK: roteiro visitas filtrado por perfil")
else:
    print("AVISO: padrao nao encontrado")

with open('visitas.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c)
    print("Sintaxe OK")
    subprocess.run(["git","add","visitas.py"])
    r = subprocess.run(["git","commit","-m","fix: roteiro visitas filtrado por perfil"],
                       capture_output=True, text=True)
    print("Commit:", r.stdout.strip() or r.stderr.strip())
    r2 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r2.stdout.strip() or r2.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
