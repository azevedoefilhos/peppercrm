import ast, subprocess

with open('cadastros.py', 'r', encoding='utf-8') as f:
    c = f.read()

cnt = 0

# 1. Central de Compras — query inicial sem filtro
antigo1 = ('    clientes = query("""\n'
           '        SELECT cliente_id,\n'
           "               nome_fantasia || ' \u2014 ' || COALESCE(status,'Ativo') AS label\n"
           '        FROM cliente\n'
           '        ORDER BY nome_fantasia\n'
           '    """)\n'
           '    if not clientes:\n'
           '        st.info("Cadastre um cliente primeiro."); return')

novo1 = ('    from permissoes import get_lista_clientes\n'
         '    _clis_cc = get_lista_clientes(so_ativos=False)\n'
         '    clientes = [(r[0], r[1]) for r in _clis_cc] if _clis_cc else []\n'
         '    if not clientes:\n'
         '        st.info("Cadastre um cliente primeiro."); return')

if antigo1 in c:
    c = c.replace(antigo1, novo1, 1)
    print("OK: Central de Compras filtrada")
    cnt += 1
else:
    print("AVISO: Central de Compras padrao nao encontrado — buscando variante")
    idx = c.find('FROM cliente\n        ORDER BY nome_fantasia')
    if idx > 0:
        linha = c[:idx].count('\n') + 1
        print(f"  Variante encontrada linha {linha}")

# 2. PDVs por Setor — busca contexto real
idx_setor = c.find('pdvs_setor = query')
if idx_setor > 0:
    linha_setor = c[:idx_setor].count('\n') + 1
    trecho = c[idx_setor:idx_setor+300]
    print(f"\nPDVs por Setor linha {linha_setor}:")
    print(repr(trecho[:200]))
else:
    print("\nPDVs por Setor: nao encontrado 'pdvs_setor'")
    # Busca por setor
    for i, l in enumerate(c.split('\n'), 1):
        if 'setor' in l.lower() and 'GROUP BY' in l:
            print(f"  linha {i}: {l.strip()}")

with open('cadastros.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c)
    print(f"\nSintaxe OK")
    if cnt > 0:
        subprocess.run(["git","add","cadastros.py"])
        r = subprocess.run(["git","commit","-m","fix: central compras filtrada por perfil"],
                           capture_output=True, text=True)
        print("Commit:", r.stdout.strip() or r.stderr.strip())
        r2 = subprocess.run(["git","push"], capture_output=True, text=True)
        print("Push:", r2.stdout.strip() or r2.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
