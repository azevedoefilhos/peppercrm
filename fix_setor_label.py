import ast, subprocess

r = subprocess.run(['git','show','HEAD:roteiros.py'], capture_output=True)
c = r.stdout.decode('utf-8', errors='replace').replace('\r\n','\n')

# Ver query de setores
idx = c.find('setores = query("""SELECT setor_id')
if idx > 0:
    print("Query setores:", repr(c[idx:idx+150]))

# O problema: setores retorna (setor_id, codigo, nome, cidade, ativo)
# O tuple usado e (s[0], s[1]) onde s[1] = codigo (S1, S2...)
# Precisa ser (s[0], s[2]) onde s[2] = nome completo

antigo1 = ("        [(s[0], s[1]) for s in setores],\n"
           "        format_func=lambda x: x[1],\n"
           "        key=\"set_gest_sel\")")

novo1 = ("        [(s[0], f\"{s[1]} — {s[2]}\") for s in setores],\n"
         "        format_func=lambda x: x[1],\n"
         "        key=\"set_gest_sel\")")

cnt = c.count(antigo1)
print(f"Ocorrencias: {cnt}")
if cnt > 0:
    c = c.replace(antigo1, novo1)
    print("OK: setor label com nome completo")

# Corrige tambem o selectbox de destino ao mover
antigo2 = ("                    opts_mv = [(s[0], s[1]) for s in setores if s[0] != sid_gest]\n"
           "                    novo_set = st.selectbox(\"Mover para\", opts_mv,\n"
           "                        format_func=lambda x: x[1], key=f\"mv_dest_{pdv_id}\")")

novo2 = ("                    opts_mv = [(s[0], f\"{s[1]} — {s[2]}\") for s in setores if s[0] != sid_gest]\n"
         "                    novo_set = st.selectbox(\"Mover para\", opts_mv,\n"
         "                        format_func=lambda x: x[1], key=f\"mv_dest_{pdv_id}\")")

if antigo2 in c:
    c = c.replace(antigo2, novo2)
    print("OK: destino mover com nome completo")
else:
    print("AVISO: destino mover nao encontrado")

with open('roteiros.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c); print("Sintaxe OK")
    subprocess.run(["git","add","roteiros.py"])
    r2 = subprocess.run(["git","commit","-m","fix: setor selectbox mostra nome completo"],
        capture_output=True, text=True)
    print("Commit:", r2.stdout.strip() or r2.stderr.strip())
    r3 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r3.stdout.strip() or r3.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
