import ast, subprocess

with open('despesas.py', 'r', encoding='utf-8') as f:
    c = f.read()

antigo = ('    ABAS = {"nova":"➕ Nova despesa",\n'
          '            "lista":"📋 Despesas",\n'
          '            "relatorio":"📊 Relatório",\n'
          '            "resultado":"💰 Resultado"}')

novo   = ('    from permissoes import e_representante, e_admin, e_master\n'
          '    _pode_resultado = e_representante() or e_admin() or e_master()\n'
          '    ABAS = {"nova":"➕ Nova despesa",\n'
          '            "lista":"📋 Despesas",\n'
          '            "relatorio":"📊 Relatório"}\n'
          '    if _pode_resultado:\n'
          '        ABAS["resultado"] = "💰 Resultado"')

if antigo in c:
    c = c.replace(antigo, novo)
    print("OK: aba Resultado ocultada para Vendedor/PV")
else:
    print("AVISO: padrao nao encontrado")

with open('despesas.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c); print("Sintaxe OK")
    subprocess.run(["git","add","despesas.py"])
    r = subprocess.run(["git","commit","-m","fix: aba Resultado de Despesas oculta para Vendedor"],
                       capture_output=True, text=True)
    print("Commit:", r.stdout.strip() or r.stderr.strip())
    r2 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r2.stdout.strip() or r2.stderr.strip())
except SyntaxError as e:
    print(f"ERRO: {e}")
