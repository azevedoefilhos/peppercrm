#!/usr/bin/env python3
"""
Corrige larguras de colunas em todos os PDFs de análise de pesquisa.
Padrão: landscape A4 = 29.7cm, margens 1.5cm cada lado = 26.7cm úteis
         A4 portrait = 21.0cm, margens 1.5cm cada lado = 18.0cm úteis
"""
import pathlib, re

CAMINHO = pathlib.Path("pesquisa.py")
src = CAMINHO.read_text(encoding="utf-8")
original = src

# ── 1. por_produto: landscape A4, 26.7cm úteis ───────────────────────────
# Colunas: Cliente-PDV, TipoPDV, Marca, ProdConc, TipoRel, UltPreco, Medio, Min, Max, Pesq, Data
# Atual:   3.5, 1.8, 2.2, 3.0, 1.5, 1.8, 1.8, 1.8, 1.8, 1.2, 1.8 = 22.2cm
# Novo:    5.0, 1.8, 2.5, 4.5, 1.8, 2.0, 1.8, 1.8, 1.8, 1.2, 2.5 = 26.7cm
src = src.replace(
    '    cw_base = [3.5*cm, 1.8*cm, 2.2*cm, 3.0*cm, 1.5*cm,\n               1.8*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.2*cm, 1.8*cm]',
    '    cw_base = [5.0*cm, 1.8*cm, 2.5*cm, 4.5*cm, 1.8*cm,\n               2.0*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.2*cm, 2.5*cm]'
)
if src != original: print("✅ por_produto: colunas ajustadas")
else: print("⚠️  por_produto: padrão não encontrado")
original2 = src

# ── 2. por_marca: landscape A4, 26.7cm úteis ─────────────────────────────
# Colunas: ProdConc, NossoProd, TipoRel, ClientePDV, TipoPDV, Preco
# Atual:   3.5, 3.0, 1.5, 3.5, 1.8, 1.8 = 15.1cm (muito pequeno!)
# Novo:    4.5, 5.0, 1.8, 6.0, 2.0, 2.0 = 21.3cm (sem tabela) / +tab: 26.7
src = src.replace(
    '        cw = [3.5*cm, 3.0*cm, 1.5*cm, 3.5*cm, 1.8*cm, 1.8*cm]',
    '        cw = [4.5*cm, 5.0*cm, 1.8*cm, 6.5*cm, 2.0*cm, 2.0*cm]'
)
src = src.replace(
    '            cw += [1.8*cm, 2.2*cm, 2.0*cm]\n',
    '            cw += [2.0*cm, 2.2*cm, 1.8*cm]\n'
)
if src != original2: print("✅ por_marca: colunas ajustadas")
else: print("⚠️  por_marca: padrão não encontrado")
original3 = src

# ── 3. por_categoria: portrait A4, 18.0cm úteis ──────────────────────────
# Colunas: Marca, Produtos, PDVs, Ocorrencias, Share, MedPreco, Min, Max
# Atual:   4.5, 2.0, 2.0, 2.5, 2.0, 2.5, 2.5, 2.5 = 20.5cm (excede portrait!)
# Novo:    4.0, 1.5, 1.5, 2.0, 1.8, 2.5, 2.3, 2.3 = 17.9cm
src = src.replace(
    '    cw      = [4.5*cm, 2.0*cm, 2.0*cm, 2.5*cm, 2.0*cm, 2.5*cm, 2.5*cm, 2.5*cm]',
    '    cw      = [4.0*cm, 1.5*cm, 1.5*cm, 2.0*cm, 1.8*cm, 2.5*cm, 2.3*cm, 2.3*cm]'
)
if src != original3: print("✅ por_categoria: colunas ajustadas")
else: print("⚠️  por_categoria: padrão não encontrado")

# ── 4. por_categoria: mudar para landscape para melhor aproveitamento ─────
src = src.replace(
    '    doc = SimpleDocTemplate(buf, pagesize=A4,\n                            leftMargin=1.5*cm, rightMargin=1.5*cm,\n                            topMargin=1.5*cm, bottomMargin=1.5*cm)',
    '    doc = SimpleDocTemplate(buf, pagesize=landscape(A4),\n                            leftMargin=1.5*cm, rightMargin=1.5*cm,\n                            topMargin=1.5*cm, bottomMargin=1.5*cm)',
    1
)
if 'por_categoria' in src: print("✅ por_categoria: mudado para landscape")

CAMINHO.write_text(src, encoding="utf-8")
print(f"\nArquivo salvo. Alterado: {src != open('pesquisa.py').read() == False}")
