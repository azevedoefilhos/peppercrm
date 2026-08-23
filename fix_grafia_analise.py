import ast, subprocess

with open('pesquisa.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Corrige apenas textos visiveis ao usuario (botoes, titulos, labels)
substituicoes = [
    # Botao principal
    ('st.button("📊 Analise consolidada"', 'st.button("📊 Análise consolidada"'),
    # Titulos PDF
    ('"Analise por Produto"', '"Análise por Produto"'),
    ('"Analise por Marca Concorrente"', '"Análise por Marca Concorrente"'),
    ('"Analise por Categoria"', '"Análise por Categoria"'),
    ('"Analise por PDV"', '"Análise por PDV"'),
]

cnt = 0
for antigo, novo in substituicoes:
    n = c.count(antigo)
    if n > 0:
        c = c.replace(antigo, novo)
        print(f"OK: '{antigo[:40]}' -> corrigido ({n}x)")
        cnt += 1

# NAO altera: file_name, variaveis, funcoes (analise_produto, etc)
print(f"\nTotal: {cnt} substituicoes")

with open('pesquisa.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c)
    print("Sintaxe OK")
    subprocess.run(["git","add","pesquisa.py"])
    r = subprocess.run(["git","commit","-m","fix: grafia Analise -> Analise nos textos visiveis"],
                       capture_output=True, text=True)
    print("Commit:", r.stdout.strip() or r.stderr.strip())
    r2 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r2.stdout.strip() or r2.stderr.strip())
except SyntaxError as e:
    print(f"ERRO: {e}")
