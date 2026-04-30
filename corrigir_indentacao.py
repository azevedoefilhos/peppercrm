#!/usr/bin/env python3
"""Corrige a indentação de _get_pg_password() no database.py"""
import pathlib, sys

CAMINHO = pathlib.Path("database.py")
if not CAMINHO.exists():
    print("ERRO: database.py não encontrado.")
    sys.exit(1)

texto = CAMINHO.read_text(encoding="utf-8")

ERRADO = """def _get_pg_password():
    import os
    return os.environ.get("SUPABASE_DB_PASSWORD", "")"""

# Versão com indentação quebrada (import e return no nível do módulo)
ERRADO2 = 'def _get_pg_password():\n    import os\n    return os.environ.get("SUPABASE_DB_PASSWORD", "")'

CORRETO = """def _get_pg_password():
    import os
    return os.environ.get("SUPABASE_DB_PASSWORD", "")"""

# Tenta substituição exata primeiro
if ERRADO in texto:
    novo = texto.replace(ERRADO, CORRETO, 1)
    print("Substituição exata aplicada.")
else:
    # Corrige linha a linha
    linhas = texto.splitlines()
    novo_linhas = []
    i = 0
    while i < len(linhas):
        linha = linhas[i]
        if linha.strip() == "def _get_pg_password():":
            novo_linhas.append(linha)
            i += 1
            # Próximas linhas devem ter 4 espaços de indentação
            while i < len(linhas) and linhas[i].strip() in ("import os", 'return os.environ.get("SUPABASE_DB_PASSWORD", "")'):
                novo_linhas.append("    " + linhas[i].strip())
                print(f"  Linha {i+1} reindentada: {linhas[i].strip()}")
                i += 1
        else:
            novo_linhas.append(linha)
            i += 1
    novo = "\n".join(novo_linhas)

CAMINHO.write_text(novo, encoding="utf-8")

# Verificação
c = CAMINHO.read_text(encoding="utf-8")
ok = '    import os\n    return os.environ.get' in c or '    import os\r\n    return os.environ.get' in c
print("✅ Indentação corrigida!" if ok else "⚠️  Verifique manualmente as linhas 95-97.")
