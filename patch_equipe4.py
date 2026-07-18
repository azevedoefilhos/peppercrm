with open('equipe.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Remove debug
antigo = '''    # DEBUG TEMPORARIO
    st.write(f"DEBUG: eid={eid} | vends_u={len(vends_u)} | vends_leg={len(vends_leg)}")

    '''
novo = '''    '''

if antigo in c:
    c = c.replace(antigo, novo)
    print("OK: debug removido")
else:
    # Tenta variante
    antigo2 = '    # DEBUG TEMPORARIO\n    st.write(f"DEBUG: eid={eid} | vends_u={len(vends_u)} | vends_leg={len(vends_leg)}")\n\n    '
    if antigo2 in c:
        c = c.replace(antigo2, '    ')
        print("OK: debug removido (variante)")
    else:
        print("debug nao encontrado - ok")

with open('equipe.py', 'w', encoding='utf-8') as f:
    f.write(c)

import ast
try:
    ast.parse(open('equipe.py').read())
    print("Sintaxe OK")
except Exception as e:
    print(f"ERRO: {e}")
