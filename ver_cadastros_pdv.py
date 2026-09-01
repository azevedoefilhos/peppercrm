# Ver onde o PDV e editado em cadastros.py
r = __import__('subprocess').run(['git','show','HEAD:cadastros.py'],
    capture_output=True)
c = r.stdout.decode('utf-8', errors='replace')
linhas = c.split('\n')
print(f"Total: {len(linhas)} linhas")

# Busca _form_editar_pdv
for i, l in enumerate(linhas, 1):
    if '_form_editar_pdv' in l or 'def _form_editar' in l:
        print(f"  {i}: {l.strip()}")

# Busca onde setor aparece no form de PDV
for i, l in enumerate(linhas, 1):
    if 'setor' in l.lower() and ('input' in l.lower() or 'select' in l.lower() or 'key=' in l):
        print(f"  {i}: {l.strip()}")
