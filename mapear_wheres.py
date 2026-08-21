# Mapeia todos os blocos WHERE que nao tem filtro de perfil
import os

arquivos = ['cadastros.py','contatos.py','pesquisa.py','visitas.py','relatorios.py','despesas.py','roteiros.py']

for fname in arquivos:
    if not os.path.exists(fname): continue
    c = open(fname, encoding='utf-8', errors='replace').read()
    linhas = c.split('\n')
    print(f"\n=== {fname} ===")
    for i, l in enumerate(linhas, 1):
        # Busca inicializacao de where sem filtro de perfil
        if ('where' in l.lower() and '= []' in l and 'params' not in l.lower()) or \
           ('where_p = [' in l) or ('where = [' in l) or ('where_cli = [' in l) or \
           ('where_params = [' in l):
            # Verifica se as proximas 5 linhas tem get_where_cliente
            proximo = '\n'.join(linhas[i:i+8])
            tem_filtro = 'get_where_cliente' in proximo or 'get_lista_clientes' in proximo
            print(f"  {'OK' if tem_filtro else 'FALTA'} linha {i}: {l.strip()}")
