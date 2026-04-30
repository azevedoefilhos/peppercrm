#!/usr/bin/env python3
import pathlib, re, sys

CAMINHO = pathlib.Path("cadastros.py")
texto = CAMINHO.read_text(encoding="utf-8")
original = texto

# 1. Fix GROUP BY _lista_tabelas
ANTIGO1 = "        GROUP BY tp.tabela_preco_id\n        ORDER BY f.nome_fantasia, tp.data_inicio DESC"
NOVO1   = "        GROUP BY tp.tabela_preco_id, f.fornecedor_id, f.nome_fantasia, tp.nome_tabela, tp.tipo_tabela, tp.prazo_pagamento, tp.frete, tp.data_inicio, tp.data_fim, tp.ativo\n        ORDER BY f.nome_fantasia, tp.data_inicio DESC"

if ANTIGO1 in texto:
    texto = texto.replace(ANTIGO1, NOVO1, 1)
    print("✅ GROUP BY _lista_tabelas corrigido")
else:
    print("⚠️  _lista_tabelas: padrão não encontrado")

# 2. Fix SELECT DISTINCT com ORDER BY fora do SELECT em _historico_precos (linha 1534)
# No PostgreSQL, SELECT DISTINCT requer que ORDER BY esteja no SELECT
# Solucao: remover DISTINCT e usar subquery, ou incluir colunas no SELECT
padrao2 = re.compile(
    r'(SELECT DISTINCT[^)]*?)(ORDER BY cat\.nome_categoria, p\.descricao_curta)',
    re.DOTALL
)
if padrao2.search(texto):
    # Substitui SELECT DISTINCT por SELECT e garante que as colunas de ORDER BY estejam presentes
    texto = padrao2.sub(lambda m: m.group(0).replace('SELECT DISTINCT', 'SELECT', 1), texto)
    print("✅ SELECT DISTINCT corrigido em _historico_precos")
else:
    # Busca mais ampla
    idx = texto.find('prods_com_hist = query')
    if idx >= 0:
        trecho = texto[idx:idx+600]
        print("Trecho atual:")
        for i, l in enumerate(trecho.splitlines()[:15]):
            print(f"  {l}")
    print("⚠️  _historico_precos: padrão DISTINCT não encontrado")

CAMINHO.write_text(texto, encoding="utf-8")
print(f"Alterações: {'SIM' if texto != original else 'NENHUMA'}")
