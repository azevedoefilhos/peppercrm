c = open('contatos.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')

print("=== Follow-ups linha 1815-1840 ===")
for i in range(1814, 1842):
    if i < len(linhas):
        print(f"  {i+1}: {linhas[i].rstrip()}")

print("\n=== Por Fornecedor linha 2355-2395 ===")
for i in range(2354, 2408):
    if i < len(linhas):
        print(f"  {i+1}: {linhas[i].rstrip()}")

print("\n=== Mensagens — busca por 'mensagem' ou 'modelo' ===")
for i, l in enumerate(linhas, 1):
    if 'mensagem' in l.lower() or 'modelo' in l.lower():
        if 'def ' in l or 'subheader' in l or 'selectbox' in l:
            print(f"  {i}: {l.rstrip()}")
