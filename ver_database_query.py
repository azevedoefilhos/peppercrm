#!/usr/bin/env python3
import pathlib
src = pathlib.Path("database.py").read_text(encoding="utf-8")
lines = src.splitlines()
for i, l in enumerate(lines, 1):
    if 'LIKE' in l or 'replace' in l.lower() or 'sql_pg' in l or '%s' in l:
        print(i, lines[i-1][:90].encode('ascii','replace').decode())
