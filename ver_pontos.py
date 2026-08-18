# Ver pontos exatos de filtro em cada arquivo
print("=== pesquisa.py - onde clientes sao listados ===")
c = open('pesquisa.py', 'rb').read().decode('utf-8', errors='replace')
for i, l in enumerate(c.split('\n'), 1):
    if 'todos_cli' in l or ('FROM cliente' in l and 'SELECT' in l):
        print(f"  {i}: {l.strip()}")

print("\n=== contatos.py - where_cli ===")
cc = open('contatos.py', 'rb').read().decode('utf-8', errors='replace')
for i, l in enumerate(cc.split('\n'), 1):
    if 'where_cli' in l or '_uid_cont' in l or '_extra' in l:
        print(f"  {i}: {l.strip()}")

print("\n=== visitas.py - where e clientes ===")
vv = open('visitas.py', 'rb').read().decode('utf-8', errors='replace')
for i, l in enumerate(vv.split('\n'), 1):
    if ('where' in l.lower() and 'visita' not in l.lower() and '=' in l) or \
       'FROM cliente' in l or '_uid_vis' in l:
        print(f"  {i}: {l.strip()}")

print("\n=== roteiros.py - lista vendedores e clientes ===")
rr = open('roteiros.py', 'rb').read().decode('utf-8', errors='replace')
for i, l in enumerate(rr.split('\n'), 1):
    if 'vends' in l or 'clientes' in l or '_uid_rot' in l:
        print(f"  {i}: {l.strip()}")
