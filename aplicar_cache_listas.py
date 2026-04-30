#!/usr/bin/env python3
"""
Aplica cache nas queries de listas de selecao mais frequentes.
Substitui queries diretas por versoes cacheadas nos modulos principais.
"""
import pathlib, re

def cachear_arquivo(caminho, substituicoes):
    src = pathlib.Path(caminho).read_text(encoding="utf-8")
    original = src
    count = 0
    for old, new in substituicoes:
        if old in src:
            src = src.replace(old, new, 1)
            count += 1
    if src != original:
        pathlib.Path(caminho).write_text(src, encoding="utf-8")
        print(f"✅ {caminho}: {count} substituicao(oes)")
    else:
        print(f"  {caminho}: sem alteracoes")
    return count

# ── crm_app.py: cachear lista de clientes no dashboard ──────────────────────
cachear_arquivo("crm_app.py", [
    (
        'clientes_ativos = query("SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo=1 ORDER BY nome_fantasia")',
        'clientes_ativos = _cache_clientes() if "_cache_clientes" in dir() else query("SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo=1 ORDER BY nome_fantasia")'
    ),
])

# ── Adiciona import das funcoes de cache nos modulos principais ──────────────
for arq in ["pesquisa.py", "cadastros.py", "relatorios.py", "concorrentes.py",
            "contatos.py", "pedido.py", "ver_pedidos.py"]:
    src = pathlib.Path(arq).read_text(encoding="utf-8")
    if "_cache_clientes" not in src and "from database import" in src:
        # Adiciona as funcoes de cache ao import existente
        src2 = re.sub(
            r'from database import ([^\n]+)',
            lambda m: f'from database import {m.group(1)}, _cache_clientes, _cache_fornecedores, _cache_categorias'
            if '_cache_clientes' not in m.group(1) else m.group(0),
            src, count=1
        )
        if src2 != src:
            pathlib.Path(arq).write_text(src2, encoding="utf-8")
            print(f"✅ {arq}: import de cache adicionado")

print("\nDone. Agora as funcoes _cache_* estao disponiveis nos modulos.")
print("O cache sera aplicado gradualmente conforme usarmos as funcoes nos proximos commits.")
