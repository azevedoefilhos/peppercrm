#!/usr/bin/env python3
import pathlib
src = pathlib.Path("crm_app.py").read_text(encoding="utf-8")
lines = src.splitlines()
for i, l in enumerate(lines, 1):
    if 'contato' in l.lower() and ('mes' in l.lower() or 'month' in l.lower() or 'mês' in l.lower()):
        print(i, l[:90].encode('ascii','replace').decode())
