# Verifica e corrige erro de sintaxe em visitas.py
import ast

with open('visitas.py', 'r', encoding='utf-8') as f:
    vv = f.read()

# Mostra contexto linha 993
linhas = vv.split('\n')
inicio = max(0, 988)
fim = min(len(linhas), 1000)
print("=== Contexto linha 993 ===")
for i, l in enumerate(linhas[inicio:fim], inicio+1):
    print(f"  {i}: {repr(l)}")

# Tenta parsear para confirmar erro
try:
    ast.parse(vv)
    print("\nSintaxe OK - erro foi corrigido")
except SyntaxError as e:
    print(f"\nErro linha {e.lineno}: {e.msg}")
    # Mostra contexto do erro
    print("Contexto:")
    for i, l in enumerate(linhas[max(0,e.lineno-4):e.lineno+2], max(0,e.lineno-4)+1):
        print(f"  {i}: {repr(l)}")
