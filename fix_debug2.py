#!/usr/bin/env python3
import pathlib

lines = pathlib.Path("pesquisa.py").read_text(encoding="utf-8").splitlines()

# Adiciona debug antes do check de produto pendente (linha 1148, index 1147)
lines.insert(1147, '    st.caption(f"DEBUG2: entrou em _campo_navegacao")')
pathlib.Path("pesquisa.py").write_text('\n'.join(lines), encoding="utf-8")
print("OK")
