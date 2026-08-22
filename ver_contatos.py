c = open('contatos.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')
print(f"Total linhas: {len(linhas)}")
print("\n=== Todos os WHEREs e queries de cliente ===")
for i, l in enumerate(linhas, 1):
    if any(x in l for x in ['FROM cliente', 'where_cli', 'where =', 'params =', 
                              'get_where', 'get_lista', 'vendedor_id', 'perfil']):
        print(f"  {i}: {l.rstrip()}")
