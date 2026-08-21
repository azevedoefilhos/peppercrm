import ast, subprocess

with open('crm_app.py', 'r', encoding='utf-8') as f:
    c = f.read()

linhas = c.split('\n')
novas = []
removidas = 0
for l in linhas:
    if ('sidebar.caption' in l and 'Sessao' in l) or \
       ('usuario_atual()' in l and '_u =' in l) or \
       ('_u.get' in l and 'tipo' in l):
        print(f"Removendo: {l.strip()}")
        removidas += 1
    else:
        novas.append(l)

c = '\n'.join(novas)
print(f"Total removido: {removidas} linhas")

with open('crm_app.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c)
    print("Sintaxe OK")
    subprocess.run(["git","add","crm_app.py"])
    r = subprocess.run(["git","commit","-m","chore: remove debug sessao do dashboard"],
                       capture_output=True, text=True)
    print("Commit:", r.stdout.strip() or r.stderr.strip())
    r2 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r2.stdout.strip() or r2.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
