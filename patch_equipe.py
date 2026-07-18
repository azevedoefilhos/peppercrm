# patch_equipe.py - corrige a query de vendedores substituindo IN por OR
import re

with open('equipe.py', 'r', encoding='utf-8') as f:
    conteudo = f.read()

print(f"Tamanho original: {len(conteudo)}")

# Substituicao cirurgica
antigo = """AND u.tipo IN ('REPRESENTANTE_ADM','REPRESENTANTE','VENDEDOR','MASTER')"""
novo   = """AND (u.tipo='REPRESENTANTE_ADM' OR u.tipo='REPRESENTANTE' OR u.tipo='VENDEDOR' OR u.tipo='MASTER')"""

if antigo in conteudo:
    conteudo = conteudo.replace(antigo, novo)
    print("OK: IN substituido por OR")
elif "OR u.tipo='VENDEDOR'" in conteudo:
    print("JA CORRIGIDO: OR ja existe")
else:
    print("ATENCAO: padrao nao encontrado")
    # Mostra contexto
    idx = conteudo.find("AND u.tipo")
    if idx >= 0:
        print("Encontrado:", repr(conteudo[idx:idx+100]))

with open('equipe.py', 'w', encoding='utf-8') as f:
    f.write(conteudo)

print(f"Tamanho final: {len(conteudo)}")

# Verifica resultado
with open('equipe.py', 'r', encoding='utf-8') as f:
    novo_conteudo = f.read()
print("OR presente:", "OR u.tipo='VENDEDOR'" in novo_conteudo)
print("IN presente:", "IN ('REPRESENTANTE_ADM','REPRESENTANTE','VENDEDOR','MASTER')" in novo_conteudo)
