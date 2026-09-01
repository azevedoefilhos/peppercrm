r = __import__('subprocess').run(['git','show','HEAD:roteiros.py'], capture_output=True)
c = r.stdout.decode('utf-8', errors='replace')
linhas = c.split('\n')

# Ver funcao _tela_setores completa
ini = next(i for i,l in enumerate(linhas) if 'def _tela_setores' in l)
fim = next(i for i,l in enumerate(linhas[ini+1:], ini+1) if l.startswith('def ') or l.startswith('# ═'))
print(f"_tela_setores: linhas {ini+1} ate {fim+1}")
for i in range(ini, fim):
    print(f"  {i+1}: {linhas[i].rstrip()}")
