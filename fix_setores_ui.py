import ast, subprocess

r = subprocess.run(['git','show','HEAD:roteiros.py'], capture_output=True)
c = r.stdout.decode('utf-8', errors='replace').replace('\r\n','\n')

# FIX 1: session_state conflito com widget key
# Solucao: usar key diferente para o botao vs session_state
antigo1 = ('            if c4.button("✏️", key=f"mv_pdv_{pdv_id}", help="Mover de setor"):\n'
           '                st.session_state[f"mv_pdv_{pdv_id}"] = True\n'
           '\n'
           '            if st.session_state.get(f"mv_pdv_{pdv_id}"):')

novo1 = ('            if c4.button("✏️", key=f"btn_mv_{pdv_id}", help="Mover de setor",\n'
         '                        on_click=lambda pid=pdv_id: st.session_state.update({f"mv_pdv_{pid}": True})):\n'
         '                pass\n'
         '\n'
         '            if st.session_state.get(f"mv_pdv_{pdv_id}"):')

if antigo1 in c:
    c = c.replace(antigo1, novo1)
    print("OK: session_state conflito corrigido")
else:
    print("AVISO: padrao session_state nao encontrado")

# FIX 2: Informacao de promotor — remover X vermelho, mostrar apenas icone quando tem
antigo2 = ('            c1.write(f"**{loja}** — {cliente}")\n'
           '            c2.write(cidade or "—")\n'
           '            c3.write("✅ Promotor" if aceita else "❌ Sem promotor")')

novo2 = ('            # Verifica se tem promotor ativo atribuido\n'
         '            n_prom_pdv = query(\n'
         '                "SELECT COUNT(*) FROM att_promotor WHERE pdv_id=%s AND ativo!=0",\n'
         '                (pdv_id,)) or [[0]]\n'
         '            tem_prom_pdv = (n_prom_pdv[0][0] or 0) > 0\n'
         '            c1.write(f"**{loja}** — {cliente}")\n'
         '            c2.caption(cidade or "—")\n'
         '            if tem_prom_pdv:\n'
         '                c3.caption("🟢 com promotor")')

if antigo2 in c:
    c = c.replace(antigo2, novo2)
    print("OK: informacao promotor simplificada")
else:
    print("AVISO: padrao promotor nao encontrado")

with open('roteiros.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c); print("Sintaxe OK")
    subprocess.run(["git","add","roteiros.py"])
    r2 = subprocess.run(["git","commit","-m",
        "fix: session_state key conflito + UI promotor simplificada"],
        capture_output=True, text=True)
    print("Commit:", r2.stdout.strip() or r2.stderr.strip())
    r3 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r3.stdout.strip() or r3.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
