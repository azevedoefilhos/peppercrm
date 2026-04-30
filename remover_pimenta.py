#!/usr/bin/env python3
import pathlib

CAMINHO = pathlib.Path("crm_app.py")
src = CAMINHO.read_text(encoding="utf-8")

# Remove page_icon do set_page_config
import re
src2 = re.sub(r',?\s*page_icon\s*=\s*"[^"]*"', '', src)

# Remove 🌶 do título (linha com st.title)
src2 = src2.replace('\U0001f336 {_nome}', '{_nome}')
src2 = src2.replace('\U0001f336 ', '')

CAMINHO.write_text(src2, encoding="utf-8")
print("Alterado:", src != src2)
