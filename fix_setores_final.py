import ast, subprocess

r = subprocess.run(['git','show','HEAD:roteiros.py'], capture_output=True)
c = r.stdout.decode('utf-8', errors='replace').replace('\r\n','\n')

antigo = ('    resumo = query("""SELECT s.nome, COUNT(p.pdv_id) as total,\n'
          '            SUM(CASE WHEN p.aceita_promotor THEN 1 ELSE 0 END) as c_prom\n'
          '        FROM setor s\n'
          '        LEFT JOIN pdv p ON p.setor_id=s.setor_id AND p.ativo!=0\n'
          '        LEFT JOIN cliente cli ON p.cliente_id=cli.cliente_id\n'
          '        WHERE s.empresa_id=%s GROUP BY s.setor_id, s.nome\n'
          '        ORDER BY s.codigo""", (eid,)) or []')

novo = ('    resumo = query("""SELECT s.nome, COUNT(p.pdv_id) as total,\n'
        '            SUM(CASE WHEN p.aceita_promotor THEN 1 ELSE 0 END) as c_prom\n'
        '        FROM setor s\n'
        '        LEFT JOIN pdv p ON p.setor_id=s.setor_id AND p.ativo!=0\n'
        '        WHERE s.empresa_id=%s GROUP BY s.setor_id, s.nome\n'
        '        ORDER BY s.codigo""", (eid,)) or []')

if antigo in c:
    c = c.replace(antigo, novo)
    print("OK: LEFT JOIN cliente removido da query setores")
else:
    print("AVISO: padrao nao encontrado")

# Fix PDVs nao habilitam - o problema e que cli_sel retorna tupla de 3 elementos
# mas o codigo usa cli_sel[0] - verificar
idx_pdvs = c.find('pdvs_disp = query("""SELECT p.pdv_id, p.nome_loja')
if idx_pdvs > 0:
    print(f"PDVs query: {repr(c[idx_pdvs-30:idx_pdvs+50])}")

with open('roteiros.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c); print("Sintaxe OK")
    subprocess.run(["git","add","roteiros.py"])
    r2 = subprocess.run(["git","commit","-m","fix: remove LEFT JOIN cliente da query setores"],
        capture_output=True, text=True)
    print("Commit:", r2.stdout.strip() or r2.stderr.strip())
    r3 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r3.stdout.strip() or r3.stderr.strip())
except SyntaxError as e:
    print(f"ERRO: {e}")
