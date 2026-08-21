import ast, subprocess

with open('cadastros.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Corrige where_p para incluir filtro de perfil
antigo = '''    # ── QUERY com todos os filtros ────────────────────────────────────────
    where_p = ["1=1"]; params_p = []
    if cli_fil[0]:
        where_p.append("p.cliente_id=?");            params_p.append(cli_fil[0])'''

novo = '''    # ── QUERY com todos os filtros ────────────────────────────────────────
    from permissoes import get_where_cliente
    _w_pdv, _p_pdv = get_where_cliente("c")
    where_p = ["1=1"]; params_p = list(_p_pdv)
    if _w_pdv:
        where_p.append(_w_pdv.lstrip("AND ").strip())
    if cli_fil[0]:
        where_p.append("p.cliente_id=?");            params_p.append(cli_fil[0])'''

if antigo in c:
    c = c.replace(antigo, novo)
    print("OK: filtro PDVs por perfil adicionado")
else:
    print("AVISO: padrao nao encontrado")
    # Mostra contexto
    idx = c.find('where_p = ["1=1"]')
    if idx > 0:
        print(f"Linha: {c[:idx].count(chr(10))+1}")
        print(f"Contexto: {repr(c[idx-50:idx+100])}")

# Remove debug temporario adicionado anteriormente
antigo_dbg = '''    from permissoes import get_lista_clientes, get_where_cliente, perfil_atual, usuario_id_atual
    _where_dbg, _params_dbg = get_where_cliente("c")
    st.caption(f"DEBUG filtro: perfil={perfil_atual()} uid={usuario_id_atual()} where={repr(_where_dbg)} params={_params_dbg}")
    _clis_vinc = get_lista_clientes(so_ativos=False)
    st.caption(f"DEBUG clientes: {len(_clis_vinc) if _clis_vinc else 0} encontrados")
    clientes = [(r[0], f"{r[1]} ({r[1]})") for r in _clis_vinc] if _clis_vinc else []'''

novo_dbg = '''    from permissoes import get_lista_clientes
    _clis_vinc = get_lista_clientes(so_ativos=False)
    clientes = [(r[0], f"{r[1]} ({r[1]})") for r in _clis_vinc] if _clis_vinc else []'''

if antigo_dbg in c:
    c = c.replace(antigo_dbg, novo_dbg)
    print("OK: debug removido")

with open('cadastros.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c); print("Sintaxe OK")
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
    return

subprocess.run(["git","add","cadastros.py"])
r = subprocess.run(["git","commit","-m","fix: PDVs filtrado por perfil na aba PDVs"],
                   capture_output=True, text=True)
print("Commit:", r.stdout.strip() or r.stderr.strip())
r2 = subprocess.run(["git","push"], capture_output=True, text=True)
print("Push:", r2.stdout.strip() or r2.stderr.strip())
