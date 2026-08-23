import ast, subprocess

with open('relatorios.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Remove a segunda chamada duplicada de get_where_cliente
# que usa 'params' (nao definido) em vez de 'where_params'
antigo = ('    from permissoes import get_where_cliente\n'
          '    _w_rel, _p_rel = get_where_cliente("c")\n'
          '    if _w_rel: where.append(_w_rel.lstrip("AND ").strip()); params.extend(_p_rel)\n'
          '    where_sql = ("WHERE " + " AND ".join(where)) if where else ""')

novo   = ('    where_sql = ("WHERE " + " AND ".join(where)) if where else ""')

if antigo in c:
    c = c.replace(antigo, novo, 1)
    print("OK: duplicata get_where_cliente removida (causava NameError)")
else:
    print("AVISO: padrao nao encontrado")
    # Mostra contexto
    idx = c.find('params.extend(_p_rel)')
    if idx > 0:
        linha = c[:idx].count('\n') + 1
        print(f"  Linha {linha}: {repr(c[idx-50:idx+60])}")

with open('relatorios.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c)
    print("Sintaxe OK")
    subprocess.run(["git","add","relatorios.py"])
    r = subprocess.run(["git","commit","-m","fix: relatorios remove duplicata get_where_cliente que causava NameError"],
                       capture_output=True, text=True)
    print("Commit:", r.stdout.strip() or r.stderr.strip())
    r2 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r2.stdout.strip() or r2.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
