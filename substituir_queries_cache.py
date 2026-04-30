#!/usr/bin/env python3
"""
Substitui queries repetitivas de listas estáticas por cache_helpers nos módulos principais.
Foca nas queries que aparecem em selectboxes - executadas a cada interação do usuário.
"""
import pathlib, re

total = 0

def substituir(arq, pares):
    global total
    src = pathlib.Path(arq).read_text(encoding="utf-8")
    original = src
    count = 0
    for old, new in pares:
        n = src.count(old)
        if n > 0:
            src = src.replace(old, new)
            count += n
    if src != original:
        # Garante import do cache_helpers
        if "from cache_helpers import" not in src and count > 0:
            src = "from cache_helpers import cache_clientes, cache_fornecedores, cache_categorias, cache_produtos_fornecedor\n" + src
        pathlib.Path(arq).write_text(src, encoding="utf-8")
        print(f"✅ {arq}: {count} substituicao(oes)")
        total += count
    else:
        print(f"  {arq}: sem alteracoes")

# Padroes mais comuns de query de clientes
QUERY_CLIENTES = [
    'query("SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo=1 ORDER BY nome_fantasia")',
    "query('SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo=1 ORDER BY nome_fantasia')",
]
QUERY_FORNS = [
    'query("SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia")',
    "query('SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia')",
]
QUERY_CATS = [
    'query("SELECT categoria_id, nome_categoria FROM categoria WHERE ativo=1 ORDER BY nome_categoria")',
    "query('SELECT categoria_id, nome_categoria FROM categoria WHERE ativo=1 ORDER BY nome_categoria')",
]

# crm_app.py
substituir("crm_app.py", [
    (QUERY_CLIENTES[0], "cache_clientes()"),
    (QUERY_FORNS[0], "cache_fornecedores()"),
])

# pesquisa.py
substituir("pesquisa.py", [
    (QUERY_CLIENTES[0], "cache_clientes()"),
    (QUERY_FORNS[0], "cache_fornecedores()"),
    (QUERY_CATS[0], "cache_categorias()"),
])

# cadastros.py
substituir("cadastros.py", [
    (QUERY_FORNS[0], "cache_fornecedores()"),
    (QUERY_CATS[0], "cache_categorias()"),
])

# relatorios.py
substituir("relatorios.py", [
    (QUERY_FORNS[0], "cache_fornecedores()"),
])

# concorrentes.py
substituir("concorrentes.py", [
    (QUERY_FORNS[0], "cache_fornecedores()"),
    (QUERY_CATS[0], "cache_categorias()"),
])

# contatos.py
substituir("contatos.py", [
    (QUERY_CLIENTES[0], "cache_clientes()"),
    (QUERY_FORNS[0], "cache_fornecedores()"),
])

# mix_analise.py
substituir("mix_analise.py", [
    (QUERY_FORNS[0], "cache_fornecedores()"),
])

# analise_competitiva.py
substituir("analise_competitiva.py", [
    (QUERY_FORNS[0], "cache_fornecedores()"),
])

print(f"\nTotal: {total} queries substituidas por cache")
