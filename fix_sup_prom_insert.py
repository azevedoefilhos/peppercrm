import ast, subprocess

r = subprocess.run(['git','show','HEAD:equipe.py'], capture_output=True)
c = r.stdout.decode('utf-8', errors='replace').replace('\r\n','\n')

# FIX 1: Query vinculados - usa 'id' nao 'supervisor_promotor_id'
antigo1 = ('            vinculados = query("""SELECT sp.supervisor_promotor_id,\n'
           '                    pr.promotor_id, pr.nome, u.tipo,\n'
           '                    sp.ativo\n'
           '                FROM supervisor_promotor sp\n'
           '                JOIN promotor pr ON sp.promotor_id=pr.promotor_id\n'
           '                LEFT JOIN usuario u ON pr.usuario_id=u.usuario_id\n'
           '                WHERE sp.supervisor_id=%s\n'
           '                ORDER BY pr.nome""", (sid,)) or []')

novo1 = ('            vinculados = query("""SELECT sp.id,\n'
         '                    pr.promotor_id, pr.nome, u.tipo,\n'
         '                    sp.ativo\n'
         '                FROM supervisor_promotor sp\n'
         '                JOIN promotor pr ON sp.promotor_id=pr.promotor_id\n'
         '                LEFT JOIN usuario u ON pr.usuario_id=u.usuario_id\n'
         '                WHERE sp.supervisor_id=%s\n'
         '                ORDER BY pr.nome""", (sid,)) or []')

if antigo1 in c:
    c = c.replace(antigo1, novo1)
    print("OK: query vinculados usa id")
else:
    print("AVISO: query vinculados nao encontrada")

# FIX 2: Remover usa 'id'
antigo2 = ('                    if col_r.button("🗑️", key=f"rem_sp_{sp_id}",\n'
           '                                   help="Remover da equipe"):\n'
           '                        execute_write(\n'
           '                            "UPDATE supervisor_promotor SET ativo=0 WHERE supervisor_promotor_id=%s",\n'
           '                            (sp_id,))')

novo2 = ('                    if col_r.button("🗑️", key=f"rem_sp_{sp_id}",\n'
         '                                   help="Remover da equipe"):\n'
         '                        execute_write(\n'
         '                            "UPDATE supervisor_promotor SET ativo=0 WHERE id=%s",\n'
         '                            (sp_id,))')

if antigo2 in c:
    c = c.replace(antigo2, novo2)
    print("OK: remover usa id")
else:
    print("AVISO: remover nao encontrado")

# FIX 3: INSERT com empresa_id
antigo3 = ('                        else:\n'
           '                            execute_write(\n'
           '                                "INSERT INTO supervisor_promotor (supervisor_id, promotor_id, ativo) VALUES (%s,%s,1)",\n'
           '                                (sid, p_sel[0]))')

novo3 = ('                        else:\n'
         '                            execute_write(\n'
         '                                "INSERT INTO supervisor_promotor (supervisor_id, promotor_id, empresa_id, ativo) VALUES (%s,%s,%s,1)",\n'
         '                                (sid, p_sel[0], eid))')

if antigo3 in c:
    c = c.replace(antigo3, novo3)
    print("OK: INSERT com empresa_id")
else:
    print("AVISO: INSERT nao encontrado")

# FIX 4: UPDATE reativacao usa 'id'
antigo4 = ('                        if existe:\n'
           '                            execute_write(\n'
           '                                "UPDATE supervisor_promotor SET ativo=1 WHERE supervisor_promotor_id=%s",\n'
           '                                (existe[0][0],))')

novo4 = ('                        if existe:\n'
         '                            execute_write(\n'
         '                                "UPDATE supervisor_promotor SET ativo=1 WHERE id=%s",\n'
         '                                (existe[0][0],))')

if antigo4 in c:
    c = c.replace(antigo4, novo4)
    print("OK: reativacao usa id")
else:
    print("AVISO: reativacao nao encontrada")

# FIX 5: Query existe usa 'id'
antigo5 = ('                        existe = query(\n'
           '                            "SELECT supervisor_promotor_id FROM supervisor_promotor WHERE supervisor_id=%s AND promotor_id=%s",\n'
           '                            (sid, p_sel[0])) or []')

novo5 = ('                        existe = query(\n'
         '                            "SELECT id FROM supervisor_promotor WHERE supervisor_id=%s AND promotor_id=%s",\n'
         '                            (sid, p_sel[0])) or []')

if antigo5 in c:
    c = c.replace(antigo5, novo5)
    print("OK: query existe usa id")
else:
    print("AVISO: query existe nao encontrada")

with open('equipe.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c); print("Sintaxe OK")
    subprocess.run(["git","add","equipe.py"])
    r2 = subprocess.run(["git","commit","-m",
        "fix: supervisor_promotor usa id e empresa_id corretos"],
        capture_output=True, text=True)
    print("Commit:", r2.stdout.strip() or r2.stderr.strip())
    r3 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r3.stdout.strip() or r3.stderr.strip())
except SyntaxError as e:
    print(f"ERRO: {e}")
