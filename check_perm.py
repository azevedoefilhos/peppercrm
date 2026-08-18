c = open('permissoes.py', encoding='utf-8').read()
print('get_lista_clientes:', 'def get_lista_clientes' in c)
print('get_where_cliente:', 'def get_where_cliente' in c)
# Mostrar as funcoes se existirem
if 'def get_where_cliente' in c:
    idx = c.find('def get_where_cliente')
    print('\nget_where_cliente:')
    print(c[idx:idx+400])
