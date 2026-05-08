import pathlib
lines = pathlib.Path("pesquisa.py").read_text(encoding="utf-8").splitlines()

# Adiciona na linha 1102 - logo apos o st.caption da navegacao
# Esta linha SEMPRE executa quando _campo_navegacao e chamada
lines.insert(1102, '    st.write("### NAVEGACAO ATIVA")')

pathlib.Path("pesquisa.py").write_text('\n'.join(lines), encoding="utf-8")
print("OK - linha inserida em 1103")
print("Verificando:", lines[1102])
