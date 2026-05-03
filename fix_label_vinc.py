#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

OLD = '            _label_vinc = f"{_dv[1]} — {_dv[0]}" + (f" {_dv[3]}{_dv[2]}" if _dv[3] else "")'
NEW = '            _label_vinc = f"{_dv[1]} — {_dv[0]}"'

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("OK")
else:
    print("NAO ENCONTRADO")
