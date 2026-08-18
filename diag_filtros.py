# Conta quantas vezes cada arquivo busca clientes sem filtro
import os

arquivos = ['cadastros.py','contatos.py','pesquisa.py','visitas.py','relatorios.py','roteiros.py']

for arq in arquivos:
    if not os.path.exists(arq): continue
    c = open(arq,'rb').read().decode('utf-8',errors='replace')
    linhas = c.split('\n')
    sem_filtro = []
    for i,l in enumerate(linhas,1):
        if ('FROM cliente' in l or 'from cliente' in l.lower()) and \
           'vendedor_id' not in l and 'att_promotor' not in l and \
           'cliente_id=' not in l and 'WHERE cliente_id' not in l:
            sem_filtro.append(f"  {i}: {l.strip()}")
    print(f"\n=== {arq} — {len(sem_filtro)} queries sem filtro ===")
    for s in sem_filtro[:10]:
        print(s)
