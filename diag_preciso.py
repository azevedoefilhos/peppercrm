# Encontra EXATAMENTE os padroes que precisam ser corrigidos
import os

def buscar(fname, termos):
    if not os.path.exists(fname): return
    c = open(fname, encoding='utf-8', errors='replace').read()
    linhas = c.split('\n')
    print(f"\n=== {fname} ===")
    for i, l in enumerate(linhas, 1):
        for t in termos:
            if t in l:
                # Mostra 2 linhas de contexto
                inicio = max(0, i-2)
                fim = min(len(linhas), i+2)
                for j in range(inicio, fim):
                    print(f"  {j+1}: {linhas[j]}")
                print("  ---")
                break

buscar('cadastros.py', ['FROM cliente', 'clientes_all', 'SELECT cliente_id'])
buscar('contatos.py', ['FROM cliente', 'where_cli', 'params_cli'])
buscar('pesquisa.py', ['FROM cliente', 'todos_cli', 'get_lista'])
buscar('visitas.py', ['FROM cliente', 'roteiro', 'clientes ='])
buscar('relatorios.py', ['FROM cliente', 'where_sql', 'where_params'])
buscar('despesas.py', ['FROM cliente', 'clientes', 'cliente_id'])
buscar('roteiros.py', ['FROM cliente', 'clientes =', 'get_lista'])
