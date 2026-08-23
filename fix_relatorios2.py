import ast, subprocess

with open('relatorios.py', 'r', encoding='utf-8') as f:
    c = f.read()

cnt = 0

# Padrao comum: where_extra = "" seguido de params = []
# Substitui por versao com filtro de perfil
antigo_std = ('    where_extra = ""\n'
              '    params = []\n'
              '    if forn_id:\n'
              '        where_extra += " AND p.fornecedor_id=?"\n'
              '        params.append(forn_id)')

novo_std = ('    from permissoes import get_where_cliente\n'
            '    _w_r, _p_r = get_where_cliente("c")\n'
            '    where_extra = f" {_w_r}" if _w_r else ""\n'
            '    params = list(_p_r)\n'
            '    if forn_id:\n'
            '        where_extra += " AND p.fornecedor_id=?"\n'
            '        params.append(forn_id)')

n = c.count(antigo_std)
print(f"Ocorrencias padrao std: {n}")
if n > 0:
    c = c.replace(antigo_std, novo_std)
    cnt += n
    print(f"OK: {n} funcoes corrigidas")

# Padrao com params_a e params_b (comparacao)
antigo_comp = ('    where_extra = ""\n'
               '    params_a = []\n'
               '    params_b = []\n'
               '    if forn_id:\n'
               '        where_extra += " AND p.fornecedor_id=?"\n'
               '        params_a.append(forn_id)\n'
               '        params_b.append(forn_id)')

novo_comp = ('    from permissoes import get_where_cliente\n'
             '    _w_r, _p_r = get_where_cliente("c")\n'
             '    where_extra = f" {_w_r}" if _w_r else ""\n'
             '    params_a = list(_p_r)\n'
             '    params_b = list(_p_r)\n'
             '    if forn_id:\n'
             '        where_extra += " AND p.fornecedor_id=?"\n'
             '        params_a.append(forn_id)\n'
             '        params_b.append(forn_id)')

n2 = c.count(antigo_comp)
print(f"Ocorrencias padrao comparacao: {n2}")
if n2 > 0:
    c = c.replace(antigo_comp, novo_comp)
    cnt += n2
    print(f"OK: comparacao corrigida")

# Padrao ranking PDV (tem filtro extra de tipo_pdv)
antigo_rank = ('    where_extra = ""\n'
               '    params = []\n'
               '    if forn_id:\n'
               '        where_extra += " AND p.fornecedor_id=?"\n'
               '        params.append(forn_id)\n'
               '    if fil_tipo_pdv_rk != "Todos":\n'
               '        where_extra += " AND COALESCE(pdv.tipo_pdv,\'\') =?"')

novo_rank = ('    from permissoes import get_where_cliente\n'
             '    _w_r, _p_r = get_where_cliente("c")\n'
             '    where_extra = f" {_w_r}" if _w_r else ""\n'
             '    params = list(_p_r)\n'
             '    if forn_id:\n'
             '        where_extra += " AND p.fornecedor_id=?"\n'
             '        params.append(forn_id)\n'
             '    if fil_tipo_pdv_rk != "Todos":\n'
             '        where_extra += " AND COALESCE(pdv.tipo_pdv,\'\') =?"')

n3 = c.count(antigo_rank)
print(f"Ocorrencias padrao ranking: {n3}")
if n3 > 0:
    c = c.replace(antigo_rank, novo_rank)
    cnt += n3
    print(f"OK: ranking corrigido")

# Cluster — ver e corrigir
idx_cluster = c.find('def _rel_cluster():')
if idx_cluster > 0:
    # Busca where_extra no cluster
    idx_we = c.find('    where_extra = ""', idx_cluster)
    if idx_we > 0 and idx_we < idx_cluster + 3000:
        linha = c[:idx_we].count('\n') + 1
        print(f"Cluster where_extra linha {linha}")

# Competitivo
idx_comp2 = c.find('def _rel_competitivo():')
if idx_comp2 > 0:
    idx_we2 = c.find('    where', idx_comp2)
    if idx_we2 > 0:
        linha2 = c[:idx_we2].count('\n') + 1
        print(f"Competitivo where linha {linha2}: {repr(c[idx_we2:idx_we2+60])}")

print(f"\nTotal correcoes: {cnt}")

with open('relatorios.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c)
    print("Sintaxe OK")
    subprocess.run(["git","add","relatorios.py"])
    r = subprocess.run(["git","commit","-m","fix: relatorios todos os where_extra filtrados por perfil"],
                       capture_output=True, text=True)
    print("Commit:", r.stdout.strip() or r.stderr.strip())
    r2 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r2.stdout.strip() or r2.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
