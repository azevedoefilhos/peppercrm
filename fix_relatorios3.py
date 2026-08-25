import ast, subprocess

with open('relatorios.py', 'r', encoding='utf-8') as f:
    c = f.read()

cnt = 0

# ═══════════════════════════════════════════════════
# 1. _FILTRO_BASE — adiciona funcao que retorna filtro dinamico
# ═══════════════════════════════════════════════════
antigo_fb = '''_FILTRO_BASE = """
    FROM pedido_item pi
    JOIN pedido  p  ON pi.pedido_id  = p.pedido_id
    JOIN produto pr ON pi.produto_id = pr.produto_id
    JOIN cliente c  ON p.cliente_id  = c.cliente_id
    JOIN fornecedor f ON p.fornecedor_id = f.fornecedor_id
    LEFT JOIN categoria cat ON pr.categoria_id = cat.categoria_id
    WHERE p.status_pedido  NOT IN ('CANCELADO','RECUSADO')
      AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO')
"""'''

novo_fb = '''_FILTRO_BASE = """
    FROM pedido_item pi
    JOIN pedido  p  ON pi.pedido_id  = p.pedido_id
    JOIN produto pr ON pi.produto_id = pr.produto_id
    JOIN cliente c  ON p.cliente_id  = c.cliente_id
    JOIN fornecedor f ON p.fornecedor_id = f.fornecedor_id
    LEFT JOIN categoria cat ON pr.categoria_id = cat.categoria_id
    WHERE p.status_pedido  NOT IN ('CANCELADO','RECUSADO')
      AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO')
"""

def _filtro_base_params():
    """Retorna (where_extra, params) de perfil para usar com _FILTRO_BASE."""
    try:
        from permissoes import get_where_cliente
        w, p = get_where_cliente("c")
        return (f"AND {w.lstrip('AND ').strip()}" if w else ""), p
    except Exception:
        return "", []'''

if antigo_fb in c:
    c = c.replace(antigo_fb, novo_fb)
    print("OK: _filtro_base_params adicionado")
    cnt += 1
else:
    print("AVISO: _FILTRO_BASE nao encontrado")

# Aplica _filtro_base_params em _rel_fornecedor
antigo_forn = ('    dados = query(f"""\n'
               '        SELECT f.nome_fantasia                           AS fornecedor,\n'
               '               COUNT(DISTINCT p.pedido_id)               AS pedidos,\n'
               '               COUNT(DISTINCT p.cliente_id)              AS clientes,\n'
               '               SUM(pi.quantidade)                        AS caixas,\n'
               '               ROUND(SUM({_VALOR_ITEM}), 2)              AS total\n'
               '        {_FILTRO_BASE}\n'
               '          AND p.data_pedido BETWEEN {d_ini} AND {d_fim}\n'
               '        GROUP BY f.fornecedor_id\n'
               '        ORDER BY total DESC\n'
               '    """)')

novo_forn = ('    _wfb, _pfb = _filtro_base_params()\n'
             '    dados = query(f"""\n'
             '        SELECT f.nome_fantasia                           AS fornecedor,\n'
             '               COUNT(DISTINCT p.pedido_id)               AS pedidos,\n'
             '               COUNT(DISTINCT p.cliente_id)              AS clientes,\n'
             '               SUM(pi.quantidade)                        AS caixas,\n'
             '               ROUND(SUM({_VALOR_ITEM}), 2)              AS total\n'
             '        {_FILTRO_BASE}\n'
             '          {_wfb}\n'
             '          AND p.data_pedido BETWEEN {d_ini} AND {d_fim}\n'
             '        GROUP BY f.fornecedor_id\n'
             '        ORDER BY total DESC\n'
             '    """, tuple(_pfb))')

if antigo_forn in c:
    c = c.replace(antigo_forn, novo_forn)
    print("OK: _rel_fornecedor usa _filtro_base_params")
    cnt += 1
else:
    print("AVISO: padrao _rel_fornecedor nao encontrado")

# ═══════════════════════════════════════════════════
# 2. _rel_sem_pedido — adiciona filtro de perfil no WHERE
# ═══════════════════════════════════════════════════
antigo_sp = ('    where_forn = "AND p2.fornecedor_id=?" if forn_id else ""\n'
             '    params = [forn_id] if forn_id else []\n'
             '    params_sub = [forn_id] if forn_id else []')

novo_sp = ('    from permissoes import get_where_cliente\n'
           '    _w_sp, _p_sp = get_where_cliente("c")\n'
           '    _where_sp = f"AND {_w_sp.lstrip(\'AND \').strip()}" if _w_sp else ""\n'
           '    where_forn = "AND p2.fornecedor_id=?" if forn_id else ""\n'
           '    params = list(_p_sp) + ([forn_id] if forn_id else [])\n'
           '    params_sub = list(_p_sp) + ([forn_id] if forn_id else [])')

if antigo_sp in c:
    c = c.replace(antigo_sp, novo_sp)
    print("OK: _rel_sem_pedido com params de perfil")
    cnt += 1
else:
    print("AVISO: padrao _rel_sem_pedido nao encontrado")

# Aplica _where_sp no WHERE da query sem_pedido
antigo_sp2 = ('        WHERE c.ativo!=0\n'
              '          {where_tipo_pdv}\n'
              '          AND NOT EXISTS (')

novo_sp2 = ('        WHERE c.ativo!=0\n'
            '          {_where_sp}\n'
            '          {where_tipo_pdv}\n'
            '          AND NOT EXISTS (')

if antigo_sp2 in c:
    c = c.replace(antigo_sp2, novo_sp2)
    print("OK: _rel_sem_pedido WHERE com filtro de perfil")
    cnt += 1
else:
    print("AVISO: WHERE sem_pedido nao encontrado")

# ═══════════════════════════════════════════════════
# 3. _rel_cluster — corrige JOIN e adiciona filtro
# ═══════════════════════════════════════════════════
antigo_cl = ('        FROM cliente c\n'
             '        JOIN pdv ON pdv.pdv_id = c.cliente_id\n'
             '        LEFT JOIN pedido p ON p.cliente_id = c.cliente_id\n'
             '            AND p.status_pedido NOT IN (\'CANCELADO\',\'RECUSADO\')\n'
             '            {_forn_where}\n'
             '        WHERE c.status NOT IN (\'Inativo\',\'Encerrado\')\n'
             '          AND (? = \'Todos\' OR pdv.cluster = ?)\n'
             '          AND (? = \'Todos\' OR pdv.tamanho_pdv = ?)')

novo_cl = ('        FROM cliente c\n'
           '        JOIN pdv ON pdv.cliente_id = c.cliente_id\n'
           '        LEFT JOIN pedido p ON p.cliente_id = c.cliente_id\n'
           '            AND p.status_pedido NOT IN (\'CANCELADO\',\'RECUSADO\')\n'
           '            {_forn_where}\n'
           '        WHERE c.status NOT IN (\'Inativo\',\'Encerrado\')\n'
           '          {_where_cl}\n'
           '          AND (? = \'Todos\' OR pdv.cluster = ?)\n'
           '          AND (? = \'Todos\' OR pdv.tamanho_pdv = ?)')

if antigo_cl in c:
    c = c.replace(antigo_cl, novo_cl)
    print("OK: _rel_cluster JOIN corrigido + filtro perfil")
    cnt += 1
else:
    print("AVISO: padrao cluster nao encontrado")

# Adiciona _where_cl antes da query cluster
antigo_cl2 = ('    _forn_id_cob = int(forn_sel[0]) if str(forn_sel[0]).lower() != \'todos\' else None\n'
              '    _forn_where  = "AND p.fornecedor_id = ?" if _forn_id_cob else ""\n'
              '    _forn_params = (_forn_id_cob,) if _forn_id_cob else ()')

novo_cl2 = ('    from permissoes import get_where_cliente\n'
            '    _w_cl, _p_cl = get_where_cliente("c")\n'
            '    _where_cl = f"AND {_w_cl.lstrip(\'AND \').strip()}" if _w_cl else ""\n'
            '    _forn_id_cob = int(forn_sel[0]) if str(forn_sel[0]).lower() != \'todos\' else None\n'
            '    _forn_where  = "AND p.fornecedor_id = ?" if _forn_id_cob else ""\n'
            '    _forn_params = ((_forn_id_cob,) if _forn_id_cob else ()) + tuple(_p_cl)')

if antigo_cl2 in c:
    c = c.replace(antigo_cl2, novo_cl2)
    print("OK: _rel_cluster _where_cl definido")
    cnt += 1
else:
    print("AVISO: padrao _forn_id_cob nao encontrado")

# ═══════════════════════════════════════════════════
# 4. _rel_competitivo — filtra pesquisas por cliente do vendedor
# ═══════════════════════════════════════════════════
antigo_comp = ('        WHERE ppi.produto_id=?\n'
               '          AND ppi.produto_concorrente_id IS NULL\n'
               '          AND pp.fornecedor_id=?\n'
               '          AND pp.status=\'finalizado\'\n'
               '          AND pp.data_pesquisa >= date(\'now\',\'-{dias} days\')\n'
               '          AND ppi.preco IS NOT NULL\n'
               '        ORDER BY pp.data_pesquisa DESC\n'
               '        LIMIT 1\n'
               '    """, (pid, forn_sel[0]))')

novo_comp = ('        WHERE ppi.produto_id=?\n'
             '          AND ppi.produto_concorrente_id IS NULL\n'
             '          AND pp.fornecedor_id=?\n'
             '          AND pp.status=\'finalizado\'\n'
             '          AND pp.data_pesquisa >= date(\'now\',\'-{dias} days\')\n'
             '          AND ppi.preco IS NOT NULL\n'
             '          AND pp.cliente_id IN (SELECT cliente_id FROM cliente c WHERE 1=1 {_w_comp_sql})\n'
             '        ORDER BY pp.data_pesquisa DESC\n'
             '        LIMIT 1\n'
             '    """, tuple([pid, forn_sel[0]] + _p_comp))')

# Adiciona _w_comp antes da query competitivo
antigo_comp2 = ('    pid       = prod_sel[0]\n'
                '    prod_nome = prod_sel[1] or prod_sel[2]\n'
                '    prod_peso = prod_sel[3]\n'
                '    prod_um   = prod_sel[4]\n'
                '    dias      = int(per_sel[0])')

novo_comp2 = ('    pid       = prod_sel[0]\n'
              '    prod_nome = prod_sel[1] or prod_sel[2]\n'
              '    prod_peso = prod_sel[3]\n'
              '    prod_um   = prod_sel[4]\n'
              '    dias      = int(per_sel[0])\n'
              '    from permissoes import get_where_cliente\n'
              '    _w_comp, _p_comp = get_where_cliente("c")\n'
              '    _w_comp_sql = _w_comp if _w_comp else ""')

if antigo_comp2 in c:
    c = c.replace(antigo_comp2, novo_comp2)
    print("OK: _rel_competitivo _w_comp definido")
    cnt += 1

if antigo_comp in c:
    c = c.replace(antigo_comp, novo_comp)
    print("OK: _rel_competitivo nosso_preco filtrado por cliente")
    cnt += 1
else:
    print("AVISO: padrao competitivo nosso_preco nao encontrado")

print(f"\nTotal: {cnt} correcoes")

with open('relatorios.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c)
    print("Sintaxe OK")
    subprocess.run(["git","add","relatorios.py"])
    r = subprocess.run(["git","commit","-m","fix: relatorios fornecedor sem_pedido cluster competitivo filtrados"],
                       capture_output=True, text=True)
    print("Commit:", r.stdout.strip() or r.stderr.strip())
    r2 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r2.stdout.strip() or r2.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
    linhas = c.split('\n')
    for i in range(max(0,e.lineno-3), min(len(linhas), e.lineno+2)):
        print(f"  {i+1}: {linhas[i]}")
