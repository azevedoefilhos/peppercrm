import ast, subprocess

# Le direto do git
r = subprocess.run(['git','show','HEAD:roteiros.py'], capture_output=True)
c = r.stdout.decode('utf-8', errors='replace')
print(f"Tamanho: {len(c)} bytes")

fixes = 0

# FIX 1: Query resumo setores
antigo1 = ('    resumo = query("""SELECT s.nome, COUNT(p.pdv_id) as total,\n'
           '            SUM(CASE WHEN p.aceita_promotor THEN 1 ELSE 0 END) as c_prom\n'
           '        FROM setor s\n'
           '        LEFT JOIN pdv p ON p.setor_id=s.setor_id AND p.ativo!=0\n'
           '        WHERE s.empresa_id=%s GROUP BY s.setor_id, s.nome\n'
           '        ORDER BY s.codigo""", (eid,)) or []')

novo1 = ('    resumo = query("""SELECT s.nome, COUNT(p.pdv_id) as total,\n'
         '            SUM(CASE WHEN p.aceita_promotor THEN 1 ELSE 0 END) as c_prom\n'
         '        FROM setor s\n'
         '        LEFT JOIN pdv p ON p.setor_id=s.setor_id AND p.ativo!=0\n'
         '        LEFT JOIN cliente cli ON p.cliente_id=cli.cliente_id\n'
         '        WHERE s.empresa_id=%s GROUP BY s.setor_id, s.nome\n'
         '        ORDER BY s.codigo""", (eid,)) or []')

if antigo1 in c:
    c = c.replace(antigo1, novo1); print("OK: resumo setores"); fixes+=1
else:
    print("AVISO: resumo setores")
    # Mostra contexto
    idx = c.find('resumo = query')
    if idx>0: print(f"  {repr(c[idx:idx+200])}")

# FIX 2: Lista clientes roteiro vendedor
antigo2 = ('            clientes = get_lista_clientes(so_ativos=False) if not (e_admin() or e_master()) else \\\n'
           '                       query("SELECT cliente_id, nome_fantasia FROM cliente WHERE empresa_id=%s AND ativo!=0 ORDER BY nome_fantasia", (eid,)) or []')
novo2 = ('            if e_admin() or e_master():\n'
         '                clientes = query("""SELECT cliente_id, nome_fantasia,\n'
         "                    COALESCE(status,'Ativo') FROM cliente\n"
         '                    WHERE empresa_id=%s ORDER BY nome_fantasia""", (eid,)) or []\n'
         '            else:\n'
         '                clientes = query("""SELECT cliente_id, nome_fantasia,\n'
         "                    COALESCE(status,'Ativo') FROM cliente\n"
         '                    WHERE vendedor_id=%s ORDER BY nome_fantasia""", (vend_uid,)) or []')
if antigo2 in c:
    c = c.replace(antigo2, novo2); print("OK: lista clientes vendedor"); fixes+=1
else:
    print("AVISO: lista clientes vendedor")
    idx = c.find('get_lista_clientes')
    if idx>0: print(f"  {repr(c[idx:idx+100])}")

# FIX 3: format_func clientes com status
antigo3 = '                                   format_func=lambda x: x[1], key="rv2_cli")'
novo3 = '                                   format_func=lambda x: f"{x[1]} [{x[2] if len(x)>2 else \'\'}]", key="rv2_cli")'
if antigo3 in c:
    c = c.replace(antigo3, novo3, 1); print("OK: format clientes status"); fixes+=1

# FIX 4: Lista clientes promotor
antigo4 = ('            if e_admin() or e_master():\n'
           '                clientes_p = query("""SELECT DISTINCT c.cliente_id, c.nome_fantasia\n'
           "                    FROM cliente c JOIN pdv p ON p.cliente_id=c.cliente_id\n"
           "                    WHERE p.ativo!=0 AND c.empresa_id=%s AND c.status='Ativo'\n"
           '                    ORDER BY c.nome_fantasia""", (eid,)) or []\n'
           '            elif e_supervisor():\n'
           '                clientes_p = query("""SELECT DISTINCT c.cliente_id, c.nome_fantasia\n'
           "                    FROM cliente c JOIN pdv p ON p.cliente_id=c.cliente_id\n"
           "                    WHERE p.ativo!=0 AND c.empresa_id=%s\n"
           '                    ORDER BY c.nome_fantasia""", (eid,)) or []\n'
           '            else:\n'
           '                clientes_p = query("""SELECT DISTINCT c.cliente_id, c.nome_fantasia\n'
           "                    FROM cliente c JOIN pdv p ON p.cliente_id=c.cliente_id\n"
           "                    WHERE p.ativo!=0 AND c.vendedor_id=%s\n"
           '                    ORDER BY c.nome_fantasia""", (uid,)) or []')

novo4 = ('            if e_admin() or e_master() or e_supervisor():\n'
         '                clientes_p = query("""SELECT DISTINCT c.cliente_id, c.nome_fantasia\n'
         "                    FROM cliente c JOIN pdv p ON p.cliente_id=c.cliente_id\n"
         "                    WHERE p.ativo!=0 AND c.empresa_id=%s AND c.status='Ativo'\n"
         '                    ORDER BY c.nome_fantasia""", (eid,)) or []\n'
         '            else:\n'
         '                clientes_p = query("""SELECT DISTINCT c.cliente_id, c.nome_fantasia\n'
         "                    FROM cliente c JOIN pdv p ON p.cliente_id=c.cliente_id\n"
         "                    WHERE p.ativo!=0 AND c.vendedor_id=%s AND c.status='Ativo'\n"
         '                    ORDER BY c.nome_fantasia""", (uid,)) or []')

if antigo4 in c:
    c = c.replace(antigo4, novo4); print("OK: lista clientes promotor"); fixes+=1
else:
    print("AVISO: lista clientes promotor — buscando")
    idx = c.find('clientes_p = query')
    if idx>0: print(f"  {repr(c[idx:idx+150])}")

# FIX 5: PDVs promotor sem filtro aceita_promotor
antigo5 = ('                pdvs_p = query("""SELECT p.pdv_id, p.nome_loja, p.cidade,\n'
           "                        COALESCE(s.nome,'Sem setor')\n"
           '                    FROM pdv p LEFT JOIN setor s ON p.setor_id=s.setor_id\n'
           '                    WHERE p.cliente_id=%s AND p.ativo!=0 AND p.aceita_promotor=TRUE\n'
           '                    ORDER BY p.nome_loja""", (cli_p[0],)) or []')

novo5 = ('                pdvs_p = query("""SELECT p.pdv_id, p.nome_loja, p.cidade,\n'
         "                        COALESCE(s.nome,'Sem setor'), p.aceita_promotor\n"
         '                    FROM pdv p LEFT JOIN setor s ON p.setor_id=s.setor_id\n'
         '                    WHERE p.cliente_id=%s AND p.ativo!=0\n'
         '                    ORDER BY p.nome_loja""", (cli_p[0],)) or []')

if antigo5 in c:
    c = c.replace(antigo5, novo5); print("OK: PDVs promotor"); fixes+=1
else:
    print("AVISO: PDVs promotor")

print(f"\nTotal: {fixes} correcoes")

with open('roteiros.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c); print("Sintaxe OK")
    subprocess.run(["git","add","roteiros.py"])
    r2 = subprocess.run(["git","commit","-m",
        "fix: roteiros setores query + clientes status + promotor todos PDVs"],
        capture_output=True, text=True)
    print("Commit:", r2.stdout.strip() or r2.stderr.strip())
    r3 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r3.stdout.strip() or r3.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
