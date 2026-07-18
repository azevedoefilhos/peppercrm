# Adiciona debug temporario na _tela_vendedores
with open('equipe.py', 'r', encoding='utf-8') as f:
    c = f.read()

antigo = '''    vends = vends_u

    if st.session_state.get("eq_vend_msg"):'''

novo = '''    vends = vends_u

    # DEBUG TEMPORARIO
    st.write(f"DEBUG: eid={eid} | vends_u={len(vends_u)} | vends_leg={len(vends_leg)}")

    if st.session_state.get("eq_vend_msg"):'''

if antigo in c:
    c = c.replace(antigo, novo)
    print("OK: debug adicionado")
else:
    print("ERRO: padrao nao encontrado")

with open('equipe.py', 'w', encoding='utf-8') as f:
    f.write(c)
