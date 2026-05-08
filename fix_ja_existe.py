import pathlib, sys

lines = pathlib.Path("pesquisa.py").read_text(encoding="utf-8").splitlines()

OLD = """    # Verifica se produto ja foi pesquisado hoje nesta pesquisa
    _confirmar_key = f"{k}_confirmar_update"
    _ja_existe = query(\"\"\"
        SELECT ppi.pesquisa_item_id, ppi.preco
        FROM pesquisa_preco_item ppi
        WHERE ppi.pesquisa_id=?
          AND (
              (? IS NOT NULL AND ppi.produto_concorrente_id=?)
              OR
              (? IS NOT NULL AND ppi.produto_id=? AND ppi.produto_concorrente_id IS NULL)
          )
        LIMIT 1
    \"\"\", (pq_id, pc_id, pc_id, produto_id, produto_id))"""

NEW = """    # Verifica se produto ja foi pesquisado hoje nesta pesquisa
    _confirmar_key = f"{k}_confirmar_update"
    if pc_id:
        _ja_existe = query(
            "SELECT pesquisa_item_id, preco FROM pesquisa_preco_item WHERE pesquisa_id=? AND produto_concorrente_id=? LIMIT 1",
            (pq_id, pc_id))
    elif produto_id:
        _ja_existe = query(
            "SELECT pesquisa_item_id, preco FROM pesquisa_preco_item WHERE pesquisa_id=? AND produto_id=? AND produto_concorrente_id IS NULL LIMIT 1",
            (pq_id, produto_id))
    else:
        _ja_existe = []"""

src = "\n".join(lines)
count = src.count(OLD)
print(f"Ocorrencias: {count}")
if count > 0:
    src = src.replace(OLD, NEW)
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("OK")
else:
    # Tenta por numero de linha
    print("Substituindo por linha...")
    for i, l in enumerate(lines):
        if '_ja_existe = query' in l and 'IS NOT NULL' in lines[i+2] if i+2 < len(lines) else False:
            print(f"Encontrado na linha {i+1}")
            break
