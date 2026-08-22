c = open('pesquisa.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')
print(f"Total linhas: {len(linhas)}")

print("\n=== Queries de cliente sem filtro ===")
for i, l in enumerate(linhas, 1):
    if 'FROM cliente' in l or 'cliente_id' in l and 'SELECT' in l:
        tem_filtro = any(x in '\n'.join(linhas[max(0,i-5):i+3]) 
                        for x in ['get_where', 'get_lista', 'vendedor_id', '_uid'])
        status = 'OK' if tem_filtro else 'FALTA'
        print(f"  {status} linha {i}: {l.rstrip()}")
