#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

OLD = '''    else:
        aud_label = "Auditavel" if resultado.get("auditavel",1) else "Nao auditavel"
        _m3 = resultado.get("marca","")
        _d3 = resultado.get("descricao","")
        _p3 = resultado.get("peso","")
        _u3 = resultado.get("um","")
        st.info(f"Concorrente encontrado: {_m3} \u2014 {_d3} {_p3}{_u3} | {aud_label}")
        _form_coleta_rapida_ean(pq_id,
                                 tipo="concorrente",
                                 produto_id=None,
                                 pc_id=resultado["pc_id"],
                                 label=resultado["descricao"],
                                 ean=ean)'''

NEW = '''    else:
        aud_label = "Auditavel" if resultado.get("auditavel",1) else "Nao auditavel"
        _m3 = resultado.get("marca","")
        _d3 = resultado.get("descricao","")
        _p3 = resultado.get("peso","")
        _u3 = resultado.get("um","")
        st.info(f"Concorrente encontrado: {_m3} \u2014 {_d3} {_p3}{_u3} | {aud_label}")

        # Busca produto nosso vinculado a este concorrente (para gravar produto_id)
        _pc_id = resultado["pc_id"]
        _rel = query("""SELECT produto_id FROM produto_concorrente_relacao
                        WHERE produto_concorrente_id=?
                        AND produto_id IN (SELECT produto_id FROM produto WHERE fornecedor_id=?)
                        LIMIT 1""", (_pc_id, forn_id))
        _prod_id_vinculado = _rel[0][0] if _rel else None

        if _prod_id_vinculado:
            st.caption(f"\u2705 Vinculado ao nosso produto ID {_prod_id_vinculado}")

        _form_coleta_rapida_ean(pq_id,
                                 tipo="concorrente",
                                 produto_id=_prod_id_vinculado,
                                 pc_id=_pc_id,
                                 label=resultado["descricao"],
                                 ean=ean)'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    print("OK")
else:
    print("NAO ENCONTRADO")
    # Tenta com dash diferente
    OLD2 = OLD.replace('\u2014', '?')
    if OLD2 in src:
        src = src.replace(OLD2, NEW, 1)
        print("OK via fallback")
    else:
        # Mostra o que existe
        idx = src.find('Concorrente encontrado:')
        if idx >= 0:
            print(repr(src[idx-200:idx+300]))

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("Salvo")

# Fix 2: no INSERT, quando tipo=concorrente com produto_id vinculado,
# gravar produto_id E produto_concorrente_id
src2 = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")

OLD2 = '''            # Determina produto_id de referência
            # tipo pode ser: "nosso", "conc" ou "concorrente"
            pid_ref   = produto_id if tipo == "nosso" else None
            pc_id_ref = pc_id if tipo in ("conc", "concorrente") else None'''

NEW2 = '''            # Determina produto_id de referência
            # tipo pode ser: "nosso", "conc" ou "concorrente"
            pid_ref   = produto_id  # produto_id pode vir preenchido mesmo para concorrente
            pc_id_ref = pc_id if tipo in ("conc", "concorrente") else None'''

if OLD2 in src2:
    src2 = src2.replace(OLD2, NEW2, 1)
    pathlib.Path("pesquisa.py").write_text(src2, encoding="utf-8")
    print("Fix 2 OK")
else:
    print("Fix 2 NAO ENCONTRADO")
