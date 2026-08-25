c = open('permissoes.py', encoding='utf-8').read()

for perfil in ['VENDEDOR', 'REPRESENTANTE', 'PROMOTOR_VENDEDOR']:
    idx = c.find(f"'{perfil}':")
    if idx > 0:
        trecho = c[idx:idx+300]
        print(f"\n=== {perfil} ===")
        print(trecho)
