c = open('contatos.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')
# Busca aba mensagens
for i, l in enumerate(linhas, 1):
    if 'mensagem' in l.lower() or 'whatsapp' in l.lower() or 'modelo' in l.lower():
        if any(x in l for x in ['def ', 'subheader', 'header', 'selectbox', 'cliente_id', 'FROM']):
            print(f"  {i}: {l.rstrip()}")
