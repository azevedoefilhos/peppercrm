import pathlib
lines = pathlib.Path("pesquisa.py").read_text(encoding="utf-8").splitlines()
# Ver _campo_navegacao segunda instancia (linha 3023)
for i in range(3022, 3095):
    print(i+1, lines[i][:90].encode('ascii','replace').decode())
