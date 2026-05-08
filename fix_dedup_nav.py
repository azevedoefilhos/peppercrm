import pathlib

lines = pathlib.Path("pesquisa.py").read_text(encoding="utf-8").splitlines()
print(f"Total linhas: {len(lines)}")

# A linha 2889 chama _campo_navegacao da segunda instancia (3023)
# A linha 969 chama _campo_navegacao da primeira instancia (1100)
# O app usa _coleta_modo_campo da linha 2845 (segunda instancia)
# que chama _campo_navegacao na linha 2889

# Precisamos fazer a primeira instancia de _campo_navegacao
# usar keys diferentes para nao conflitar
# Solucao simples: adicionar sufixo "_v1" nas keys da primeira instancia

# Ver linhas 1174-1190 (primeira instancia - botoes)
for i in range(1173, 1200):
    print(i+1, lines[i][:80].encode('ascii','replace').decode())
