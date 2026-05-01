#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
old = 'st.session_state[f"ean_input_{pq_id}"] = ""'
new = 'st.session_state.pop(f"ean_input_{pq_id}", None)'
src2 = src.replace(old, new)
pathlib.Path("pesquisa.py").write_text(src2, encoding="utf-8")
print("OK" if src != src2 else "NAO ENCONTRADO")
