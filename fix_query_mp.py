import pathlib

lines = pathlib.Path("pesquisa.py").read_text(encoding="utf-8").splitlines()

# Substitui linhas 1148-1155 com query simples
novo = [
    '',
    '    # Mapa de itens ja pesquisados nesta pesquisa',
    '    _pesq = query("SELECT produto_id, produto_concorrente_id, preco, em_oferta, ponto_extra, ruptura FROM pesquisa_preco_item WHERE pesquisa_id=?", (pq_id,))',
    '    _mp = {}',
    '    for _r in _pesq:',
    '        if _r[0]: _mp[("n", int(_r[0]))] = (_r[2], _r[3], _r[4], _r[5])',
    '        if _r[1]: _mp[("c", int(_r[1]))] = (_r[2], _r[3], _r[4], _r[5])',
]

# Substitui linhas 1147-1155 (indices 1146-1155)
new_lines = lines[:1146] + novo + lines[1156:]
pathlib.Path("pesquisa.py").write_text('\n'.join(new_lines), encoding="utf-8")
print(f"OK")
