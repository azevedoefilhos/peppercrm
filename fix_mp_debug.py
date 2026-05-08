#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

OLD = '''    _mp = {}
    for _r in _pesq:
        _p  = _r[0]
        _c  = _r[1]
        _pr = _r[2]
        _of = _r[3]
        _pe = _r[4]
        _ru = _r[5]
        if _p: _mp[("n", int(_p))] = (_pr, _of, _pe, _ru)
        if _c: _mp[("c", int(_c))] = (_pr, _of, _pe, _ru)'''

NEW = '''    _mp = {}
    for _r in _pesq:
        _p  = _r[0]
        _c  = _r[1]
        _pr = _r[2]
        _of = _r[3]
        _pe = _r[4]
        _ru = _r[5]
        if _p: _mp[("n", int(_p))] = (_pr, _of, _pe, _ru)
        if _c: _mp[("c", int(_c))] = (_pr, _of, _pe, _ru)
    st.caption(f"DEBUG: {len(_pesq)} itens pesquisados, {len(_mp)} no mapa")'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("OK")
else:
    print("NAO ENCONTRADO")
