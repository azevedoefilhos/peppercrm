import ast, subprocess

with open('visitas.py', 'r', encoding='utf-8') as f:
    vv = f.read()

# Corrige TODAS as ocorrencias do problema de indentacao
# O padrao errado e: 8 espacos + from permissoes, depois 4 espacos + clientes =
linhas = vv.split('\n')
corrigidas = 0
for i in range(len(linhas)-1):
    l_atual = linhas[i]
    l_prox  = linhas[i+1]
    # Detecta: linha com 8 espacos de import seguida de linha com 4 espacos de clientes
    if ('from permissoes import get_lista_clientes' in l_atual and
        l_atual.startswith('        ') and  # 8 espacos
        l_prox.strip().startswith('clientes = get_lista_clientes') and
        l_prox.startswith('    clientes')):  # apenas 4 espacos
        # Corrige para 8 espacos
        linhas[i+1] = '        ' + l_prox.lstrip()
        corrigidas += 1
        print(f"  Linha {i+2} corrigida: {repr(linhas[i+1])}")

print(f"Total corrigido: {corrigidas} linha(s)")
vv = '\n'.join(linhas)

with open('visitas.py', 'w', encoding='utf-8') as f:
    f.write(vv)

try:
    ast.parse(vv)
    print("Sintaxe OK")
    subprocess.run(["git","add","visitas.py"])
    r = subprocess.run(["git","commit","-m","fix: visitas.py todas as indentacoes corrigidas"],
                       capture_output=True, text=True)
    print("Commit:", r.stdout.strip() or r.stderr.strip())
    r2 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r2.stdout.strip() or r2.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
    linhas2 = vv.split('\n')
    for i, l in enumerate(linhas2[max(0,e.lineno-3):e.lineno+2], max(0,e.lineno-3)+1):
        print(f"  {i}: {repr(l)}")
