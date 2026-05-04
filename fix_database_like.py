#!/usr/bin/env python3
import pathlib

src = pathlib.Path("database.py").read_text(encoding="utf-8")
original = src

# A solucao correta: os params com % ja funcionam no psycopg2 
# porque ele usa mogrify/execute com params separados
# O problema pode ser outro - vamos ver como params e passado

# Verifica se o problema e que b = f"%Viena%" passa como string
# e o psycopg2 nao consegue usar com %s

# Fix: no _traduzir_sql_pg, escapar % duplo apos substituir ?
OLD = '    sql = sql.replace("?", "%s")'
NEW = '    sql = sql.replace("?", "%s")\n    # Escapa % literais no SQL (nao sao parametros)\n    # Nota: %s ja foi inserido, entao escapamos apenas os outros %\n    import re\n    sql = re.sub(r\'%(?!s)\', \'%%\', sql)'

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    pathlib.Path("database.py").write_text(src, encoding="utf-8")
    print("OK database.py")
else:
    print("NAO ENCONTRADO")
