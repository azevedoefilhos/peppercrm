#!/usr/bin/env python3
import pathlib, re

src = pathlib.Path("database.py").read_text(encoding="utf-8")
original = src

# Ver o que ja existe na traducao
idx = src.find("def _traduzir_sql_pg")
print(src[idx:idx+600])
