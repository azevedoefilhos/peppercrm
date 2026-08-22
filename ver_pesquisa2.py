c = open('pesquisa.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')

for bloco in [(200, 215), (360, 375), (760, 775), (4065, 4080)]:
    print(f"\n=== Linhas {bloco[0]}-{bloco[1]} ===")
    for i in range(bloco[0]-1, bloco[1]):
        if i < len(linhas):
            print(f"  {i+1}: {linhas[i].rstrip()}")
