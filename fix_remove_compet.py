import ast, subprocess

with open('relatorios.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Remove compet do menu ABAS_REL
antigo1 = '        "cluster":"🎯 Cluster","napres":"🏭 Não apresentados",\n        "cobertura":"📡 Cobertura","compet":"⚔️ Competitivo"'
novo1   = '        "cluster":"🎯 Cluster","napres":"🏭 Não apresentados",\n        "cobertura":"📡 Cobertura"'

if antigo1 in c:
    c = c.replace(antigo1, novo1)
    print("OK: compet removido do menu ABAS_REL")
else:
    print("AVISO: padrao menu nao encontrado")

# Remove compet do dispatcher _ABAS_CALL
antigo2 = '        "cluster":_rel_cluster,"napres":_rel_nao_apresentados,\n        "cobertura":_rel_cobertura,"compet":_rel_competitivo'
novo2   = '        "cluster":_rel_cluster,"napres":_rel_nao_apresentados,\n        "cobertura":_rel_cobertura'

if antigo2 in c:
    c = c.replace(antigo2, novo2)
    print("OK: compet removido do dispatcher _ABAS_CALL")
else:
    print("AVISO: padrao dispatcher nao encontrado")

with open('relatorios.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c)
    print("Sintaxe OK")
    subprocess.run(["git","add","relatorios.py"])
    r = subprocess.run(["git","commit","-m","fix: remove aba Competitivo do modulo Relatorios"],
                       capture_output=True, text=True)
    print("Commit:", r.stdout.strip() or r.stderr.strip())
    r2 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r2.stdout.strip() or r2.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
