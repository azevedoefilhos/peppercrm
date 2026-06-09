# verificar_contatos.py
f = open('contatos.py', encoding='utf-8').read()
print('r[6] OK:', 'r[6] not in (0, False, None)' in f)
print('r[ativo] ainda existe:', "r['ativo']" in f)
# Mostra as linhas com filtro de ativo
for i, l in enumerate(f.splitlines(), 1):
    if 'ativo' in l and ('filter' in l.lower() or 'r[6]' in l or "r['ativo']" in l):
        print(f"  linha {i}: {l.strip()}")
