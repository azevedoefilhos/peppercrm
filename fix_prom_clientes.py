import ast, subprocess

r = subprocess.run(['git','show','HEAD:roteiros.py'], capture_output=True)
c = r.stdout.decode('utf-8', errors='replace')

# Mostra o padrao exato atual
idx = c.find('clientes_p = query')
if idx > 0:
    print("Padrao atual:")
    print(repr(c[idx-20:idx+300]))
