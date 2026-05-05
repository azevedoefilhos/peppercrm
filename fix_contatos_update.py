#!/usr/bin/env python3
import pathlib

src = pathlib.Path("contatos.py").read_text(encoding="utf-8")
original = src

# Fix: mudar COALESCE(?,data_followup) para evitar que o regex do database.py
# capture 'data_followup' como campo de strftime
OLD = '''        conn.execute("""UPDATE contato_registro SET status=?, tipo_topico=?,
            data_followup=COALESCE(?,data_followup) WHERE contato_id=?""",
            (_nst, _ntp,
             _fup.isoformat() if _fup and hasattr(_fup,'isoformat') else None, cid))'''

NEW = '''        _fup_val = _fup.isoformat() if _fup and hasattr(_fup,'isoformat') else None
        if _fup_val:
            conn.execute("UPDATE contato_registro SET status=?, tipo_topico=?, data_followup=? WHERE contato_id=?",
                (_nst, _ntp, _fup_val, cid))
        else:
            conn.execute("UPDATE contato_registro SET status=?, tipo_topico=? WHERE contato_id=?",
                (_nst, _ntp, cid))'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    print("OK")
    pathlib.Path("contatos.py").write_text(src, encoding="utf-8")
else:
    print("NAO ENCONTRADO")
