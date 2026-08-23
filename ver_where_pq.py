c = open('pesquisa.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')
for i in range(218, 237):
    print(f"  {i+1}: {linhas[i].rstrip()}")
