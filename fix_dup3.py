#!/usr/bin/env python3
import pathlib

lines = pathlib.Path("pesquisa.py").read_text(encoding="utf-8").splitlines()

# Ver linhas ao redor de 4201
for i in range(4196, 4206):
    print(i+1, repr(lines[i][:80]))

# Remove linha duplicada
del lines[4200]  # linha 4201, index 4200
pathlib.Path("pesquisa.py").write_text('\n'.join(lines), encoding="utf-8")
print("OK")
