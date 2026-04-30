#!/usr/bin/env python3
import pathlib

CAMINHO = pathlib.Path("pesquisa.py")
src = CAMINHO.read_text(encoding="utf-8")

# Largura util landscape A4 = 29.7 - 3.0 (margens) = 26.7cm
# Sem tabela: Data(1.8) + NossoProd(5.5) + Marca(3.0) + ProdConc(6.0) + TipoRel(2.0) + Preco(2.5) = 20.8cm
# Com tabela: + MeuUnit(2.5) + Dif(2.5) + Score(1.8) = 27.6cm -> ajusta para 26.5cm total

ANTIGO = '''        colunas = ["Data","Nosso produto","Marca","Produto concorrente","Tipo rel.","Preco conc."]
        cw      = [1.8*cm, 3.5*cm, 2.5*cm, 3.5*cm, 1.8*cm, 2.0*cm]
        if tem_tab:
            colunas += ["Meu unit. (tab.)","Dif. vs tab.","Score"]
            cw      += [2.0*cm, 2.5*cm, 2.0*cm]'''

NOVO = '''        colunas = ["Data","Nosso produto","Marca","Produto concorrente","Tipo rel.","Preco conc."]
        cw      = [1.8*cm, 5.5*cm, 3.0*cm, 6.0*cm, 2.0*cm, 2.5*cm]
        if tem_tab:
            colunas += ["Meu unit. (tab.)","Dif. vs tab.","Score"]
            cw      += [2.5*cm, 2.5*cm, 1.8*cm]'''

if ANTIGO in src:
    src = src.replace(ANTIGO, NOVO, 1)
    print("✅ Larguras de colunas ajustadas")
else:
    print("⚠️  Padrão não encontrado")

# Remove KeepTogether que força quebra de pagina
# Substitui por simples append da tabela
ANTIGO2 = "        el.append(KeepTogether(_pdf_tabela(rows, colunas, cw, s)))"
NOVO2   = "        el.append(_pdf_tabela(rows, colunas, cw, s))"

if ANTIGO2 in src:
    src = src.replace(ANTIGO2, NOVO2, 1)
    print("✅ KeepTogether removido — tabela flui naturalmente entre páginas")
else:
    print("⚠️  KeepTogether não encontrado")

CAMINHO.write_text(src, encoding="utf-8")
