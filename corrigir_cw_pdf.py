#!/usr/bin/env python3
import pathlib, re

CAMINHO = pathlib.Path("pesquisa.py")
src = CAMINHO.read_text(encoding="utf-8")

# Localiza a linha exata com as larguras
for i, l in enumerate(src.splitlines(), 1):
    if '3.5*cm' in l and '1.8*cm' in l and 'cw' in l and '2.0*cm' in l:
        print(f"Linha {i}: {repr(l)}")

# Substitui usando regex
src2 = re.sub(
    r'(cw\s*=\s*\[)1\.8\*cm,\s*3\.5\*cm,\s*2\.5\*cm,\s*3\.5\*cm,\s*1\.8\*cm,\s*2\.0\*cm(\])',
    r'\g<1>1.8*cm, 5.5*cm, 3.0*cm, 6.0*cm, 2.0*cm, 2.5*cm\g<2>',
    src
)
src2 = re.sub(
    r'(cw\s*\+=\s*\[)2\.0\*cm,\s*2\.5\*cm,\s*2\.0\*cm(\])',
    r'\g<1>2.5*cm, 2.5*cm, 1.8*cm\g<2>',
    src2
)

if src2 != src:
    CAMINHO.write_text(src2, encoding="utf-8")
    print("✅ Larguras corrigidas")
else:
    print("⚠️  Nenhuma alteração")
