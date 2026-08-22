c = open('contatos.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')

# Busca todas as abas definidas no modulo
print("=== Abas definidas ===")
for i, l in enumerate(linhas, 1):
    if '"msg"' in l or "'msg'" in l or 'mensag' in l.lower() or \
       ('ABAS' in l and '{' in l) or ('abas' in l.lower() and ':' in l):
        print(f"  {i}: {l.rstrip()}")

# Busca o dicionario de abas
print("\n=== Dicionario de navegacao ===")
for i in range(60, 80):
    print(f"  {i+1}: {linhas[i].rstrip()}")
