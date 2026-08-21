c = open('cadastros.py', encoding='utf-8').read()
linhas = c.split('\n')
for i, l in enumerate(linhas, 1):
    if 2524 <= i <= 2560:
        print(f"  {i}: {l.rstrip()}")
