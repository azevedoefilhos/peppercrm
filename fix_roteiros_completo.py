import ast, subprocess

# Le roteiros.py do disco local (versao atual)
r = subprocess.run(['git','show','HEAD:roteiros.py'], capture_output=True)
c = r.stdout.decode('utf-8', errors='replace')
print(f"Tamanho: {len(c)}")

# Normaliza quebras de linha para facilitar substituicoes
c = c.replace('\r\n', '\n')
fixes = 0

# ═══ FIX 1: Query setores - LEFT JOIN errado ═══
# O problema e que a condicao AND cli.empresa_id=%s esta no JOIN
# mas precisa estar no WHERE ou sem condicao (setor ja filtra por empresa)
antigo1 = ('    resumo = query("""SELECT s.nome, COUNT(p.pdv_id) as total,\n'
           '            SUM(CASE WHEN p.aceita_promotor THEN 1 ELSE 0 END) as c_prom\n'
           '        FROM setor s\n'
           '        LEFT JOIN pdv p ON p.setor_id=s.setor_id AND p.ativo!=0\n'
           '        LEFT JOIN cliente cli ON p.cliente_id=cli.cliente_id AND cli.empresa_id=%s\n'
           '        WHERE s.empresa_id=%s GROUP BY s.setor_id, s.nome\n'
           '        ORDER BY s.codigo""", (eid, eid)) or []')

novo1 = ('    resumo = query("""SELECT s.nome, COUNT(p.pdv_id) as total,\n'
         '            SUM(CASE WHEN p.aceita_promotor THEN 1 ELSE 0 END) as c_prom\n'
         '        FROM setor s\n'
         '        LEFT JOIN pdv p ON p.setor_id=s.setor_id AND p.ativo!=0\n'
         '        WHERE s.empresa_id=%s GROUP BY s.setor_id, s.nome\n'
         '        ORDER BY s.codigo""", (eid,)) or []')

if antigo1 in c:
    c = c.replace(antigo1, novo1)
    print("OK: query setores simplificada"); fixes+=1
else:
    # Tenta versao sem o LEFT JOIN cli
    antigo1b = ('    resumo = query("""SELECT s.nome, COUNT(p.pdv_id) as total,\n'
                '            SUM(CASE WHEN p.aceita_promotor THEN 1 ELSE 0 END) as c_prom\n'
                '        FROM setor s\n'
                '        LEFT JOIN pdv p ON p.setor_id=s.setor_id AND p.ativo!=0\n'
                '        WHERE s.empresa_id=%s GROUP BY s.setor_id, s.nome\n'
                '        ORDER BY s.codigo""", (eid,)) or []')
    if antigo1b in c:
        print("OK: query setores ja esta correta")
    else:
        print("AVISO: query setores nao encontrada")
        idx = c.find('resumo = query')
        if idx>0: print(f"  {repr(c[idx:idx+300])}")

# ═══ FIX 2: Lista clientes vendedor - mostrar por carteira correta ═══
antigo2 = ('            if e_admin() or e_master():\n'
           '                clientes = query("""SELECT cliente_id, nome_fantasia,\n'
           "                    COALESCE(status,'Ativo') FROM cliente\n"
           '                    WHERE empresa_id=%s ORDER BY nome_fantasia""", (eid,)) or []\n'
           '            else:\n'
           '                clientes = query("""SELECT cliente_id, nome_fantasia,\n'
           "                    COALESCE(status,'Ativo') FROM cliente\n"
           '                    WHERE vendedor_id=%s ORDER BY nome_fantasia""", (vend_uid,)) or []')

novo2 = ('            # Clientes conforme carteira do vendedor selecionado\n'
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

if antigo2 in c:
    c = c.replace(antigo2, novo2)
    print("OK: lista clientes vendedor por carteira"); fixes+=1
else:
    print("AVISO: lista clientes vendedor nao encontrada")
    idx = c.find('clientes = query("""SELECT cliente_id, nome_fantasia')
    if idx>0: print(f"  {repr(c[idx:idx+200])}")

# ═══ FIX 3: Lista clientes promotor ═══
# Busca padrao atual
idx_prom = c.find('clientes_p = query("""SELECT DISTINCT c.cliente_id')
if idx_prom > 0:
    # Encontra o bloco completo (ate o proximo 'else' ou fechamento)
    fim = c.find('\n            cli_p', idx_prom)
    bloco = c[idx_prom-50:fim+1]
    print(f"Bloco promotor encontrado ({len(bloco)} chars)")
    
    # Substitui toda a logica de clientes_p
    inicio_bloco = c.rfind('\n            if ', 0, idx_prom)
    fim_bloco = c.find('\n            cli_p', idx_prom)
    
    velho = c[inicio_bloco:fim_bloco]
    novo3 = ('\n            # Clientes ativos com PDVs\n'
             '            if e_admin() or e_master() or e_supervisor():\n'
             '                clientes_p = query("""SELECT DISTINCT c.cliente_id, c.nome_fantasia\n'
             '                    FROM cliente c JOIN pdv p ON p.cliente_id=c.cliente_id\n'
             "                    WHERE p.ativo!=0 AND c.empresa_id=%s AND c.status='Ativo'\n"
             '                    ORDER BY c.nome_fantasia""", (eid,)) or []\n'
             '            else:\n'
             '                clientes_p = query("""SELECT DISTINCT c.cliente_id, c.nome_fantasia\n'
             '                    FROM cliente c JOIN pdv p ON p.cliente_id=c.cliente_id\n'
             "                    WHERE p.ativo!=0 AND c.vendedor_id=%s AND c.status='Ativo'\n"
             '                    ORDER BY c.nome_fantasia""", (uid,)) or []')
    
    c = c[:inicio_bloco] + novo3 + c[fim_bloco:]
    print("OK: lista clientes promotor substituida"); fixes+=1
else:
    print("AVISO: clientes_p nao encontrado")

print(f"\nTotal: {fixes} fixes")

with open('roteiros.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c); print("Sintaxe OK")
    subprocess.run(["git","add","roteiros.py"])
    r2 = subprocess.run(["git","commit","-m","fix: roteiros setores correto + clientes por carteira + promotor"],
        capture_output=True, text=True)
    print("Commit:", r2.stdout.strip() or r2.stderr.strip())
    r3 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r3.stdout.strip() or r3.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
    lines = c.split('\n')
    for i in range(max(0,e.lineno-3), min(len(lines),e.lineno+2)):
        print(f"  {i+1}: {lines[i]}")
