import ast, subprocess

r = subprocess.run(['git','show','HEAD:roteiros.py'], capture_output=True)
c = r.stdout.decode('utf-8', errors='replace').replace('\r\n','\n')

# Insere gestao de PDVs ENTRE o resumo e o novo setor
antigo = ('    st.divider()\n'
          '\n'
          '    # Novo setor\n'
          '    with st.expander("➕ Novo setor"):')

novo = ('    st.divider()\n'
        '\n'
        '    # ── Gestao de PDVs por setor ────────────────────────────────────\n'
        '    st.markdown("#### 🔧 Atribuir / mover PDVs entre setores")\n'
        '    st.caption("Selecione um setor para ver seus PDVs e mover entre setores.")\n'
        '\n'
        '    col_sg, _ = st.columns([2,2])\n'
        '    setor_gest = col_sg.selectbox("Setor para gerenciar",\n'
        '        [(s[0], s[1]) for s in setores],\n'
        '        format_func=lambda x: x[1],\n'
        '        key="set_gest_sel")\n'
        '\n'
        '    if setor_gest:\n'
        '        sid_gest = setor_gest[0]\n'
        '        pdvs_setor_gest = query("""SELECT p.pdv_id,\n'
        '                COALESCE(p.nome_loja,\'Matriz\') as loja,\n'
        '                c.nome_fantasia, p.cidade, p.aceita_promotor\n'
        '            FROM pdv p JOIN cliente c ON p.cliente_id=c.cliente_id\n'
        '            WHERE p.setor_id=%s ORDER BY c.nome_fantasia, p.nome_loja""",\n'
        '            (sid_gest,)) or []\n'
        '\n'
        '        st.caption(f"{len(pdvs_setor_gest)} PDV(s) neste setor")\n'
        '\n'
        '        for pdv in pdvs_setor_gest:\n'
        '            pdv_id, loja, cliente, cidade, aceita = pdv\n'
        '            c1, c2, c3, c4 = st.columns([3, 2, 1.5, 0.8])\n'
        '            c1.write(f"**{loja}** — {cliente}")\n'
        '            c2.write(cidade or "—")\n'
        '            c3.write("✅ Promotor" if aceita else "❌ Sem promotor")\n'
        '            if c4.button("✏️", key=f"mv_pdv_{pdv_id}", help="Mover de setor"):\n'
        '                st.session_state[f"mv_pdv_{pdv_id}"] = True\n'
        '\n'
        '            if st.session_state.get(f"mv_pdv_{pdv_id}"):\n'
        '                with st.form(f"form_mv_{pdv_id}"):\n'
        '                    opts_mv = [(s[0], s[1]) for s in setores if s[0] != sid_gest]\n'
        '                    novo_set = st.selectbox("Mover para", opts_mv,\n'
        '                        format_func=lambda x: x[1], key=f"mv_dest_{pdv_id}")\n'
        '                    ca, cb = st.columns(2)\n'
        '                    if ca.form_submit_button("✅ Mover", type="primary"):\n'
        '                        nome_s = novo_set[1].split(" — ",1)[-1] if " — " in novo_set[1] else novo_set[1]\n'
        '                        execute_write(\n'
        '                            "UPDATE pdv SET setor_id=%s, setor=%s WHERE pdv_id=%s",\n'
        '                            (novo_set[0], nome_s, pdv_id))\n'
        '                        st.session_state.pop(f"mv_pdv_{pdv_id}", None)\n'
        '                        st.success("PDV movido!"); st.rerun()\n'
        '                    if cb.form_submit_button("Cancelar"):\n'
        '                        st.session_state.pop(f"mv_pdv_{pdv_id}", None); st.rerun()\n'
        '\n'
        '        st.divider()\n'
        '        with st.expander("➕ Adicionar PDV sem setor a este setor"):\n'
        '            pdvs_ss = query("""SELECT p.pdv_id,\n'
        '                    COALESCE(p.nome_loja,\'Matriz\'), c.nome_fantasia, p.cidade\n'
        '                FROM pdv p JOIN cliente c ON p.cliente_id=c.cliente_id\n'
        '                WHERE p.setor_id IS NULL AND c.empresa_id=%s\n'
        '                ORDER BY c.nome_fantasia, p.nome_loja""", (eid,)) or []\n'
        '            if not pdvs_ss:\n'
        '                st.caption("Todos os PDVs já têm setor. ✅")\n'
        '            else:\n'
        '                with st.form("form_add_pdv_s"):\n'
        '                    pdv_add = st.selectbox("PDV", pdvs_ss,\n'
        '                        format_func=lambda x: f"{x[1]} — {x[2]}",\n'
        '                        key="set_add_pdv2")\n'
        '                    if st.form_submit_button("➕ Adicionar", type="primary"):\n'
        '                        nome_s2 = setor_gest[1].split(" — ",1)[-1] if " — " in setor_gest[1] else setor_gest[1]\n'
        '                        execute_write(\n'
        '                            "UPDATE pdv SET setor_id=%s, setor=%s WHERE pdv_id=%s",\n'
        '                            (sid_gest, nome_s2, pdv_add[0]))\n'
        '                        st.success("PDV adicionado!"); st.rerun()\n'
        '\n'
        '    st.divider()\n'
        '\n'
        '    # Novo setor\n'
        '    with st.expander("➕ Novo setor"):')

if antigo in c:
    c = c.replace(antigo, novo)
    print("OK: gestao PDVs por setor adicionada")
else:
    print("AVISO: padrao nao encontrado")
    idx = c.find('st.divider()\n\n    # Novo setor')
    print(f"Contexto: {repr(c[idx-20:idx+50])}")

with open('roteiros.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c); print("Sintaxe OK")
    subprocess.run(["git","add","roteiros.py"])
    r2 = subprocess.run(["git","commit","-m","feat: gestao PDVs por setor na aba Setores"],
        capture_output=True, text=True)
    print("Commit:", r2.stdout.strip() or r2.stderr.strip())
    r3 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r3.stdout.strip() or r3.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
