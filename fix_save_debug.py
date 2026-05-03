#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

# Substitui o bloco de save com debug detalhado
OLD = '''        if _salvar:
            if preco <= 0 and not ruptura:
                st.error("Informe o pre\u00e7o ou marque Ruptura.")
                return

            conn = conectar()

            # Determina produto_id de refer\u00eancia
            # tipo pode ser: "nosso", "conc" ou "concorrente"
            pid_ref   = produto_id  # produto_id pode vir preenchido mesmo para concorrente
            pc_id_ref = pc_id if tipo in ("conc", "concorrente") else None

            # Busca por pc_id_ref primeiro (mais especifico), depois produto_id
            if pc_id_ref:
                where_ex = "pesquisa_id=? AND produto_concorrente_id=?"
                val_ex   = (pq_id, pc_id_ref)
            else:
                where_ex = "pesquisa_id=? AND produto_id=? AND produto_concorrente_id IS NULL"
                val_ex   = (pq_id, pid_ref)
            existente = conn.execute(
                f"SELECT pesquisa_item_id FROM pesquisa_preco_item WHERE {where_ex} LIMIT 1",
                val_ex).fetchone()

            if existente:
                conn.execute(
                    "UPDATE pesquisa_preco_item SET "
                    "preco=?, frentes=?, em_oferta=?, ponto_extra=?, "
                    "ruptura=?, observacao=? "
                    "WHERE pesquisa_item_id=?",
                    (preco if not ruptura else None,
                     frentes, 1 if oferta else 0,
                     1 if ponto_extra else 0,
                     1 if ruptura else 0,
                     obs.strip() or None,
                     existente[0]))
            else:
                conn.execute("""INSERT INTO pesquisa_preco_item
                    (pesquisa_id, produto_id, produto_concorrente_id,
                     preco, frentes, em_oferta, ponto_extra, ruptura,
                     observacao)
                    VALUES (?,?,?,?,?,?,?,?,?)""",
                    (pq_id,
                     pid_ref, pc_id_ref,
                     preco if not ruptura else None,
                     frentes, 1 if oferta else 0,
                     1 if ponto_extra else 0,
                     1 if ruptura else 0,
                     obs.strip() or None))'''

NEW = '''        if _salvar:
            if preco <= 0 and not ruptura:
                st.error("Informe o pre\u00e7o ou marque Ruptura.")
                return

            try:
                conn = conectar()

                pid_ref   = produto_id
                pc_id_ref = pc_id if tipo in ("conc", "concorrente") else None

                # Busca item existente
                if pc_id_ref:
                    where_ex = "pesquisa_id=? AND produto_concorrente_id=?"
                    val_ex   = (pq_id, pc_id_ref)
                else:
                    where_ex = "pesquisa_id=? AND produto_id=? AND produto_concorrente_id IS NULL"
                    val_ex   = (pq_id, pid_ref)

                existente = conn.execute(
                    f"SELECT pesquisa_item_id FROM pesquisa_preco_item WHERE {where_ex} LIMIT 1",
                    val_ex).fetchone()

                if existente:
                    conn.execute(
                        "UPDATE pesquisa_preco_item SET "
                        "preco=?, frentes=?, em_oferta=?, ponto_extra=?, "
                        "ruptura=?, observacao=? "
                        "WHERE pesquisa_item_id=?",
                        (preco if not ruptura else None,
                         frentes, 1 if oferta else 0,
                         1 if ponto_extra else 0,
                         1 if ruptura else 0,
                         obs.strip() or None,
                         existente[0]))
                    conn.commit()
                    st.success(f"\u2705 **{label}** atualizado!")
                else:
                    conn.execute(
                        "INSERT INTO pesquisa_preco_item "
                        "(pesquisa_id, produto_id, produto_concorrente_id, "
                        "preco, frentes, em_oferta, ponto_extra, ruptura, observacao) "
                        "VALUES (?,?,?,?,?,?,?,?,?)",
                        (pq_id, pid_ref, pc_id_ref,
                         preco if not ruptura else None,
                         frentes, 1 if oferta else 0,
                         1 if ponto_extra else 0,
                         1 if ruptura else 0,
                         obs.strip() or None))
                    conn.commit()
                    st.success(f"\u2705 **{label}** salvo!")
                conn.close()
            except Exception as _e:
                st.error(f"Erro ao salvar: {_e}")
                return'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    print("OK")
else:
    print("NAO ENCONTRADO")
    # Tenta localizar
    idx = src.find('if _salvar:')
    if idx >= 0:
        print(f"_salvar encontrado na posicao {idx}")

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("Salvo")
