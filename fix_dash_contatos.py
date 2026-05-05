#!/usr/bin/env python3
import pathlib

src = pathlib.Path("crm_app.py").read_text(encoding="utf-8")
original = src

# Fix: contatos este mes = criados no mes OU com interacao no mes
OLD = '''            "qtd_contatos_mes": q1("SELECT COUNT(*) FROM contato_registro WHERE ativo=1 AND data_contato >= date(\\'now\\',\\'start of month\\')")'''

NEW = '''            "qtd_contatos_mes": q1("SELECT COUNT(*) FROM contato_registro cr WHERE ativo=1 AND (cr.data_contato >= date(\\'now\\',\\'start of month\\') OR EXISTS (SELECT 1 FROM contato_interacao ci WHERE ci.contato_id=cr.contato_id AND ci.ativo=1 AND ci.data_interacao >= date(\\'now\\',\\'start of month\\')))")'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    pathlib.Path("crm_app.py").write_text(src, encoding="utf-8")
    print("OK")
else:
    # Tenta sem escape
    idx = src.find('"qtd_contatos_mes": q1("SELECT COUNT(*) FROM contato_registro WHERE ativo=1 AND data_contato >= date(')
    if idx >= 0:
        line_end = src.find(')")', idx) + 3
        old_q = src[idx:line_end]
        print("Encontrado:")
        print(repr(old_q[:150]))
        new_q = '"qtd_contatos_mes": q1("SELECT COUNT(*) FROM contato_registro cr WHERE ativo=1 AND (cr.data_contato >= date(\'now\',\'start of month\') OR EXISTS (SELECT 1 FROM contato_interacao ci WHERE ci.contato_id=cr.contato_id AND ci.ativo=1 AND ci.data_interacao >= date(\'now\',\'start of month\')))")'
        src = src[:idx] + new_q + src[line_end:]
        pathlib.Path("crm_app.py").write_text(src, encoding="utf-8")
        print("OK via posicao")
    else:
        print("NAO ENCONTRADO")
