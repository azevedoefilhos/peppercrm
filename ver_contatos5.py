c = open('contatos.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')

print("=== Aba Novo (linha 1576-1650) ===")
for i in range(1575, 1650):
    if i < len(linhas):
        print(f"  {i+1}: {linhas[i].rstrip()}")

print("\n=== Follow-ups (busca def _follow ou similar) ===")
for i, l in enumerate(linhas, 1):
    if 'follow' in l.lower() or 'acompan' in l.lower():
        print(f"  {i}: {l.rstrip()}")

print("\n=== Por Fornecedor _por_fornecedor (linha 2342+) ===")
for i in range(2341, 2420):
    if i < len(linhas):
        l = linhas[i]
        if any(x in l for x in ['cliente', 'FROM', 'where', 'query', 'SELECT']):
            print(f"  {i+1}: {l.rstrip()}")

print("\n=== Mensagens (busca def _mensagem ou msg) ===")
for i, l in enumerate(linhas, 1):
    if 'mensagem' in l.lower() or ('msg' in l.lower() and 'def' in l.lower()):
        print(f"  {i}: {l.rstrip()}")
