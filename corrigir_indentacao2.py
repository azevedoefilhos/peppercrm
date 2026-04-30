#!/usr/bin/env python3
"""Corrige a indentação de _get_pg_password() — def estava dentro de outra função"""
import pathlib, sys

CAMINHO = pathlib.Path("database.py")
texto = CAMINHO.read_text(encoding="utf-8")
linhas = texto.splitlines()

novo = []
i = 0
while i < len(linhas):
    l = linhas[i]
    # Detecta a def indentada errada
    if l == '    def _get_pg_password():':
        # Emite as 3 linhas corretamente no nível do módulo
        novo.append('def _get_pg_password():')
        i += 1
        while i < len(linhas) and linhas[i].strip() in ('import os', 'return os.environ.get("SUPABASE_DB_PASSWORD", "")'):
            novo.append('    ' + linhas[i].strip())
            i += 1
        print("✅ _get_pg_password() reindentada para nível do módulo.")
    else:
        novo.append(l)
        i += 1

CAMINHO.write_text("\n".join(novo), encoding="utf-8")

# Verificação
c = CAMINHO.read_text(encoding="utf-8")
ok = 'def _get_pg_password():\n    import os\n    return' in c
print("✅ Indentação correta!" if ok else "⚠️ Verifique manualmente.")
