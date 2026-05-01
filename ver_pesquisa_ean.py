#!/usr/bin/env python3
import pathlib
src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
lines = src.splitlines()

# Procura referencias a EAN e modo rapido
print("=== Referencias a EAN ===")
for i, l in enumerate(lines, 1):
    if 'ean' in l.lower() and i < 2500:
        print(i, l.encode('ascii', 'replace').decode()[:90])

print("\n=== Referencias a rapido/nova pesquisa ===")
for i, l in enumerate(lines, 1):
    if ('rapido' in l.lower() or 'nova_pesq' in l.lower() or
        'nova pesq' in l.lower() or 'iniciar' in l.lower()) and i < 500:
        print(i, l.encode('ascii', 'replace').decode()[:90])
