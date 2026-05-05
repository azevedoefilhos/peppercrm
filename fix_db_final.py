#!/usr/bin/env python3
import pathlib, re

src = pathlib.Path("database.py").read_text(encoding="utf-8")

# Encontra TODOS os lugares que geram ::DATE
matches = list(re.finditer(r'::DATE', src))
print(f"Ocorrencias de ::DATE: {len(matches)}")
for m in matches:
    print(repr(src[m.start()-80:m.end()+20]))
    print("---")
