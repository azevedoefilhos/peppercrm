c = open('resultado_operacional.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')

print("=== _buscar_totais_periodo completo ===")
for i in range(106, 170):
    if i < len(linhas):
        print(f"  {i+1}: {linhas[i].rstrip()}")

print("\n=== tela_resultado_operacional ===")
for i, l in enumerate(linhas, 1):
    if 'def tela_resultado' in l:
        for j in range(i-1, min(len(linhas), i+30)):
            print(f"  {j+1}: {linhas[j].rstrip()}")
        break
