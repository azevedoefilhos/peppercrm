#!/usr/bin/env python3
import pathlib

src = pathlib.Path("concorrentes.py").read_text(encoding="utf-8")
original = src

OLD = '                    peso=?,unidade_medida=?,ean=?,observacao=?,ativo=?'
NEW = '                    peso=?,unidade_medida=?,ean_concorrente=?,observacao=?,ativo=?'

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    pathlib.Path("concorrentes.py").write_text(src, encoding="utf-8")
    print("OK")
else:
    print("NAO ENCONTRADO")
