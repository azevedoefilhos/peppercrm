import pathlib
lines = pathlib.Path("pesquisa.py").read_text(encoding="utf-8").splitlines()
for i, l in enumerate(lines, 1):
    if 'def _campo_navegacao' in l and i < 1200:
        for j in range(i-1, min(i+85, len(lines))):
            print(j+1, lines[j][:90].encode('ascii','replace').decode())
        break
