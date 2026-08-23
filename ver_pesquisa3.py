c = open('pesquisa.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')

# Busca a query que lista pesquisas com todos os clientes
print("=== Queries de listagem de pesquisas ===")
for i, l in enumerate(linhas, 1):
    if ('pesquisa_preco' in l or 'pq_full' in l) and 'SELECT' in l:
        tem_filtro = any(x in '\n'.join(linhas[max(0,i-5):i+5])
                        for x in ['get_where', 'vendedor_id', '_uid', '_w_'])
        print(f"\n  {'OK' if tem_filtro else 'FALTA'} linha {i}: {l.rstrip()}")
        for j in range(max(0,i-1), min(len(linhas), i+6)):
            if j+1 != i:
                print(f"    {j+1}: {linhas[j].rstrip()}")
