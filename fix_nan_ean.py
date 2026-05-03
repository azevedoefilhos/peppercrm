#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

OLD = '''          AND (pc.ean_concorrente IS NULL OR pc.ean_concorrente='')
          AND pc.ativo=1'''

NEW = '''          AND (pc.ean_concorrente IS NULL OR pc.ean_concorrente='' OR pc.ean_concorrente='nan')
          AND pc.ativo=1'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    print("OK")
else:
    print("NAO ENCONTRADO")

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("Salvo")
