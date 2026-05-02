#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

OLD = '''            # Determina produto_id de referência
            pid_ref    = produto_id if tipo == "nosso" else None
            pc_id_ref  = pc_id     if tipo == "conc"  else None'''

NEW = '''            # Determina produto_id de referência
            # tipo pode ser: "nosso", "conc" ou "concorrente"
            pid_ref   = produto_id if tipo == "nosso" else None
            pc_id_ref = pc_id if tipo in ("conc", "concorrente") else None'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    print("OK")
else:
    print("NAO ENCONTRADO")
    # Mostra contexto
    idx = src.find("pid_ref")
    print(repr(src[idx-20:idx+120]))

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("Salvo")
