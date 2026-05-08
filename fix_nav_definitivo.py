import pathlib

lines = pathlib.Path("pesquisa.py").read_text(encoding="utf-8").splitlines()

# Verifica estado atual da linha 1100
print("Estado atual linhas 1147-1182:")
for i in range(1146, 1183):
    print(i+1, lines[i][:80].encode('ascii','replace').decode())
