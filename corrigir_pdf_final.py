#!/usr/bin/env python3
import pathlib

CAMINHO = pathlib.Path("pesquisa.py")
src = CAMINHO.read_text(encoding="utf-8")
original = src

# ── 1. Fix filtro fornecedor no PDF por PDV ───────────────────────────────
ANTIGO_FILTRO = '''    # Monta where da pesquisa
    where_pdv  = list(where_base)
    params_pdv = list(params_base)
    where_pdv.append("pp.cliente_id=?"); params_pdv.append(cli_id_sel)'''

NOVO_FILTRO = '''    # Monta where da pesquisa
    where_pdv  = list(where_base)
    params_pdv = list(params_base)
    where_pdv.append("pp.fornecedor_id=?"); params_pdv.append(forn_p[0])
    where_pdv.append("pp.cliente_id=?"); params_pdv.append(cli_id_sel)'''

if ANTIGO_FILTRO in src:
    src = src.replace(ANTIGO_FILTRO, NOVO_FILTRO, 1)
    print("✅ Fix 1: filtro fornecedor_id adicionado na query por PDV")
else:
    print("⚠️  Fix 1: padrão não encontrado")

# ── 2. Fix larguras por_produto ───────────────────────────────────────────
src = src.replace(
    '    cw_base = [3.5*cm, 1.8*cm, 2.2*cm, 3.0*cm, 1.5*cm,\n               1.8*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.2*cm, 1.8*cm]',
    '    cw_base = [5.0*cm, 1.8*cm, 2.5*cm, 4.5*cm, 1.8*cm,\n               2.0*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.2*cm, 2.5*cm]'
)
print("✅ Fix 2: por_produto larguras ajustadas" if src != original else "⚠️  Fix 2: sem alteração")

# ── 3. Fix larguras por_marca ─────────────────────────────────────────────
src = src.replace(
    '        cw = [3.5*cm, 3.0*cm, 1.5*cm, 3.5*cm, 1.8*cm, 1.8*cm]',
    '        cw = [4.5*cm, 5.0*cm, 1.8*cm, 5.5*cm, 2.0*cm, 2.0*cm]'
)
src = src.replace(
    '            cw += [1.8*cm, 2.2*cm, 2.0*cm]\n        colunas.append("Data")',
    '            cw += [2.0*cm, 2.2*cm, 1.8*cm]\n        colunas.append("Data")'
)
print("✅ Fix 3: por_marca larguras ajustadas")

# ── 4. Fix por_categoria: landscape + larguras ────────────────────────────
src = src.replace(
    '    doc = SimpleDocTemplate(buf, pagesize=A4,\n                            leftMargin=1.5*cm, rightMargin=1.5*cm,\n                            topMargin=1.5*cm, bottomMargin=1.5*cm)\n    el  = []\n\n    _pdf_cabecalho(el, s,\n        "Analise por Categoria"',
    '    doc = SimpleDocTemplate(buf, pagesize=landscape(A4),\n                            leftMargin=1.5*cm, rightMargin=1.5*cm,\n                            topMargin=1.5*cm, bottomMargin=1.5*cm)\n    el  = []\n\n    _pdf_cabecalho(el, s,\n        "Analise por Categoria"'
)
src = src.replace(
    '    cw      = [4.5*cm, 2.0*cm, 2.0*cm, 2.5*cm, 2.0*cm, 2.5*cm, 2.5*cm, 2.5*cm]',
    '    cw      = [5.5*cm, 1.8*cm, 1.8*cm, 2.2*cm, 1.8*cm, 2.8*cm, 2.5*cm, 2.5*cm]'
)
print("✅ Fix 4: por_categoria landscape + larguras ajustadas")

CAMINHO.write_text(src, encoding="utf-8")
print(f"\nAlterado: {src != original}")
