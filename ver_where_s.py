c = open('cadastros.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')
for i, l in enumerate(linhas, 1):
    if 4050 <= i <= 4112:
        if any(x in l for x in ['where_s', 'params_s', 'get_where', 'perfil']):
            print(f"  {i}: {l.rstrip()}")
