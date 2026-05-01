#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
old = '''        _form_coleta_rapida_ean(pq_id,
                                 produto_id=None,
                                 pc_id=resultado["pc_id"],
                                 label=resultado["descricao"],
                                 ean=ean)'''
new = '''        _form_coleta_rapida_ean(pq_id,
                                 tipo="concorrente",
                                 produto_id=None,
                                 pc_id=resultado["pc_id"],
                                 label=resultado["descricao"],
                                 ean=ean)'''
src2 = src.replace(old, new)
pathlib.Path("pesquisa.py").write_text(src2, encoding="utf-8")
print("OK" if src != src2 else "NAO ENCONTRADO")
