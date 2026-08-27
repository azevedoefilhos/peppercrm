import ast, subprocess

with open('cadastros.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Corrige a linha que usa get_lista_clientes sem import
antigo = ('    from permissoes import get_lista_clientes\n'
          '    clientes_all = get_lista_clientes(so_ativos=False) or []')

# Verifica se ja existe
if antigo in c:
    print("OK: import ja existe")
else:
    # Busca a linha sem import
    antigo2 = '    clientes_all = get_lista_clientes(so_ativos=False) or []'
    novo2   = ('    from permissoes import get_lista_clientes\n'
               '    clientes_all = get_lista_clientes(so_ativos=False) or []')
    n = c.count(antigo2)
    print(f"Ocorrencias sem import: {n}")
    if n > 0:
        c = c.replace(antigo2, novo2)
        print("OK: import adicionado")
    else:
        print("AVISO: padrao nao encontrado")

with open('cadastros.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c); print("Sintaxe OK")
    subprocess.run(["git","add","cadastros.py"])
    r = subprocess.run(["git","commit","-m","fix: import get_lista_clientes faltando em cadastros PDVs"],
                       capture_output=True, text=True)
    print("Commit:", r.stdout.strip() or r.stderr.strip())
    r2 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r2.stdout.strip() or r2.stderr.strip())
except SyntaxError as e:
    print(f"ERRO: {e}")
