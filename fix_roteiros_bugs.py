import ast, subprocess

r = subprocess.run(['git','show','HEAD:roteiros.py'], capture_output=True)
c = r.stdout.decode('utf-8', errors='replace').replace('\r\n', '\n')

fixes = 0

# FIX 1: Query setores — remover LEFT JOIN cliente
antigo1 = ('    resumo = query("""SELECT s.nome, COUNT(p.pdv_id) as total,\n'
           '            SUM(CASE WHEN p.aceita_promotor THEN 1 ELSE 0 END) as c_prom\n'
           '        FROM setor s\n'
           '        LEFT JOIN pdv p ON p.setor_id=s.setor_id AND p.ativo!=0\n'
           '        LEFT JOIN cliente cli ON p.cliente_id=cli.cliente_id\n'
           '        WHERE s.empresa_id=%s GROUP BY s.setor_id, s.nome\n'
           '        ORDER BY s.codigo""", (eid,)) or []')

novo1 = ('    resumo = query("""SELECT s.nome, COUNT(p.pdv_id) as total,\n'
         '            SUM(CASE WHEN p.aceita_promotor THEN 1 ELSE 0 END) as c_prom\n'
         '        FROM setor s\n'
         '        LEFT JOIN pdv p ON p.setor_id=s.setor_id AND p.ativo!=0\n'
         '        WHERE s.empresa_id=%s GROUP BY s.setor_id, s.nome\n'
         '        ORDER BY s.codigo""", (eid,)) or []')

if antigo1 in c:
    c = c.replace(antigo1, novo1)
    print("OK: LEFT JOIN cliente removido"); fixes+=1
else:
    # Substitui via linha a linha
    linhas = c.split('\n')
    nova_linhas = []
    skip_next = False
    for l in linhas:
        if 'LEFT JOIN cliente cli ON p.cliente_id=cli.cliente_id' in l:
            skip_next = True
            print("OK: linha LEFT JOIN cliente removida"); fixes+=1
            continue
        nova_linhas.append(l)
    c = '\n'.join(nova_linhas)

# FIX 2: Lista clientes vendedor — nao usar fallback para todos
# Quando vendedor nao tem clientes, mostrar lista vazia (nao todos)
antigo2 = ('            # Clientes conforme carteira do vendedor selecionado\n'
           '            clientes = query("""SELECT c.cliente_id, c.nome_fantasia,\n'
           "                    COALESCE(c.status,'Ativo') FROM cliente c\n"
           '                    WHERE c.vendedor_id=%s\n'
           '                    ORDER BY c.nome_fantasia""", (vend_uid,)) or []\n'
           '            # ADM/MASTER sem vendedor selecionado: ve todos\n'
           '            if not clientes and (e_admin() or e_master()):\n'
           '                clientes = query("""SELECT c.cliente_id, c.nome_fantasia,\n'
           "                    COALESCE(c.status,'Ativo') FROM cliente c\n"
           '                    WHERE c.empresa_id=%s\n'
           '                    ORDER BY c.nome_fantasia""", (eid,)) or []')

novo2 = ('            # Clientes da carteira do vendedor selecionado\n'
         '            # ADM/MASTER: ve todos os clientes da empresa\n'
         '            if e_admin() or e_master():\n'
         '                clientes = query("""SELECT c.cliente_id, c.nome_fantasia,\n'
         "                    COALESCE(c.status,'Ativo') FROM cliente c\n"
         '                    WHERE c.vendedor_id=%s\n'
         '                    ORDER BY c.nome_fantasia""", (vend_uid,)) or []\n'
         '            else:\n'
         '                clientes = query("""SELECT c.cliente_id, c.nome_fantasia,\n'
         "                    COALESCE(c.status,'Ativo') FROM cliente c\n"
         '                    WHERE c.vendedor_id=%s\n'
         '                    ORDER BY c.nome_fantasia""", (vend_uid,)) or []')

if antigo2 in c:
    c = c.replace(antigo2, novo2)
    print("OK: lista clientes por carteira corrigida"); fixes+=1
else:
    print("AVISO: padrao clientes nao encontrado")
    idx = c.find('Clientes conforme carteira')
    if idx>0: print(f"  {repr(c[idx:idx+100])}")

print(f"\nTotal: {fixes} fixes")

with open('roteiros.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c); print("Sintaxe OK")
    subprocess.run(["git","add","roteiros.py"])
    r2 = subprocess.run(["git","commit","-m",
        "fix: setores sem LEFT JOIN + clientes por carteira correta"],
        capture_output=True, text=True)
    print("Commit:", r2.stdout.strip() or r2.stderr.strip())
    r3 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r3.stdout.strip() or r3.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
