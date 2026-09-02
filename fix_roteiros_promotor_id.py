import ast, subprocess

r = subprocess.run(['git','show','HEAD:roteiros.py'], capture_output=True)
c = r.stdout.decode('utf-8', errors='replace').replace('\r\n','\n')

fixes = 0

# ═══ FIX 1: Query promotores no Rot.Promotor — LEFT JOIN usuario ═══
antigo1 = ('        proms = query("""SELECT u.usuario_id, u.nome, u.tipo FROM usuario u\n'
           '            WHERE u.empresa_id=%s\n'
           "            AND u.tipo IN ('PROMOTOR','PROMOTOR_VENDEDOR')\n"
           '            AND u.ativo=1 ORDER BY u.nome""", (eid,)) or []')

novo1 = ('        # Busca promotores com E sem login\n'
         '        proms = query("""SELECT\n'
         '                COALESCE(u.usuario_id, 0) as uid,\n'
         '                COALESCE(u.nome, pr.nome) as nome,\n'
         "                COALESCE(u.tipo, 'PROMOTOR') as tipo,\n"
         '                pr.promotor_id\n'
         '            FROM promotor pr\n'
         '            LEFT JOIN usuario u ON pr.usuario_id=u.usuario_id\n'
         '            WHERE pr.empresa_id=%s AND pr.ativo!=0\n'
         '            AND pr.nome != \'Sem promotor\'\n'
         '            ORDER BY nome""", (eid,)) or []')

if antigo1 in c:
    c = c.replace(antigo1, novo1)
    print("OK: lista promotores ADM com LEFT JOIN"); fixes+=1
else:
    print("AVISO: lista promotores ADM nao encontrada")

# ═══ FIX 2: Query promotores supervisor — LEFT JOIN ═══
antigo2 = ('        proms = query("""SELECT u.usuario_id, u.nome, u.tipo\n'
           '            FROM supervisor_promotor sp\n'
           '            JOIN promotor pr ON sp.promotor_id=pr.promotor_id\n'
           '            JOIN usuario u ON pr.usuario_id=u.usuario_id\n'
           '            WHERE sp.supervisor_id=%s AND sp.ativo=1 AND u.ativo=1\n'
           '            ORDER BY u.nome""", (sup_id,)) or [] if sup_id else []')

novo2 = ('        proms = query("""SELECT\n'
         '                COALESCE(u.usuario_id, 0) as uid,\n'
         '                COALESCE(u.nome, pr.nome) as nome,\n'
         "                COALESCE(u.tipo, 'PROMOTOR') as tipo,\n"
         '                pr.promotor_id\n'
         '            FROM supervisor_promotor sp\n'
         '            JOIN promotor pr ON sp.promotor_id=pr.promotor_id\n'
         '            LEFT JOIN usuario u ON pr.usuario_id=u.usuario_id\n'
         '            WHERE sp.supervisor_id=%s AND sp.ativo=1\n'
         '            ORDER BY nome""", (sup_id,)) or [] if sup_id else []')

if antigo2 in c:
    c = c.replace(antigo2, novo2)
    print("OK: promotores supervisor LEFT JOIN"); fixes+=1
else:
    print("AVISO: promotores supervisor nao encontrado")

# ═══ FIX 3: prom_uid — agora vem da query como 4 campos ═══
# Antes: prom_sel[0] era usuario_id
# Agora: prom_sel[0]=uid, prom_sel[1]=nome, prom_sel[2]=tipo, prom_sel[3]=promotor_id
antigo3 = ('    prom_uid = prom_sel[0]\n'
           '\n'
           '    # Ponto de base do promotor')

novo3 = ('    prom_uid      = prom_sel[0]  # usuario_id (0 se sem login)\n'
         '    prom_promotor_id = prom_sel[3] if len(prom_sel) > 3 else None\n'
         '    prom_tem_login = prom_uid > 0\n'
         '\n'
         '    # Ponto de base do promotor')

if antigo3 in c:
    c = c.replace(antigo3, novo3)
    print("OK: prom_uid com promotor_id"); fixes+=1
else:
    print("AVISO: prom_uid nao encontrado")

# ═══ FIX 4: Busca roteiro do promotor — usa promotor_id OU usuario_id ═══
antigo4 = ('        WHERE ri.usuario_id=%s AND ri.tipo_roteiro=\'promotor\' AND ri.ativo=TRUE\n'
           '        ORDER BY ri.dia_semana, ri.turno, ri.ordem_rota""", (prom_uid,)) or []')

novo4 = ('        WHERE ri.tipo_roteiro=\'promotor\' AND ri.ativo=TRUE\n'
         '          AND (ri.usuario_id=%s OR ri.promotor_id=%s)\n'
         '        ORDER BY ri.dia_semana, ri.turno, ri.ordem_rota""",\n'
         '        (prom_uid if prom_tem_login else -1,\n'
         '         prom_promotor_id if not prom_tem_login else -1)) or []')

if antigo4 in c:
    c = c.replace(antigo4, novo4)
    print("OK: busca roteiro promotor usa promotor_id OU usuario_id"); fixes+=1
else:
    print("AVISO: busca roteiro nao encontrada")

# ═══ FIX 5: INSERT no roteiro do promotor — usa promotor_id quando sem login ═══
antigo5 = ('                    execute_write("""INSERT INTO roteiro_item\n'
           '                        (tipo_roteiro, usuario_id, pdv_id, dia_semana, turno,\n'
           '                         ordem_rota, frequencia, ativo, empresa_id, criado_por)\n'
           '                        VALUES (\'promotor\',%s,%s,%s,%s,%s,%s,TRUE,%s,%s)\n'
           '                        ON CONFLICT (tipo_roteiro,usuario_id,pdv_id,dia_semana,turno)\n'
           '                        DO UPDATE SET ativo=TRUE, frequencia=EXCLUDED.frequencia""",\n'
           '                        (prom_uid, pdv_p[0], dia_p[0], turno_p,\n'
           '                         nova_ord, freq_p, eid, uid))')

novo5 = ('                    if prom_tem_login:\n'
         '                        execute_write("""INSERT INTO roteiro_item\n'
         '                            (tipo_roteiro, usuario_id, pdv_id, dia_semana, turno,\n'
         '                             ordem_rota, frequencia, ativo, empresa_id, criado_por)\n'
         '                            VALUES (\'promotor\',%s,%s,%s,%s,%s,%s,TRUE,%s,%s)\n'
         '                            ON CONFLICT (tipo_roteiro,usuario_id,pdv_id,dia_semana,turno)\n'
         '                            DO UPDATE SET ativo=TRUE, frequencia=EXCLUDED.frequencia""",\n'
         '                            (prom_uid, pdv_p[0], dia_p[0], turno_p,\n'
         '                             nova_ord, freq_p, eid, uid))\n'
         '                    else:\n'
         '                        execute_write("""INSERT INTO roteiro_item\n'
         '                            (tipo_roteiro, promotor_id, pdv_id, dia_semana, turno,\n'
         '                             ordem_rota, frequencia, ativo, empresa_id, criado_por)\n'
         '                            VALUES (\'promotor\',%s,%s,%s,%s,%s,%s,TRUE,%s,%s)\n'
         '                            ON CONFLICT (tipo_roteiro,promotor_id,pdv_id,dia_semana,turno)\n'
         '                            DO UPDATE SET ativo=TRUE, frequencia=EXCLUDED.frequencia""",\n'
         '                            (prom_promotor_id, pdv_p[0], dia_p[0], turno_p,\n'
         '                             nova_ord, freq_p, eid, uid))')

if antigo5 in c:
    c = c.replace(antigo5, novo5)
    print("OK: INSERT roteiro promotor com promotor_id"); fixes+=1
else:
    print("AVISO: INSERT promotor nao encontrado")

# ═══ FIX 6: format_func do selectbox de promotores ═══
# Agora tem 4 campos — adiciona indicador de sem login
antigo6 = ('                               format_func=lambda x: f"{x[1]} ({x[2]})",\n'
           '                               key="rp2_sel")')

novo6 = ('                               format_func=lambda x: f"{x[1]} ({x[2]})" +\n'
         '                                   (" 🔑" if x[0] > 0 else " 📋"),\n'
         '                               key="rp2_sel")')

if antigo6 in c:
    c = c.replace(antigo6, novo6)
    print("OK: selectbox promotor com indicador login"); fixes+=1
else:
    print("AVISO: selectbox promotor nao encontrado")

print(f"\nTotal: {fixes} fixes")

with open('roteiros.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c); print("Sintaxe OK")
    subprocess.run(["git","add","roteiros.py","etapa2_roteiro_promotor_id.py"])
    r2 = subprocess.run(["git","commit","-m",
        "feat: roteiro promotor suporta promotor_id para promotores sem login"],
        capture_output=True, text=True)
    print("Commit:", r2.stdout.strip() or r2.stderr.strip())
    r3 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r3.stdout.strip() or r3.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
    lines = c.split('\n')
    for i in range(max(0,e.lineno-3), min(len(lines),e.lineno+2)):
        print(f"  {i+1}: {lines[i]}")
