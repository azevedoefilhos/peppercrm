# verificar_resultado.py
# Cole na pasta peppercrm e rode: python verificar_resultado.py

import os, sys

# Força o diretório correto
pasta = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pasta)

print(f"Pasta: {pasta}")
print(f"Arquivo resultado_operacional.py existe? {os.path.exists(os.path.join(pasta, 'resultado_operacional.py'))}")

# Mostra as primeiras 15 linhas do arquivo em disco
arq = os.path.join(pasta, "resultado_operacional.py")
with open(arq, encoding="utf-8") as f:
    linhas = f.readlines()
print(f"\nTotal de linhas no arquivo: {len(linhas)}")
print("\n--- Primeiras 20 linhas ---")
for i, l in enumerate(linhas[:20], 1):
    print(f"{i:3}: {l}", end="")

print("\n\n--- Procurando '_query_safe' e '_garantir_tabela' no arquivo ---")
for i, l in enumerate(linhas, 1):
    if "_query_safe" in l or "_garantir_tabela" in l or "execute_write" in l:
        print(f"  linha {i:3}: {l.rstrip()}")

# Testa a função diretamente
print("\n\n--- Testando _buscar_totais_periodo diretamente ---")
try:
    # Limpa cache de módulo se existir
    if "resultado_operacional" in sys.modules:
        del sys.modules["resultado_operacional"]

    from resultado_operacional import _buscar_totais_periodo, _garantir_tabela_despesa
    print("Import OK")
    _garantir_tabela_despesa()
    print("_garantir_tabela_despesa OK")
    total_com, total_desp = _buscar_totais_periodo("previsto", "2025-12-01", "2026-05-31")
    print(f"total_com  = {total_com}")
    print(f"total_desp = {total_desp}")
except Exception as e:
    import traceback
    print(f"ERRO: {e}")
    traceback.print_exc()
