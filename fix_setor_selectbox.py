import ast, subprocess

r = subprocess.run(['git','show','HEAD:cadastros.py'], capture_output=True)
c = r.stdout.decode('utf-8', errors='replace').replace('\r\n','\n')
print(f"Tamanho: {len(c)}")

fixes = 0

# FIX 1: Novo PDV — setor text_input -> selectbox
antigo1 = ('            setor            = st.text_input("Setor",\n'
           '                                             placeholder="Ex: Setor Centro, Setor Leste, Setor Baixada 1",\n'
           '                                             help="Setor geografico — facilita planejamento de roteiro e alocacao de promotores")')

novo1 = ('            # Setor geografico\n'
         '            from database import query as _q\n'
         '            from permissoes import empresa_id_atual as _eid\n'
         '            _setores_novo = _q("SELECT setor_id, codigo, nome FROM setor WHERE empresa_id=%s AND ativo=TRUE ORDER BY codigo", (_eid(),)) or []\n'
         '            _set_opts_novo = [(None,"— Sem setor —")] + [(s[0], f"{s[1]} — {s[2]}") for s in _setores_novo]\n'
         '            _set_sel_novo = st.selectbox("Setor geográfico",\n'
         '                                         _set_opts_novo,\n'
         '                                         format_func=lambda x: x[1],\n'
         '                                         key="pdv_setor_novo",\n'
         '                                         help="Setor geográfico para planejamento de roteiro")\n'
         '            setor_id_novo = _set_sel_novo[0] if _set_sel_novo else None\n'
         '            setor         = _set_sel_novo[1].split(" — ",1)[-1] if _set_sel_novo and _set_sel_novo[0] else ""\n'
         '            aceita_prom_novo = st.checkbox("Comporta promotor",\n'
         '                                           value=True,\n'
         '                                           key="pdv_aceita_prom_novo",\n'
         '                                           help="Desmarque para PDVs que nao recebem promotor (bares, hamburguerias, etc.)")')

if antigo1 in c:
    c = c.replace(antigo1, novo1)
    print("OK: Novo PDV setor selectbox"); fixes+=1
else:
    print("AVISO: padrao novo PDV setor nao encontrado")

# FIX 2: Editar PDV — setor text_input -> selectbox
antigo2 = ('            setor_at = p["setor"] if "setor" in p.keys() and p["setor"] else ""\n'
           '            setor       = st.text_input("Setor", value=setor_at,\n'
           '                                        placeholder="Ex: Setor Centro, Setor Leste",\n'
           f'                                        key=f"pdv_setor_{{pdv_id}}",\n'
           '                                        help="Setor geografico para planejamento de roteiro")')

novo2 = ('            from database import query as _q\n'
         '            from permissoes import empresa_id_atual as _eid\n'
         '            _setores_ed = _q("SELECT setor_id, codigo, nome FROM setor WHERE empresa_id=%s AND ativo=TRUE ORDER BY codigo", (_eid(),)) or []\n'
         '            _set_opts_ed = [(None,"— Sem setor —")] + [(s[0], f"{s[1]} — {s[2]}") for s in _setores_ed]\n'
         '            _sid_atual = p["setor_id"] if "setor_id" in p.keys() else None\n'
         '            _set_idx = next((i for i,s in enumerate(_set_opts_ed) if s[0]==_sid_atual), 0)\n'
         f'            _set_sel_ed = st.selectbox("Setor geográfico", _set_opts_ed,\n'
         '                                        index=_set_idx,\n'
         '                                        format_func=lambda x: x[1],\n'
         f'                                        key=f"pdv_setor_ed_{{pdv_id}}")\n'
         '            setor_id_ed = _set_sel_ed[0] if _set_sel_ed else None\n'
         '            setor = _set_sel_ed[1].split(" — ",1)[-1] if _set_sel_ed and _set_sel_ed[0] else ""\n'
         '            _ap_atual = p["aceita_promotor"] if "aceita_promotor" in p.keys() else True\n'
         '            aceita_prom_ed = st.checkbox("Comporta promotor",\n'
         '                                         value=bool(_ap_atual),\n'
         f'                                         key=f"pdv_aceita_prom_{{pdv_id}}")')

if antigo2 in c:
    c = c.replace(antigo2, novo2)
    print("OK: Editar PDV setor selectbox"); fixes+=1
else:
    print("AVISO: padrao editar PDV setor nao encontrado")
    idx = c.find('setor_at = p["setor"]')
    if idx>0: print(f"  {repr(c[idx:idx+150])}")

# FIX 3: Salvar novo PDV — adicionar setor_id e aceita_promotor no INSERT
antigo3 = ('            INSERT INTO pdv\n'
           '            (cliente_id, numero_loja, nome_loja, tipo_pdv, cnpj, ie,\n'
           '             endereco, bairro, cidade, estado, cep, latitude, longitude,\n'
           '             horario_recebimento, setor, cluster, tamanho_pdv, observacao, status, ativo)')

novo3 = ('            INSERT INTO pdv\n'
         '            (cliente_id, numero_loja, nome_loja, tipo_pdv, cnpj, ie,\n'
         '             endereco, bairro, cidade, estado, cep, latitude, longitude,\n'
         '             horario_recebimento, setor, setor_id, aceita_promotor, cluster, tamanho_pdv, observacao, status, ativo)')

if antigo3 in c:
    c = c.replace(antigo3, novo3)
    print("OK: INSERT PDV com setor_id"); fixes+=1
else:
    print("AVISO: INSERT PDV nao encontrado")

print(f"\nTotal: {fixes} fixes")

with open('cadastros.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c); print("Sintaxe OK")
    subprocess.run(["git","add","cadastros.py"])
    r2 = subprocess.run(["git","commit","-m","feat: setor selectbox + aceita_promotor no form PDV"],
        capture_output=True, text=True)
    print("Commit:", r2.stdout.strip() or r2.stderr.strip())
    r3 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r3.stdout.strip() or r3.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
