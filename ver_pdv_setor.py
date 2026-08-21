c = open('cadastros.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')

# Busca PDVs por Setor e Central de Compras
print("=== PDVs por Setor ===")
for i, l in enumerate(linhas, 1):
    if 2700 <= i <= 2800:
        if any(x in l for x in ['where', 'WHERE', 'cliente', 'pdv', 'setor', 'params']):
            print(f"  {i}: {l.rstrip()}")

print("\n=== Central de Compras ===")
for i, l in enumerate(linhas, 1):
    if 3050 <= i <= 3120:
        print(f"  {i}: {l.rstrip()}")
