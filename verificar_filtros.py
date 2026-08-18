import os
arquivos = {
    'pesquisa.py': ['e_vendedor', 'vendedor_id', 'uid_pq', '_uid_pq'],
    'contatos.py': ['e_vendedor', 'vendedor_id', 'uid_cont', '_uid_cont'],
    'visitas.py':  ['e_vendedor', 'vendedor_id', 'uid_vis', '_uid_vis'],
    'roteiros.py': ['e_vendedor', 'vendedor_id', 'uid_rot', '_uid_rot'],
}
for arq, chaves in arquivos.items():
    if os.path.exists(arq):
        c = open(arq, 'rb').read().decode('utf-8', errors='replace')
        print(f"\n=== {arq} ({len(c)} bytes) ===")
        for chave in chaves:
            print(f"  {chave}: {chave in c}")
    else:
        print(f"\n{arq}: NAO ENCONTRADO")
