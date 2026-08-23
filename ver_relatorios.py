c = open('relatorios.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')
print(f"Total linhas: {len(linhas)}")

print("\n=== WHEREs e params sem filtro de perfil ===")
for i, l in enumerate(linhas, 1):
    if ('where' in l.lower() and ('= []' in l or '= [' in l)) or \
       'params_base' in l or 'params_nao' in l:
        tem = any(x in '\n'.join(linhas[max(0,i-3):i+3])
                 for x in ['get_where','get_lista','vendedor_id','_uid'])
        print(f"  {'OK' if tem else 'FALTA'} linha {i}: {l.rstrip()}")
