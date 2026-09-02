r = __import__('subprocess').run(['git','show','HEAD:roteiros.py'], capture_output=True)
c = r.stdout.decode('utf-8', errors='replace')
linhas = c.split('\n')
# Busca queries de supervisor no roteiro
for i, l in enumerate(linhas, 1):
    if 'supervisor_promotor' in l or 'sup_id' in l or 'promotor_id' in l and 'sup' in c[max(0,i-200):i+200].lower():
        print(f"  {i}: {l.rstrip()}")
