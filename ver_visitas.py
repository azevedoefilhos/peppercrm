c = open('visitas.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')
print(f"Total linhas: {len(linhas)}")

print("\n=== WHEREs e queries sem filtro de perfil ===")
for i, l in enumerate(linhas, 1):
    if ('where' in l.lower() and ('= []' in l or '= ["' in l or "= ['1=1']" in l)) or \
       ('FROM cliente' in l and 'get_where' not in l and 'get_lista' not in l):
        bloco = '\n'.join(linhas[max(0,i-3):i+5])
        tem = any(x in bloco for x in ['get_where','get_lista','vendedor_id','_uid_vis'])
        print(f"  {'OK' if tem else 'FALTA'} linha {i}: {l.rstrip()}")
