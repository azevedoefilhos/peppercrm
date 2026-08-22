c = open('contatos.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')

# Busca todas as queries de clientes em contatos.py
print("=== Todas as queries de cliente/selectbox cliente ===")
for i, l in enumerate(linhas, 1):
    if ('SELECT' in l and 'cliente_id' in l and 'nome_fantasia' in l) or \
       ('selectbox' in l.lower() and 'cli' in l.lower()):
        print(f"\n  {i}: {l.rstrip()}")
        for j in range(max(0,i-2), min(len(linhas), i+3)):
            if j+1 != i:
                print(f"  {j+1}: {linhas[j].rstrip()}")
