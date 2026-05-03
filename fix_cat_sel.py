#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

OLD = '             (cat_sel[0] if hasattr(cat_sel, \'__getitem__\') else cat_sel) if cat_sel'
NEW = '             (cat_sel[0] if hasattr(cat_sel, \'__getitem__\') else cat_sel) if cat_sel else None,'

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    print("OK")
else:
    # Tenta encontrar variacao
    idx = src.find('cat_sel[0] if hasattr(cat_sel')
    if idx >= 0:
        print("Encontrado em posicao diferente:")
        print(repr(src[idx-10:idx+80]))
    else:
        print("NAO ENCONTRADO")

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("Salvo")
