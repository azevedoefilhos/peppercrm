#!/usr/bin/env python3
import pathlib
src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
lines = src.splitlines()

# Ver a parte onde os botoes de produto sao renderizados
for i in range(3760, 3850):
    print(i+1, lines[i][:90].encode('ascii','replace').decode())
