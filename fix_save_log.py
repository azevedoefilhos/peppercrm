#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

# Adiciona log imediatamente apos _salvar ser True
OLD = '''        if _salvar:
            if preco <= 0 and not ruptura:
                st.error("Informe o pre\u00e7o ou marque Ruptura.")
                return

            try:'''

NEW = '''        if _salvar:
            st.info(f"DEBUG: salvando {label} | preco={preco} | pc_id={pc_id} | produto_id={produto_id} | tipo={tipo}")
            if preco <= 0 and not ruptura:
                st.error("Informe o pre\u00e7o ou marque Ruptura.")
                return

            try:'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    print("OK")
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
else:
    print("NAO ENCONTRADO")
