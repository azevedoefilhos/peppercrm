c = open('permissoes.py', encoding='utf-8').read()
# Mostra apenas o bloco MODULOS
idx_ini = c.find('MODULOS = {')
idx_fim = c.find('\n}', idx_ini) + 2
print(c[idx_ini:idx_fim])
