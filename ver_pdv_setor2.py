c = open('cadastros.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')
for i, l in enumerate(linhas, 1):
    if 4105 <= i <= 4160:
        print(f"  {i}: {l.rstrip()}")
