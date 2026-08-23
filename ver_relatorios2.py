c = open('relatorios.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')

print("=== Linha 850-875 (nao_apresentados) ===")
for i in range(849, 876):
    if i < len(linhas):
        print(f"  {i+1}: {linhas[i].rstrip()}")

print("\n=== Linha 1298-1310 (where_p) ===")
for i in range(1297, 1312):
    if i < len(linhas):
        print(f"  {i+1}: {linhas[i].rstrip()}")
