c = open('roteiros.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')
print(f"Linhas: {len(linhas)}")
for i, l in enumerate(linhas, 1):
    if 'def ' in l:
        print(f"  {i}: {l.strip()}")
