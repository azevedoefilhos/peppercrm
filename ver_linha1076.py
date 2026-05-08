import pathlib
lines = pathlib.Path("pesquisa.py").read_text(encoding="utf-8").splitlines()
# Ver contexto ao redor da linha 1076
for i in range(1055, 1100):
    print(i+1, lines[i][:90].encode('ascii','replace').decode())
