c = open('permissoes.py', encoding='utf-8').read()
# Mostra funcoes criticas
for fn in ['def usuario_atual', 'def perfil_atual', 'def usuario_id_atual', 
           'def empresa_id_atual', 'def get_where_cliente']:
    idx = c.find(fn)
    if idx >= 0:
        print(f"\n=== {fn} ===")
        print(c[idx:idx+200])
