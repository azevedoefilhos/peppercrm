import pathlib

lines = pathlib.Path("pesquisa.py").read_text(encoding="utf-8").splitlines()

# Ver o que ha entre linha 2620-2635 para confirmar ponto de corte
print("Linhas 2625-2635:")
for i in range(2624, 2635):
    print(i+1, lines[i][:70].encode('ascii','replace').decode())
