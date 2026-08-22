c = open('contatos.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')

print("=== Linha 140-150 (where inicial) ===")
for i in range(138, 155):
    print(f"  {i+1}: {linhas[i].rstrip()}")

print("\n=== Linha 1880-1892 (contatos recentes) ===")
for i in range(1877, 1895):
    print(f"  {i+1}: {linhas[i].rstrip()}")

print("\n=== Linha 2063-2070 (cidades) ===")
for i in range(2060, 2072):
    print(f"  {i+1}: {linhas[i].rstrip()}")
