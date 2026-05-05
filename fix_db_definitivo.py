#!/usr/bin/env python3
import pathlib

src = pathlib.Path("database.py").read_text(encoding="utf-8")
original = src

# Remove os regex antigos de strftime que usam ([^)]+) - causam o problema ::DATE
OLD1 = '''    sql = re.sub(r"strftime\\('%Y-%m',\\s*([^)]+)\\)",
        lambda m: f"TO_CHAR({m.group(1).strip()}::DATE, 'YYYY-MM')", sql)
    sql = re.sub(r"strftime\\('%Y',\\s*([^)]+)\\)",
        lambda m: f"TO_CHAR({m.group(1).strip()}::DATE, 'YYYY')", sql)
    sql = re.sub(r"strftime\\('%m',\\s*([^)]+)\\)",
        lambda m: f"TO_CHAR({m.group(1).strip()}::DATE, 'MM')", sql)'''

if OLD1 in src:
    src = src.replace(OLD1, '')
    print("OK: removidos regex antigos strftime")
else:
    # Tenta linha por linha
    lines = src.splitlines()
    new_lines = []
    removed = 0
    for l in lines:
        if ("strftime('%Y-%m'" in l or "strftime('%Y'" in l or "strftime('%m'" in l) and '::DATE' in l:
            removed += 1
            print(f"Removendo: {l.strip()[:70]}")
            # Pula esta linha e a proxima (lambda)
            continue
        if removed > 0 and 'lambda m: f"TO_CHAR' in l and removed <= 3:
            removed -= 1
            continue
        new_lines.append(l)
    src = '\n'.join(new_lines)
    print("OK via linha a linha")

if src != original:
    pathlib.Path("database.py").write_text(src, encoding="utf-8")
    print("Salvo")
else:
    print("NADA MUDOU")
