c = open('resultado_operacional.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')

print("=== Funcao _q (bifurcada) linha 60-80 ===")
for i in range(59, 82):
    if i < len(linhas):
        print(f"  {i+1}: {linhas[i].rstrip()}")

print("\n=== Funcao principal tela_ linha 80-170 ===")
for i in range(79, 170):
    if i < len(linhas):
        l = linhas[i]
        if any(x in l for x in ['def ', 'vendedor', 'usuario', 'WHERE', 'FROM pedido',
                                  'FROM despesa', 'comissao', 'params', 'query']):
            print(f"  {i+1}: {l.rstrip()}")
