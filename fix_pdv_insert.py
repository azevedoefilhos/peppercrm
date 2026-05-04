#!/usr/bin/env python3
import pathlib

src = pathlib.Path("cadastros.py").read_text(encoding="utf-8")
original = src

OLD = '''            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,1)
        """, (cli_id, numero or None, nome_loja.strip(), tipo_pdv,
              cnpj or None, None,
              endereco or None, bairro or None, cidade or None, estado,
              gerente or None, fone_gerente or None,
              encarregado or None, fone_encarregado or None,
              horario or None, setor or None,
              cluster if cluster != "\u2014" else None,
              tamanho_pdv if tamanho_pdv != "\u2014" else None,
              obs or None))'''

NEW = '''            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,1)
        """, (cli_id, numero or None, nome_loja.strip(), tipo_pdv,
              cnpj or None, None,
              endereco or None, bairro or None, cidade or None, estado,
              gerente or None, fone_gerente or None,
              encarregado or None, fone_encarregado or None,
              horario or None, setor or None,
              cluster if cluster != "\u2014" else None,
              tamanho_pdv if tamanho_pdv != "\u2014" else None,
              obs or None,
              status_pdv))'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    print("OK")
else:
    # Tenta com — diferente
    OLD2 = OLD.replace('\u2014', '?')
    if OLD2 in src:
        src = src.replace(OLD2, NEW, 1)
        print("OK fallback")
    else:
        print("NAO ENCONTRADO")

if src != original:
    pathlib.Path("cadastros.py").write_text(src, encoding="utf-8")
    print("Salvo")
