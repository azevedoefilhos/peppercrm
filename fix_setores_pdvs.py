import ast, subprocess

r = subprocess.run(['git','show','HEAD:roteiros.py'], capture_output=True)
c = r.stdout.decode('utf-8', errors='replace').replace('\r\n','\n')

# Ver query atual de setores
idx = c.find('resumo = query')
print("Query atual:")
print(repr(c[idx:idx+400]))
print()

# A query tem LEFT JOIN cliente cli — isso causa o problema
# Cada PDV que nao tem cliente com empresa_id correspondente some
# Solucao: remover o LEFT JOIN cli completamente — setor ja filtra por empresa
antigo = c[idx:idx+400]

# Encontra o fim exato da query
fim_query = c.find(') or []', idx) + 7
query_completa = c[idx:fim_query]
print(f"Query completa ({len(query_completa)} chars):")
print(query_completa)
