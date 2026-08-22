c = open('contatos.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')

# Busca funcoes das abas
abas = ['novo', 'follow', 'fornecedor', 'mensagem', 'msg']
print("=== Funcoes das abas ===")
for i, l in enumerate(linhas, 1):
    if any(f'def _' in l.lower() and x in l.lower() for x in abas):
        print(f"  {i}: {l.rstrip()}")

# Busca queries de cliente nessas abas
print("\n=== Queries FROM cliente sem filtro ===")
for i, l in enumerate(linhas, 1):
    if 'FROM cliente' in l and 'get_where' not in l:
        # Mostra contexto
        print(f"\n  linha {i}: {l.rstrip()}")
        if i > 1: print(f"  linha {i-1}: {linhas[i-2].rstrip()}")
        if i < len(linhas): print(f"  linha {i+1}: {linhas[i].rstrip()}")
