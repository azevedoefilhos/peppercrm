# Adiciona debug no crm_app.py lendo o arquivo do disco
with open('crm_app.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Mostra contexto do titulo
linhas = c.split('\n')
for i, l in enumerate(linhas, 1):
    if 'nome_empresa' in l or ('title' in l.lower() and 'st.' in l):
        print(f"  {i}: {l.strip()}")

# Adiciona debug antes do primeiro botao do menu
antigo = 'if pagina == "home":'
idx = c.find(antigo)
if idx >= 0:
    # Pega a linha seguinte
    fim_linha = c.find('\n', idx) + 1
    novo_bloco = (antigo + '\n'
        '    from permissoes import usuario_atual\n'
        '    _u = usuario_atual()\n'
        '    import streamlit as st\n'
        '    st.sidebar.caption(f"Sessao: tipo={_u.get(\'tipo\',\'?\')}'
        ' id={_u.get(\'id\',\'?\')} eid={_u.get(\'empresa_id\',\'?\')}") \n')
    c2 = c.replace(antigo, novo_bloco, 1)
    with open('crm_app.py', 'w', encoding='utf-8') as f:
        f.write(c2)
    print("OK: debug na sidebar")
else:
    print("AVISO: pagina home nao encontrado")
