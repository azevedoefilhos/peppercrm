import ast, subprocess

arquivos_modificados = []

# 1. Remove debug do crm_app.py (sidebar)
with open('crm_app.py', 'r', encoding='utf-8') as f:
    c = f.read()

antigo_app = ('    # DEBUG TEMPORARIO - remover apos confirmar\n'
              '    from permissoes import perfil_atual, usuario_id_atual, usuario_atual\n'
              '    _u = usuario_atual()\n'
              '    st.sidebar.caption(f"Sessao: tipo={_u.get(\'tipo\',\'?\')} id={_u.get(\'id\',\'?\')} eid={_u.get(\'empresa_id\',\'?\')}") \n')

if antigo_app in c:
    c = c.replace(antigo_app, '')
    print("OK: debug sidebar removido do crm_app.py")
    with open('crm_app.py', 'w', encoding='utf-8') as f:
        f.write(c)
    arquivos_modificados.append('crm_app.py')
else:
    print("-- debug sidebar nao encontrado em crm_app.py")

# 2. Remove debug do cadastros.py (vinculos)
with open('cadastros.py', 'r', encoding='utf-8') as f:
    c = f.read()

antigo_cad = ('    from permissoes import get_lista_clientes, get_where_cliente, perfil_atual, usuario_id_atual\n'
              '    _where_dbg, _params_dbg = get_where_cliente("c")\n'
              '    st.caption(f"DEBUG filtro: perfil={perfil_atual()} uid={usuario_id_atual()} where={repr(_where_dbg)} params={_params_dbg}")\n'
              '    _clis_vinc = get_lista_clientes(so_ativos=False)\n'
              '    st.caption(f"DEBUG clientes: {len(_clis_vinc) if _clis_vinc else 0} encontrados")\n'
              '    clientes = [(r[0], f"{r[1]} ({r[1]})") for r in _clis_vinc] if _clis_vinc else []')

novo_cad = ('    from permissoes import get_lista_clientes\n'
            '    _clis_vinc = get_lista_clientes(so_ativos=False)\n'
            '    clientes = [(r[0], f"{r[1]} ({r[1]})") for r in _clis_vinc] if _clis_vinc else []')

if antigo_cad in c:
    c = c.replace(antigo_cad, novo_cad)
    print("OK: debug vinculos removido do cadastros.py")
    with open('cadastros.py', 'w', encoding='utf-8') as f:
        f.write(c)
    arquivos_modificados.append('cadastros.py')
else:
    print("-- debug vinculos nao encontrado (pode ja ter sido removido)")

# Verifica sintaxe
for fname in arquivos_modificados:
    try:
        ast.parse(open(fname).read())
        print(f"  {fname}: Sintaxe OK")
    except SyntaxError as e:
        print(f"  {fname} ERRO: {e}")

# Commit
if arquivos_modificados:
    subprocess.run(["git","add"] + arquivos_modificados)
    r = subprocess.run(["git","commit","-m","chore: remove debug temporario"],
                       capture_output=True, text=True)
    print("Commit:", r.stdout.strip() or r.stderr.strip())
    r2 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r2.stdout.strip() or r2.stderr.strip())
