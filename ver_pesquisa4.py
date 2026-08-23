c = open('pesquisa.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')

# Busca where de listagem de pesquisas (where_pq, where_lista, etc)
print("=== WHERE de listagem principal ===")
for i, l in enumerate(linhas, 1):
    if ('where_pq' in l or 'where_lista' in l or 'fil_cli' in l or
        'fil_per' in l or 'periodo' in l.lower()) and \
       ('=' in l or 'append' in l):
        print(f"  {i}: {l.rstrip()}")

# Busca a query principal com JOIN cliente
print("\n=== Query principal de listagem ===")
for i, l in enumerate(linhas, 1):
    if 230 <= i <= 290:
        print(f"  {i}: {l.rstrip()}")
