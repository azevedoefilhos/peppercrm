#!/usr/bin/env python3
"""
Corrige o tradutor julianday no database.py:
- CAST(julianday('now') - julianday(EXPR) AS INTEGER)
  → EXTRACT(DAY FROM (CURRENT_DATE - (EXPR)::DATE))::INTEGER
- julianday('now') - julianday(EXPR)
  → EXTRACT(DAY FROM (CURRENT_DATE - (EXPR)::DATE))

O parêntese ao redor de EXPR é essencial quando EXPR é COALESCE(...) ou outra função.
"""
import pathlib, sys

CAMINHO = pathlib.Path("database.py")
if not CAMINHO.exists():
    print("ERRO: database.py não encontrado.")
    sys.exit(1)

texto = CAMINHO.read_text(encoding="utf-8")

ANTIGO_1 = r"lambda m: f\"EXTRACT(DAY FROM (CURRENT_DATE - {m.group(1).strip()}::DATE))::INTEGER\""
NOVO_1   = r"lambda m: f\"EXTRACT(DAY FROM (CURRENT_DATE - ({m.group(1).strip()})::DATE))::INTEGER\""

ANTIGO_2 = r"lambda m: f\"EXTRACT(DAY FROM (CURRENT_DATE - {m.group(1).strip()}::DATE))\""
NOVO_2   = r"lambda m: f\"EXTRACT(DAY FROM (CURRENT_DATE - ({m.group(1).strip()})::DATE))\""

novo = texto.replace(ANTIGO_1, NOVO_1).replace(ANTIGO_2, NOVO_2)

if novo == texto:
    print("⚠️  Padrão exato não encontrado — tentando substituição por linha...")
    linhas = texto.splitlines()
    alteradas = 0
    for i, linha in enumerate(linhas):
        if "EXTRACT(DAY FROM (CURRENT_DATE -" in linha and "m.group(1).strip()}::DATE)" in linha:
            linhas[i] = linha.replace(
                "{m.group(1).strip()}::DATE)",
                "({m.group(1).strip()})::DATE)"
            )
            alteradas += 1
            print(f"  Linha {i+1} corrigida.")
    if alteradas:
        novo = "\n".join(linhas)
    else:
        print("❌ Nenhuma linha encontrada. Verifique manualmente.")
        sys.exit(1)

CAMINHO.write_text(novo, encoding="utf-8")

# Verificação
c = CAMINHO.read_text(encoding="utf-8")
ok = "({m.group(1).strip()})::DATE)" in c
print("✅ Correção aplicada!" if ok else "⚠️ Verifique manualmente.")
