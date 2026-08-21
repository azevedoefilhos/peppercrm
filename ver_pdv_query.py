c = open('cadastros.py', encoding='utf-8').read()
linhas = c.split('\n')
# Busca a funcao de PDVs
for i, l in enumerate(linhas, 1):
    if 2450 <= i <= 2550:
        if 'pdv' in l.lower() or 'FROM pdv' in l or 'cliente' in l.lower():
            print(f"  {i}: {l.rstrip()}")
