#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

OLD = '''        # Opcao 1: vincular a concorrente sem EAN
        sem_ean = _lookup_ean_concorrentes_sem_ean(_ean_limpo, forn_id)'''

NEW = '''        # Opcao 1: vincular a concorrente sem EAN
        st.caption(f"DEBUG: forn_id={forn_id} | ean={_ean_limpo}")
        sem_ean = _lookup_ean_concorrentes_sem_ean(_ean_limpo, forn_id)
        st.caption(f"DEBUG: sem_ean count={len(sem_ean) if sem_ean else 0}")'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("OK")
else:
    print("NAO ENCONTRADO")
