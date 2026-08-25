c = open('relatorios.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')

print("=== Menu de abas (ABAS_REL) ===")
for i, l in enumerate(linhas, 1):
    if 50 <= i <= 145:
        if 'compet' in l.lower() or 'ABAS' in l or '":' in l or 'elif' in l or 'if a==' in l or 'a ==' in l:
            print(f"  {i}: {l.rstrip()}")
