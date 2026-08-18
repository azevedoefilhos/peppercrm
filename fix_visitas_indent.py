import ast, subprocess

with open('visitas.py', 'r', encoding='utf-8') as f:
    vv = f.read()

# Corrige a indentacao errada
antigo = ('        from permissoes import get_lista_clientes\n'
          '    clientes = get_lista_clientes(so_ativos=True)\n'
          '        if not clientes:')

novo   = ('        from permissoes import get_lista_clientes\n'
          '        clientes = get_lista_clientes(so_ativos=True)\n'
          '        if not clientes:')

if antigo in vv:
    vv = vv.replace(antigo, novo)
    print("OK: indentacao corrigida")
else:
    print("AVISO: padrao nao encontrado, buscando variante...")
    # Busca qualquer ocorrencia do problema
    linhas = vv.split('\n')
    for i, l in enumerate(linhas):
        if 'get_lista_clientes' in l and l.startswith('    c'):
            print(f"  linha {i+1}: {repr(l)}")
            linhas[i] = l.replace('    clientes', '        clientes')
            print(f"  corrigido: {repr(linhas[i])}")
    vv = '\n'.join(linhas)

with open('visitas.py', 'w', encoding='utf-8') as f:
    f.write(vv)

try:
    ast.parse(vv)
    print("Sintaxe OK")
    subprocess.run(["git","add","visitas.py"])
    r = subprocess.run(["git","commit","-m","fix: visitas.py indentacao get_lista_clientes"],
                       capture_output=True, text=True)
    print("Commit:", r.stdout.strip() or r.stderr.strip())
    r2 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r2.stdout.strip() or r2.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
    linhas = vv.split('\n')
    for i, l in enumerate(linhas[max(0,e.lineno-3):e.lineno+2], max(0,e.lineno-3)+1):
        print(f"  {i}: {repr(l)}")
