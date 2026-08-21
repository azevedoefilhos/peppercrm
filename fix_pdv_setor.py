import ast, subprocess

with open('cadastros.py', 'r', encoding='utf-8') as f:
    c = f.read()

antigo = ("    where_s  = [\"COALESCE(p.status,'Ativo') NOT IN ('Inativo','Encerrado','Suspenso')\"]\n"
          "    params_s = []")

novo   = ("    from permissoes import get_where_cliente\n"
          "    _w_s, _p_s = get_where_cliente(\"c\")\n"
          "    where_s  = [\"COALESCE(p.status,'Ativo') NOT IN ('Inativo','Encerrado','Suspenso')\"]\n"
          "    params_s = list(_p_s)\n"
          "    if _w_s: where_s.append(_w_s.lstrip('AND ').strip())")

if antigo in c:
    c = c.replace(antigo, novo, 1)
    print("OK: PDVs por Setor filtrado por perfil")
else:
    print("AVISO: padrao nao encontrado")

with open('cadastros.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c)
    print("Sintaxe OK")
    subprocess.run(["git","add","cadastros.py"])
    r = subprocess.run(["git","commit","-m","fix: PDVs por Setor filtrado por perfil"],
                       capture_output=True, text=True)
    print("Commit:", r.stdout.strip() or r.stderr.strip())
    r2 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r2.stdout.strip() or r2.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
