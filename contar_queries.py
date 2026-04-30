#!/usr/bin/env python3
import pathlib

arquivos = ['crm_app.py','pesquisa.py','cadastros.py','relatorios.py',
            'comissoes.py','contatos.py','pedido.py','ver_pedidos.py',
            'analise_competitiva.py','mix_analise.py','concorrentes.py',
            'configuracao.py','catalogo.py']

total = 0
for arq in arquivos:
    try:
        src = pathlib.Path(arq).read_text(encoding='utf-8')
        n_query = src.count('query(')
        n_conn  = src.count('conectar()')
        n_exec  = src.count('conn.execute(') + src.count('cur.execute(')
        print(f"{arq}: {n_query} query() + {n_conn} conectar() + {n_exec} execute() direto")
        total += n_query + n_conn
    except Exception as e:
        print(f"{arq}: ERRO {e}")

print(f"\nTotal chamadas DB: {total}")
