c = open('catalogo.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')
print(f"Total linhas: {len(linhas)}")

# Localiza _tela_mensagens
for i, l in enumerate(linhas, 1):
    if '_tela_mensagens' in l or 'def _tela_mensagens' in l:
        print(f"  {i}: {l.rstrip()}")

# Mostra contexto da funcao
idx = c.find('def _tela_mensagens')
if idx >= 0:
    linha_inicio = c[:idx].count('\n') + 1
    print(f"\n=== _tela_mensagens (linha {linha_inicio}) ===")
    for i in range(linha_inicio-1, min(len(linhas), linha_inicio+50)):
        print(f"  {i+1}: {linhas[i].rstrip()}")
