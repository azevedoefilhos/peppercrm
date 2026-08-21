# Adiciona debug no modulo Clientes para ver o que get_lista_clientes retorna
with open('cadastros.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Busca onde get_lista_clientes e chamado
idx = c.find('get_lista_clientes')
print(f"Primeira ocorrencia em linha:", c[:idx].count('\n')+1)
print(f"Contexto:", repr(c[idx:idx+100]))

# Adiciona debug temporario apos a chamada
antigo = '''    from permissoes import get_lista_clientes
    _clis_vinc = get_lista_clientes(so_ativos=False)
    clientes = [(r[0], f"{r[1]} ({r[1]})") for r in _clis_vinc] if _clis_vinc else []'''

novo = '''    from permissoes import get_lista_clientes, get_where_cliente, perfil_atual, usuario_id_atual
    _where_dbg, _params_dbg = get_where_cliente("c")
    st.caption(f"DEBUG filtro: perfil={perfil_atual()} uid={usuario_id_atual()} where={repr(_where_dbg)} params={_params_dbg}")
    _clis_vinc = get_lista_clientes(so_ativos=False)
    st.caption(f"DEBUG clientes: {len(_clis_vinc) if _clis_vinc else 0} encontrados")
    clientes = [(r[0], f"{r[1]} ({r[1]})") for r in _clis_vinc] if _clis_vinc else []'''

if antigo in c:
    c = c.replace(antigo, novo, 1)
    print("OK: debug adicionado em vinculos")
else:
    print("AVISO: padrao nao encontrado")

with open('cadastros.py', 'w', encoding='utf-8') as f:
    f.write(c)

import ast
try:
    ast.parse(c); print("Sintaxe OK")
except SyntaxError as e:
    print(f"ERRO: {e}")
