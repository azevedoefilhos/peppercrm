#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

OLD = '''    # Busca itens ja pesquisados para destacar na lista
    _pesq = query("""SELECT produto_id, produto_concorrente_id, preco,
        em_oferta, ponto_extra, ruptura FROM pesquisa_preco_item WHERE pesquisa_id=?
    """, (pq_id,))
    _mp = {}
    for _r in _pesq:
        _p, _c, _pr, _of, _pe, _ru = _r
        if _p: _mp[("n", _p)] = (_pr, _of, _pe, _ru)
        if _c: _mp[("c", _c)] = (_pr, _of, _pe, _ru)'''

NEW = '''    # Busca itens ja pesquisados para destacar na lista
    _pesq = query("""SELECT produto_id, produto_concorrente_id, preco,
        em_oferta, ponto_extra, ruptura FROM pesquisa_preco_item WHERE pesquisa_id=?
    """, (pq_id,))
    _mp = {}
    for _r in _pesq:
        _p  = _r[0]
        _c  = _r[1]
        _pr = _r[2]
        _of = _r[3]
        _pe = _r[4]
        _ru = _r[5]
        if _p: _mp[("n", int(_p))] = (_pr, _of, _pe, _ru)
        if _c: _mp[("c", int(_c))] = (_pr, _of, _pe, _ru)'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("OK")
else:
    print("NAO ENCONTRADO")
