# Adiciona debug na tela home para ver perfil real do usuario logado
with open('crm_app.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Adiciona debug logo apos o header do home
antigo = '    st.title(f"{_nome_empresa()}")'
novo   = '''    st.title(f"{_nome_empresa()}")
    # DEBUG TEMPORARIO - remover apos confirmar
    from permissoes import perfil_atual, usuario_id_atual, usuario_atual
    _u = usuario_atual()
    st.caption(f"DEBUG sessao: tipo={_u.get('tipo','?')} id={_u.get('id','?')} empresa_id={_u.get('empresa_id','?')}")'''

if antigo in c:
    c = c.replace(antigo, novo, 1)
    print("OK: debug adicionado")
else:
    print("AVISO: padrao nao encontrado")

with open('crm_app.py', 'w', encoding='utf-8') as f:
    f.write(c)

import ast
try:
    ast.parse(c); print("Sintaxe OK")
except SyntaxError as e:
    print(f"ERRO: {e}")
