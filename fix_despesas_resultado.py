import ast, subprocess

# 1. DESPESAS.PY — oculta aba Resultado para Vendedor e PV
with open('despesas.py', 'r', encoding='utf-8') as f:
    c = f.read()

antigo1 = ('    ABAS = {"nova":"➕ Nova despesa",\n'
           '            "lista":"📋 Ver despesas",\n'
           '            "relatorio":"📄 Relatório PDF",\n'
           '            "resultado":"💰 Resultado"}')

novo1 = ('    from permissoes import e_representante, e_admin, e_master\n'
         '    _pode_resultado = e_representante() or e_admin() or e_master()\n'
         '    ABAS = {"nova":"➕ Nova despesa",\n'
         '            "lista":"📋 Ver despesas",\n'
         '            "relatorio":"📄 Relatório PDF"}\n'
         '    if _pode_resultado:\n'
         '        ABAS["resultado"] = "💰 Resultado"')

if antigo1 in c:
    c = c.replace(antigo1, novo1)
    print("OK: aba Resultado ocultada para Vendedor/PV")
else:
    print("AVISO: padrao ABAS despesas nao encontrado")
    idx = c.find('ABAS = {"nova"')
    if idx > 0:
        print(f"Contexto: {repr(c[idx:idx+200])}")

with open('despesas.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c); print("despesas: Sintaxe OK")
except SyntaxError as e:
    print(f"ERRO: {e}")

# 2. RESULTADO_OPERACIONAL.PY — filtra por vendedor_id
with open('resultado_operacional.py', 'r', encoding='utf-8') as f:
    r = f.read()

# Adiciona filtro de vendedor nas queries de pedido
antigo2 = ('                 WHERE p.status_pedido = \'ENTREGUE\'\n'
           '                   AND COALESCE(cpag.status_pagamento, \'PENDENTE\') IN (\'PENDENTE\',\'PAGO_PARCIAL\')\n'
           '                   AND COALESCE(p.data_entrega_realizada, p.data_pedido) BETWEEN ? AND ?""",')

novo2 = ('                 WHERE p.status_pedido = \'ENTREGUE\'\n'
         '                   AND COALESCE(cpag.status_pagamento, \'PENDENTE\') IN (\'PENDENTE\',\'PAGO_PARCIAL\')\n'
         '                   AND COALESCE(p.data_entrega_realizada, p.data_pedido) BETWEEN ? AND ?\n'
         '                   {_filtro_vend_sql}""",')

# Adiciona helper de filtro no topo da funcao _buscar_totais_periodo
antigo3 = 'def _buscar_totais_periodo(visao, d_ini, d_fim):'
novo3   = ('def _get_filtro_vendedor():\n'
           '    """Retorna (sql_where, params) para filtrar pedidos pelo representante logado."""\n'
           '    try:\n'
           '        from permissoes import e_admin, e_master, usuario_id_atual, perfil_atual\n'
           '        p = perfil_atual()\n'
           '        uid = usuario_id_atual()\n'
           '        if p in ("MASTER","ADM","REPRESENTANTE_ADM"):\n'
           '            return "", []\n'
           '        elif p in ("REPRESENTANTE","VENDEDOR"):\n'
           '            return "AND p.vendedor_id=?", [uid]\n'
           '        return "", []\n'
           '    except Exception:\n'
           '        return "", []\n'
           '\n'
           'def _buscar_totais_periodo(visao, d_ini, d_fim):')

if antigo3 in r:
    r = r.replace(antigo3, novo3)
    print("OK: _get_filtro_vendedor adicionado")
else:
    print("AVISO: _buscar_totais_periodo nao encontrado")

# Aplica filtro nas queries SQLite de pedido (status ENTREGUE)
antigo4 = ("                 WHERE p.status_pedido = 'ENTREGUE'\n"
           "                   AND COALESCE(cpag.status_pagamento, 'PENDENTE') IN ('PENDENTE','PAGO_PARCIAL')\n"
           "                   AND COALESCE(p.data_entrega_realizada, p.data_pedido) BETWEEN ? AND ?\"\"\"")

novo4 = ("                 WHERE p.status_pedido = 'ENTREGUE'\n"
         "                   AND COALESCE(cpag.status_pagamento, 'PENDENTE') IN ('PENDENTE','PAGO_PARCIAL')\n"
         "                   AND COALESCE(p.data_entrega_realizada, p.data_pedido) BETWEEN ? AND ?\n"
         "                   {_fv_sql}\"\"\"")

# Injeta _fv_sql no inicio da funcao
antigo5 = 'def _buscar_totais_periodo(visao, d_ini, d_fim):\n    if visao == "previsto":'
novo5   = ('def _buscar_totais_periodo(visao, d_ini, d_fim):\n'
           '    _fv_sql, _fv_params = _get_filtro_vendedor()\n'
           '    if visao == "previsto":')

if antigo5 in r:
    r = r.replace(antigo5, novo5)
    print("OK: _fv_sql injetado em _buscar_totais_periodo")

if antigo4 in r:
    r = r.replace(antigo4, novo4)
    print("OK: filtro vendedor na query SQLite ENTREGUE")
else:
    print("AVISO: query SQLite ENTREGUE nao encontrada")

# Ajusta params para incluir _fv_params
antigo6 = '            (d_ini, d_fim)\n        )\n    else:'
novo6   = '            tuple([d_ini, d_fim] + _fv_params)\n        )\n    else:'
if antigo6 in r:
    r = r.replace(antigo6, novo6)
    print("OK: params ENTREGUE com _fv_params")

# Filtro nas despesas por usuario_id
antigo7 = ('        """SELECT ROUND(SUM(valor), 2) FROM despesa\n'
           '           WHERE ativo IS NOT FALSE AND data_despesa BETWEEN ? AND ?""",\n'
           '        """SELECT ROUND(SUM(valor)::NUMERIC, 2) FROM despesa\n'
           '           WHERE ativo IS NOT FALSE AND data_despesa BETWEEN %s AND %s""",\n'
           '        (d_ini, d_fim)')

novo7 = ('        f"""SELECT ROUND(SUM(valor), 2) FROM despesa\n'
         '           WHERE ativo IS NOT FALSE AND data_despesa BETWEEN ? AND ?\n'
         '           {"AND usuario_id=?" if _fv_params else ""}""",\n'
         '        f"""SELECT ROUND(SUM(valor)::NUMERIC, 2) FROM despesa\n'
         '           WHERE ativo IS NOT FALSE AND data_despesa BETWEEN %s AND %s\n'
         '           {"AND usuario_id=%s" if _fv_params else ""}""",\n'
         '        tuple([d_ini, d_fim] + _fv_params)')

if antigo7 in r:
    r = r.replace(antigo7, novo7)
    print("OK: despesas filtradas por usuario_id no resultado")
else:
    print("AVISO: query despesas resultado nao encontrada")

with open('resultado_operacional.py', 'w', encoding='utf-8') as f:
    f.write(r)

try:
    ast.parse(r); print("resultado_operacional: Sintaxe OK")
except SyntaxError as e:
    print(f"ERRO: {e}")
    linhas = r.split('\n')
    for i in range(max(0,e.lineno-3), min(len(linhas), e.lineno+2)):
        print(f"  {i+1}: {linhas[i]}")

subprocess.run(["git","add","despesas.py","resultado_operacional.py"])
r2 = subprocess.run(["git","commit","-m","fix: resultado oculto p/ vendedor + filtro vendedor_id no resultado operacional"],
                    capture_output=True, text=True)
print("Commit:", r2.stdout.strip() or r2.stderr.strip())
r3 = subprocess.run(["git","push"], capture_output=True, text=True)
print("Push:", r3.stdout.strip() or r3.stderr.strip())
