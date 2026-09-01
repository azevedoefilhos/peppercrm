import ast, subprocess

r = subprocess.run(['git','show','HEAD:roteiros.py'], capture_output=True)
c = r.stdout.decode('utf-8', errors='replace').replace('\r\n','\n')

# FIX: Query setores com contagem real de promotores atribuidos
antigo = ('    resumo = query("""SELECT s.nome, COUNT(p.pdv_id) as total,\n'
          '            SUM(CASE WHEN p.aceita_promotor THEN 1 ELSE 0 END) as c_prom\n'
          '        FROM setor s\n'
          '        LEFT JOIN pdv p ON p.setor_id=s.setor_id\n'
          '        WHERE s.empresa_id=%s GROUP BY s.setor_id, s.nome\n'
          '        ORDER BY s.codigo""", (eid,)) or []')

novo = ('    resumo = query("""SELECT s.nome,\n'
        '            COUNT(p.pdv_id) as total,\n'
        '            SUM(CASE WHEN p.aceita_promotor THEN 1 ELSE 0 END) as comporta,\n'
        '            COUNT(DISTINCT ap.att_promotor_id) as tem_promotor\n'
        '        FROM setor s\n'
        '        LEFT JOIN pdv p ON p.setor_id=s.setor_id\n'
        '        LEFT JOIN att_promotor ap ON ap.pdv_id=p.pdv_id AND ap.ativo!=0\n'
        '        WHERE s.empresa_id=%s GROUP BY s.setor_id, s.nome\n'
        '        ORDER BY s.codigo""", (eid,)) or []')

if antigo in c:
    c = c.replace(antigo, novo)
    print("OK: query setores com contagem real promotores")
else:
    print("AVISO: padrao nao encontrado")

# FIX: Texto de exibicao dos setores
antigo2 = ('        st.write(f"**{nome_s}** — {total or 0} PDVs "\n'
           '                 f"({c_prom or 0} com promotor, {sem_prom} sem promotor)")')

novo2 = ('        comporta = r[2] or 0\n'
         '        tem_prom = r[3] or 0\n'
         '        nao_comp = (total or 0) - comporta\n'
         '        st.write(f"**{nome_s}** — {total or 0} PDVs | "\n'
         '                 f"{comporta} comportam promotor ({tem_prom} com promotor ativo) | "\n'
         '                 f"{nao_comp} não comportam")')

if antigo2 in c:
    c = c.replace(antigo2, novo2)
    print("OK: nomenclatura corrigida")
else:
    print("AVISO: padrao texto nao encontrado")
    idx = c.find('com promotor, {sem_prom}')
    if idx>0: print(f"  {repr(c[idx-30:idx+80])}")

# FIX: loop for r in resumo - ajusta variaveis
antigo3 = ('    for r in resumo:\n'
           '        nome_s, total, c_prom = r\n'
           '        sem_prom = (total or 0) - (c_prom or 0)')

novo3 = ('    for r in resumo:\n'
         '        nome_s, total = r[0], r[1]')

if antigo3 in c:
    c = c.replace(antigo3, novo3)
    print("OK: loop resumo ajustado")
else:
    print("AVISO: loop nao encontrado")
    idx = c.find('for r in resumo')
    if idx>0: print(f"  {repr(c[idx:idx+100])}")

with open('roteiros.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c); print("Sintaxe OK")
    subprocess.run(["git","add","roteiros.py"])
    r2 = subprocess.run(["git","commit","-m",
        "feat: setores nomenclatura comporta_promotor + contagem real atribuidos"],
        capture_output=True, text=True)
    print("Commit:", r2.stdout.strip() or r2.stderr.strip())
    r3 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r3.stdout.strip() or r3.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
    lines = c.split('\n')
    for i in range(max(0,e.lineno-3),min(len(lines),e.lineno+2)):
        print(f"  {i+1}: {lines[i]}")
