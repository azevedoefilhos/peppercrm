c = open('despesas.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')
print(f"Total linhas: {len(linhas)}")

print("\n=== WHEREs e queries sem filtro ===")
for i, l in enumerate(linhas, 1):
    if ('where' in l.lower() and ('= []' in l or '= ["' in l or "= ['" in l)) or \
       'usuario_id' in l or 'get_where' in l or 'get_lista' in l:
        print(f"  {i}: {l.rstrip()}")
