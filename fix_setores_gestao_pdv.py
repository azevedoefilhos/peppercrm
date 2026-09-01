import ast, subprocess

r = subprocess.run(['git','show','HEAD:roteiros.py'], capture_output=True)
c = r.stdout.decode('utf-8', errors='replace').replace('\r\n','\n')

# Adiciona gestao de PDVs por setor APOS o resumo de PDVs e ANTES do novo setor
antigo = ('    st.divider()\n'
          '    # Novo setor\n'
          '    with st.expander("➕ Novo setor"):')

novo = ('    st.divider()\n'
        '    # ── Gestao de PDVs por setor ────────────────────────────────────────\n'
        '    st.markdown("#### 🔧 Atribuir / mover PDVs entre setores")\n'
        '    st.caption("Selecione um setor para ver seus PDVs e fazer alterações.")\n'
        '\n'
        '    setor_gest = st.selectbox("Setor para gerenciar",\n'
        '        [(s[0], s[1]) for s in setores],\n'
        '        format_func=lambda x: x[1],\n'
        '        key="set_gest_sel")\n'
        '\n'
        '    if setor_gest:\n'
        '        sid_gest = setor_gest[0]\n'
        '\n'
        '        # PDVs do setor\n'
        '        pdvs_setor = query("""SELECT p.pdv_id,\n'
        '                COALESCE(p.nome_loja,\'Matriz\') as loja,\n'
        '                c.nome_fantasia, p.cidade,\n'
        '                p.aceita_promotor\n'
        '            FROM pdv p JOIN cliente c ON p.cliente_id=c.cliente_id\n'
        '            WHERE p.setor_id=%s\n'
        '            ORDER BY c.nome_fantasia, p.nome_loja""", (sid_gest,)) or []\n'
        '\n'
        '        st.caption(f"{len(pdvs_setor)} PDV(s) neste setor")\n'
        '\n'
        '        if pdvs_setor:\n'
        '            for pdv in pdvs_setor:\n'
        '                pdv_id, loja, cliente, cidade, aceita = pdv\n'
        '                col1, col2, col3, col4 = st.columns([3, 2, 1.5, 1])\n'
        '                col1.write(f"**{loja}** — {cliente}")\n'
        '                col2.write(cidade or "—")\n'
        '                col3.write("✅ Promotor" if aceita else "❌ Sem promotor")\n'
        '                # Mover para outro setor\n'
        '                if col4.button("✏️", key=f"mv_pdv_{pdv_id}",\n'
        '                               help="Mover para outro setor"):\n'
        '                    st.session_state[f"mv_pdv_{pdv_id}"] = True\n'
        '\n'
        '                if st.session_state.get(f"mv_pdv_{pdv_id}"):\n'
        '                    with st.form(f"form_mv_{pdv_id}"):\n'
        '                        novo_set = st.selectbox("Mover para setor",\n'
        '                            [(s[0], s[1]) for s in setores if s[0] != sid_gest],\n'
        '                            format_func=lambda x: x[1],\n'
        '                            key=f"mv_dest_{pdv_id}")\n'
        '                        col_ok, col_no = st.columns(2)\n'
        '                        if col_ok.form_submit_button("✅ Mover", type="primary"):\n'
        '                            execute_write(\n'
        '                                "UPDATE pdv SET setor_id=%s, setor=%s WHERE pdv_id=%s",\n'
        '                                (novo_set[0], novo_set[1].split(" — ",1)[-1], pdv_id))\n'
        '                            st.session_state.pop(f"mv_pdv_{pdv_id}", None)\n'
        '                            st.success(f"PDV movido para {novo_set[1]}!")\n'
        '                            st.rerun()\n'
        '                        if col_no.form_submit_button("Cancelar"):\n'
        '                            st.session_state.pop(f"mv_pdv_{pdv_id}", None)\n'
        '                            st.rerun()\n'
        '\n'
        '        st.divider()\n'
        '\n'
        '        # PDVs sem setor — adicionar ao setor selecionado\n'
        '        with st.expander("➕ Adicionar PDV sem setor a este setor"):\n'
        '            pdvs_sem_setor = query("""SELECT p.pdv_id,\n'
        '                    COALESCE(p.nome_loja,\'Matriz\'), c.nome_fantasia, p.cidade\n'
        '                FROM pdv p JOIN cliente c ON p.cliente_id=c.cliente_id\n'
        '                WHERE p.setor_id IS NULL AND c.empresa_id=%s\n'
        '                ORDER BY c.nome_fantasia, p.nome_loja""", (eid,)) or []\n'
        '\n'
        '            if not pdvs_sem_setor:\n'
        '                st.caption("Todos os PDVs já têm setor atribuído. ✅")\n'
        '            else:\n'
        '                st.caption(f"{len(pdvs_sem_setor)} PDV(s) sem setor")\n'
        '                with st.form("form_add_pdv_setor"):\n'
        '                    pdv_add = st.selectbox("PDV para adicionar",\n'
        '                        pdvs_sem_setor,\n'
        '                        format_func=lambda x: f"{x[1]} — {x[2]} ({x[3] or \'—\'})",\n'
        '                        key="set_add_pdv")\n'
        '                    if st.form_submit_button("➕ Adicionar ao setor", type="primary"):\n'
        '                        nome_setor = setor_gest[1].split(" — ",1)[-1] if " — " in setor_gest[1] else setor_gest[1]\n'
        '                        execute_write(\n'
        '                            "UPDATE pdv SET setor_id=%s, setor=%s WHERE pdv_id=%s",\n'
        '                            (sid_gest, nome_setor, pdv_add[0]))\n'
        '                        st.success(f"{pdv_add[1]} adicionado ao setor!")\n'
        '                        st.rerun()\n'
        '\n'
        '    st.divider()\n'
        '    # Novo setor\n'
        '    with st.expander("➕ Novo setor"):')

if antigo in c:
    c = c.replace(antigo, novo)
    print("OK: gestao PDVs por setor adicionada")
else:
    print("AVISO: padrao nao encontrado")
    idx = c.find('# Novo setor')
    if idx > 0:
        linha = c[:idx].count('\n') + 1
        print(f"  'Novo setor' na linha {linha}")
        print(f"  Contexto: {repr(c[idx-50:idx+30])}")

with open('roteiros.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c); print("Sintaxe OK")
    subprocess.run(["git","add","roteiros.py"])
    r2 = subprocess.run(["git","commit","-m",
        "feat: gestao PDVs por setor na aba Setores do modulo Roteiros"],
        capture_output=True, text=True)
    print("Commit:", r2.stdout.strip() or r2.stderr.strip())
    r3 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r3.stdout.strip() or r3.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
    lines = c.split('\n')
    for i in range(max(0,e.lineno-3), min(len(lines),e.lineno+2)):
        print(f"  {i+1}: {lines[i]}")
