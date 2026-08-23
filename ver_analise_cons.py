c = open('pesquisa.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')

# Busca a funcao de analise consolidada
print("=== Funcao analise consolidada ===")
for i, l in enumerate(linhas, 1):
    if 'analise' in l.lower() and ('def ' in l or 'subheader' in l or 'header' in l):
        print(f"  {i}: {l.rstrip()}")

# Busca where_base (usado na analise consolidada)
print("\n=== where_base ===")
for i, l in enumerate(linhas, 1):
    if 'where_base' in l:
        print(f"  {i}: {l.rstrip()}")
