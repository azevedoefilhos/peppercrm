c = open('relatorios.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')

for linha_alvo in [150, 245, 305, 363, 434, 606, 668]:
    print(f"\n=== Linha {linha_alvo} ===")
    for i in range(linha_alvo-2, linha_alvo+8):
        if 0 <= i < len(linhas):
            print(f"  {i+1}: {linhas[i].rstrip()}")
