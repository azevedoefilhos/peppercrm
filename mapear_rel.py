c = open('relatorios.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')

print("=== Todas as funcoes de relatorio ===")
for i, l in enumerate(linhas, 1):
    if l.startswith('def _rel_') or l.startswith('def tela_'):
        print(f"  {i}: {l.rstrip()}")

print("\n=== WHEREs inicializados sem filtro de perfil ===")
for i, l in enumerate(linhas, 1):
    if ('where' in l.lower() and ('= []' in l or '= ["' in l or "= ['" in l)) or \
       ('params' in l.lower() and '= []' in l):
        bloco = '\n'.join(linhas[max(0,i-2):i+4])
        tem = any(x in bloco for x in ['get_where','get_lista','_w_rel','vendedor_id'])
        if not tem:
            print(f"  FALTA linha {i}: {l.rstrip()}")
