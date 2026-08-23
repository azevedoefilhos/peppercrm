import ast, subprocess

with open('pesquisa.py', 'r', encoding='utf-8') as f:
    c = f.read()

cnt = 0

# 1. Corrige where_base sem filtro de perfil
antigo1 = ("    where_base  = [\"pp.status='finalizado'\"]\n"
           "    params_base = []")

novo1   = ("    from permissoes import get_where_cliente\n"
           "    _w_ac, _p_ac = get_where_cliente(\"cli\")\n"
           "    where_base  = [\"pp.status='finalizado'\"]\n"
           "    params_base = list(_p_ac)\n"
           "    if _w_ac: where_base.append(_w_ac.lstrip('AND ').strip())")

if antigo1 in c:
    c = c.replace(antigo1, novo1, 1)
    print("OK: where_base filtrado por perfil")
    cnt += 1
else:
    print("AVISO: padrao where_base nao encontrado")

# 2. Corrige grafia "Analise" -> "Análise"
c = c.replace('st.header("Analise Consolidada de Pesquisas")',
              'st.header("Análise Consolidada de Pesquisas")')
c = c.replace('"Analise Consolidada"', '"Análise Consolidada"')
c = c.replace("'Analise Consolidada'", "'Análise Consolidada'")
print("OK: grafia Análise corrigida")

with open('pesquisa.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c)
    print(f"Sintaxe OK — {cnt} correcoes")
    subprocess.run(["git","add","pesquisa.py"])
    r = subprocess.run(["git","commit","-m","fix: analise consolidada filtrada por perfil + grafia"],
                       capture_output=True, text=True)
    print("Commit:", r.stdout.strip() or r.stderr.strip())
    r2 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r2.stdout.strip() or r2.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
