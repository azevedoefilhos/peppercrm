#!/usr/bin/env python3
import pathlib, re

src = pathlib.Path("database.py").read_text(encoding="utf-8")

# Ver contexto do regex com _cols
idx = src.find('vigencia|data_upload')
print(src[idx-300:idx+300])
