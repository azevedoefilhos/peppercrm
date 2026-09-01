import ast, subprocess

r = subprocess.run(['git','show','HEAD:equipe.py'], capture_output=True)
c = r.stdout.decode('utf-8', errors='replace').replace('\r\n','\n')

# Adiciona secao de equipe de promotores ANTES do divisor e novo supervisor
antigo = ('    st.divider()\n'
          '    st.subheader("➕ Novo supervisor")')

novo = ('    st.divider()\n'
        '    # ── Equipe de promotores do supervisor ──────────────────────────────\n'
        '    st.subheader("👥 Equipe de promotores por supervisor")\n'
        '    st.caption("Vincule promotores à equipe de cada supervisor para controle de roteiros e cobertura.")\n'
        '\n'
        '    for sup in (sups or []):\n'
        '        sid, s_nome = sup[0], sup[1]\n'
        '        with st.expander(f"👤 {s_nome}"):\n'
        '            # Promotores ja vinculados\n'
        '            vinculados = query("""SELECT sp.supervisor_promotor_id,\n'
        '                    pr.promotor_id, pr.nome, u.tipo,\n'
        '                    sp.ativo\n'
        '                FROM supervisor_promotor sp\n'
        '                JOIN promotor pr ON sp.promotor_id=pr.promotor_id\n'
        '                LEFT JOIN usuario u ON pr.usuario_id=u.usuario_id\n'
        '                WHERE sp.supervisor_id=%s\n'
        '                ORDER BY pr.nome""", (sid,)) or []\n'
        '\n'
        '            if vinculados:\n'
        '                for v in vinculados:\n'
        '                    sp_id, pr_id, pr_nome, pr_tipo, ativo = v\n'
        '                    col_n, col_t, col_a, col_r = st.columns([3,1.5,1,0.8])\n'
        '                    col_n.write(pr_nome)\n'
        '                    col_t.write(pr_tipo or "PROMOTOR")\n'
        '                    col_a.write("✅ Ativo" if ativo else "❌ Inativo")\n'
        '                    if col_r.button("🗑️", key=f"rem_sp_{sp_id}",\n'
        '                                   help="Remover da equipe"):\n'
        '                        execute_write(\n'
        '                            "UPDATE supervisor_promotor SET ativo=0 WHERE supervisor_promotor_id=%s",\n'
        '                            (sp_id,))\n'
        '                        st.rerun()\n'
        '            else:\n'
        '                st.caption("Nenhum promotor vinculado ainda.")\n'
        '\n'
        '            # Adicionar promotor\n'
        '            proms_disp = query("""SELECT pr.promotor_id, pr.nome, u.tipo\n'
        '                FROM promotor pr\n'
        '                LEFT JOIN usuario u ON pr.usuario_id=u.usuario_id\n'
        '                WHERE pr.empresa_id=%s AND pr.ativo!=0\n'
        '                AND pr.promotor_id NOT IN (\n'
        '                    SELECT promotor_id FROM supervisor_promotor\n'
        '                    WHERE supervisor_id=%s AND ativo=1)\n'
        '                ORDER BY pr.nome""", (eid, sid)) or []\n'
        '\n'
        '            if proms_disp:\n'
        '                with st.form(f"add_prom_sup_{sid}"):\n'
        '                    p_sel = st.selectbox("Adicionar promotor",\n'
        '                        proms_disp,\n'
        '                        format_func=lambda x: f"{x[1]} ({x[2] or \'PROMOTOR\'})",\n'
        '                        key=f"ps_add_{sid}")\n'
        '                    if st.form_submit_button("➕ Adicionar à equipe", type="primary"):\n'
        '                        # Verifica se ja existe registro inativo\n'
        '                        existe = query(\n'
        '                            "SELECT supervisor_promotor_id FROM supervisor_promotor WHERE supervisor_id=%s AND promotor_id=%s",\n'
        '                            (sid, p_sel[0])) or []\n'
        '                        if existe:\n'
        '                            execute_write(\n'
        '                                "UPDATE supervisor_promotor SET ativo=1 WHERE supervisor_promotor_id=%s",\n'
        '                                (existe[0][0],))\n'
        '                        else:\n'
        '                            execute_write(\n'
        '                                "INSERT INTO supervisor_promotor (supervisor_id, promotor_id, ativo) VALUES (%s,%s,1)",\n'
        '                                (sid, p_sel[0]))\n'
        '                        st.success(f"{p_sel[1]} adicionado à equipe de {s_nome}!")\n'
        '                        st.rerun()\n'
        '\n'
        '    st.divider()\n'
        '    st.subheader("➕ Novo supervisor")')

if antigo in c:
    c = c.replace(antigo, novo)
    print("OK: secao equipe promotores adicionada")
else:
    print("AVISO: padrao nao encontrado")
    idx = c.find('st.subheader("➕ Novo supervisor")')
    print(f"  Linha: {c[:idx].count(chr(10))+1}")

with open('equipe.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c); print("Sintaxe OK")
    subprocess.run(["git","add","equipe.py"])
    r2 = subprocess.run(["git","commit","-m",
        "feat: equipe supervisores com vinculacao de promotores"],
        capture_output=True, text=True)
    print("Commit:", r2.stdout.strip() or r2.stderr.strip())
    r3 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r3.stdout.strip() or r3.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
