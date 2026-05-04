#!/usr/bin/env python3
import pathlib

# Fix em concorrentes.py - escapar % no valor de busca
src = pathlib.Path("concorrentes.py").read_text(encoding="utf-8")
original = src

OLD = '        b = f"%{fil_busca.strip()}%"'
NEW = '        _term = fil_busca.strip().replace("%","%%").replace("_","\\_")\n        b = f"%{_term}%"'

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    print("OK concorrentes.py")
    pathlib.Path("concorrentes.py").write_text(src, encoding="utf-8")
else:
    print("NAO ENCONTRADO em concorrentes.py")

# Fix em cadastros.py - busca de produtos
src2 = pathlib.Path("cadastros.py").read_text(encoding="utf-8")
original2 = src2

# Procura padroes de busca LIKE em cadastros.py
for old_pat in [
    '        b = f"%{busca.strip()}%"',
    '        termo = f"%{busca}%"',
    '        _busca = f"%{busca.strip()}%"',
]:
    if old_pat in src2:
        new_pat = old_pat.replace(
            'f"%{', 
            'f"%{"% ".join(("",)).join(str(x).replace("%","%%") for x in [('
        )
        # Abordagem mais simples
        varname = old_pat.split('{')[1].split('}')[0].split('.')[0]
        new_simple = old_pat.replace(
            f'f"%{{{varname}',
            f'f"%{{{varname}.strip().replace("%","%%").replace("_","\\\\_")'
        )
        # Ainda mais simples: adicionar linha de escape antes
        indent = len(old_pat) - len(old_pat.lstrip())
        spaces = ' ' * indent
        varname2 = old_pat.strip().split('=')[0].strip()
        src2 = src2.replace(old_pat, old_pat + '\n' + spaces + f'{varname2} = {varname2}.replace("%%","%%")', 1)
        print(f"OK cadastros.py: {old_pat[:40]}")
        break

# Fix mais direto - no database.py, escapar % nos params quando for LIKE
# Abordagem: modificar _traduzir_sql_pg para lidar com LIKE corretamente
src3 = pathlib.Path("database.py").read_text(encoding="utf-8")
if 'sql.replace("?", "%s")' in src3:
    # Adiciona escape de % nos params apos a traducao
    OLD3 = 'def _traduzir_sql_pg(sql):\n'
    # Ver contexto
    idx = src3.find('def _traduzir_sql_pg(sql):')
    print("\ndatabase.py _traduzir_sql_pg:")
    print(src3[idx:idx+300])
