# Versao sem caracteres especiais no output
import os, sys

def buscar(fname, termos):
    if not os.path.exists(fname): return
    c = open(fname, encoding='utf-8', errors='replace').read()
    linhas = c.split('\n')
    print(f"\n### {fname} ###")
    achados = set()
    for i, l in enumerate(linhas, 1):
        for t in termos:
            if t in l and i not in achados:
                achados.add(i)
                for j in range(max(0,i-1), min(len(linhas),i+2)):
                    try:
                        linha_safe = linhas[j].encode('ascii','replace').decode('ascii')
                        print(f"  {j+1}: {linha_safe}")
                    except:
                        print(f"  {j+1}: [linha com encoding especial]")
                print("  ---")

buscar('cadastros.py',  ['FROM cliente ORDER', 'clientes = query', 'clientes_all'])
buscar('contatos.py',   ['FROM cliente', 'where_cli', 'params_cli'])
buscar('pesquisa.py',   ['todos_cli', 'get_lista', 'FROM cliente ORDER'])
buscar('visitas.py',    ['roteiro', 'clientes = ', 'FROM cliente'])
buscar('relatorios.py', ['where_sql', 'WHERE.*cliente', 'where_params', 'params_nao'])
buscar('despesas.py',   ['FROM cliente', 'clientes', 'cliente_id'])
buscar('roteiros.py',   ['clientes =', 'get_lista', 'FROM cliente'])
