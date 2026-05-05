#!/usr/bin/env python3
import pathlib
src = pathlib.Path("database.py").read_text(encoding="utf-8")
idx = src.find("def _traduzir_sql_pg")
print(src[idx:idx+3000])
