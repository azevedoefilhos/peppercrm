#!/usr/bin/env python3
import pathlib

lines = pathlib.Path("pesquisa.py").read_text(encoding="utf-8").splitlines()

# Insere st.caption de debug na linha 1171 (antes do if nossos)
lines.insert(1171, '    st.caption(f"[STATUS] itens no mapa: {len(_mp)}")')

pathlib.Path("pesquisa.py").write_text('\n'.join(lines), encoding="utf-8")
print("OK")
