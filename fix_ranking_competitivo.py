import ast, subprocess

with open('relatorios.py', 'r', encoding='utf-8') as f:
    c = f.read()

cnt = 0

# 1. Ranking PDV — exclui SUSPENSO alem de CANCELADO
antigo1 = "        WHERE p.status_pedido != 'CANCELADO'\n          AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO')"
novo1   = "        WHERE p.status_pedido NOT IN ('CANCELADO','RECUSADO','SUSPENSO')\n          AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO')"

if antigo1 in c:
    c = c.replace(antigo1, novo1)
    print("OK: Ranking PDV exclui SUSPENSO")
    cnt += 1
else:
    print("AVISO: padrao ranking nao encontrado")

# 2. Remove aba Competitivo do dicionario de abas
antigo2 = '        "competitivo": "⚔️ Competitivo",'
if antigo2 in c:
    c = c.replace(antigo2, '')
    print("OK: aba Competitivo removida do menu")
    cnt += 1
else:
    # Tenta variante
    for variante in ['"competitivo"', "'competitivo'"]:
        idx = c.find(variante)
        if idx > 0:
            linha = c[:idx].count('\n') + 1
            print(f"Competitivo encontrado linha {linha}: {repr(c[idx:idx+60])}")

# 3. Remove chamada ao _rel_competitivo no dispatcher
antigo3 = '    elif a == "competitivo": _rel_competitivo()'
if antigo3 in c:
    c = c.replace(antigo3, '')
    print("OK: chamada _rel_competitivo removida")
    cnt += 1
else:
    antigo3b = '    if a=="competitivo": _rel_competitivo()'
    if antigo3b in c:
        c = c.replace(antigo3b, '')
        print("OK: chamada _rel_competitivo removida (variante)")
        cnt += 1
    else:
        # Busca padrao
        idx = c.find('_rel_competitivo()')
        if idx > 0:
            linha = c[:idx].count('\n') + 1
            print(f"_rel_competitivo() linha {linha}: {repr(c[idx-40:idx+30])}")

with open('relatorios.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c)
    print(f"Sintaxe OK — {cnt} correcoes")
    subprocess.run(["git","add","relatorios.py"])
    r = subprocess.run(["git","commit","-m","fix: ranking exclui suspenso + remove aba competitivo de relatorios"],
                       capture_output=True, text=True)
    print("Commit:", r.stdout.strip() or r.stderr.strip())
    r2 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r2.stdout.strip() or r2.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
