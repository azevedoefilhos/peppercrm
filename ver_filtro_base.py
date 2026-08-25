c = open('relatorios.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')

print("=== _FILTRO_BASE ===")
idx = c.find('_FILTRO_BASE')
for i, l in enumerate(linhas, 1):
    if '_FILTRO_BASE' in l and i < 50:
        print(f"  {i}: {l.rstrip()}")

# Mostra definicao
for i in range(0, 50):
    if '_FILTRO_BASE' in linhas[i]:
        for j in range(max(0,i-1), min(len(linhas), i+15)):
            print(f"  {j+1}: {linhas[j].rstrip()}")
        break

print("\n=== _rel_competitivo linha 1320-1380 ===")
for i in range(1319, 1385):
    if i < len(linhas):
        print(f"  {i+1}: {linhas[i].rstrip()}")
