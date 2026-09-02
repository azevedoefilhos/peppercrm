import ast, subprocess

r = subprocess.run(['git','show','HEAD:roteiros.py'], capture_output=True)
c = r.stdout.decode('utf-8', errors='replace').replace('\r\n','\n')

# Verifica o padrao atual antes do novo setor
idx = c.find('# Novo setor')
if idx > 0:
    linha = c[:idx].count('\n') + 1
    print(f"'# Novo setor' na linha {linha}")
    print(f"Contexto anterior: {repr(c[idx-80:idx+30])}")
else:
    print("'# Novo setor' nao encontrado")
    # Busca alternativo
    idx2 = c.find('with st.expander("➕ Novo setor")')
    if idx2 > 0:
        linha2 = c[:idx2].count('\n') + 1
        print(f"'Novo setor expander' na linha {linha2}")
        print(f"Contexto: {repr(c[idx2-100:idx2+50])}")
