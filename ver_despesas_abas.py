c = open('despesas.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')

# Busca menu de abas e dispatcher
print("=== Menu e abas de despesas ===")
for i, l in enumerate(linhas, 1):
    if 'ABAS' in l or 'resultado' in l.lower() or '"res"' in l or "'res'" in l or \
       'tela_resultado' in l or 'aba' in l.lower() and ('=' in l or ':' in l):
        print(f"  {i}: {l.rstrip()}")
