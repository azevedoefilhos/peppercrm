# diagnostico.py — rode com: python diagnostico.py
# Coloca este arquivo na pasta peppercrm e rode no terminal

import sys, os, traceback

print("=" * 60)
print("DIAGNOSTICO PEPPERCRM")
print("=" * 60)
print(f"Python: {sys.version}")
print(f"Pasta: {os.getcwd()}")
print()

erros = []

# Testa cada modulo
modulos = [
    "database",
    "configuracao",
    "cadastros",
    "pedido",
    "ver_pedidos",
    "relatorios",
    "comissoes",
    "visitas",
    "mix_analise",
    "concorrentes",
    "analise_competitiva",
    "pesquisa",
]

for mod in modulos:
    try:
        if mod in sys.modules:
            del sys.modules[mod]
        m = __import__(mod)
        print(f"  OK  {mod}")
    except Exception as e:
        print(f"  ERRO {mod}:")
        print(f"       {type(e).__name__}: {e}")
        # Mostra traceback completo
        tb = traceback.format_exc()
        for linha in tb.split('\n'):
            if linha.strip() and 'Traceback' not in linha:
                print(f"       {linha}")
        erros.append(mod)
        print()

print()
print("=" * 60)
if erros:
    print(f"MODULOS COM ERRO: {', '.join(erros)}")
    print("Copie o texto acima e envie para correcao.")
else:
    print("TODOS OS MODULOS OK!")
print("=" * 60)
input("\nPressione Enter para fechar...")