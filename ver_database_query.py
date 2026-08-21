# Ver como a funcao query() trata os placeholders
c = open('database.py', encoding='utf-8').read()
# Mostra _traduzir_sql_pg
idx = c.find('def _traduzir_sql_pg')
print("=== _traduzir_sql_pg ===")
print(c[idx:idx+300])

# Mostra funcao query
idx2 = c.find('\ndef query(')
print("\n=== query() ===")
print(c[idx2:idx2+400])

# Mostra execute_write
idx3 = c.find('\ndef execute_write(')
print("\n=== execute_write() ===")
print(c[idx3:idx3+300])
