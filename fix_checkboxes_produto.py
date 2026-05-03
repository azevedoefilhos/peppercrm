#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

# Fix 1: Mostrar descricao do produto vinculado em vez do ID
OLD1 = '''        if _prod_id_vinculado:
            st.caption(f"✅ Vinculado ao nosso produto ID {_prod_id_vinculado}")'''

NEW1 = '''        if _prod_id_vinculado:
            _desc_vinc = query("""SELECT p.descricao_curta, m.nome_marca, p.unidade_medida, p.peso
                FROM produto p JOIN marca m ON p.marca_id=m.marca_id
                WHERE p.produto_id=? LIMIT 1""", (_prod_id_vinculado,))
            if _desc_vinc:
                _dv = _desc_vinc[0]
                _label_vinc = f"{_dv[1]} — {_dv[0]}" + (f" {_dv[3]}{_dv[2]}" if _dv[3] else "")
            else:
                _label_vinc = f"ID {_prod_id_vinculado}"
            st.caption(f"✅ Vinculado ao nosso produto: **{_label_vinc}**")'''

if OLD1 in src:
    src = src.replace(OLD1, NEW1, 1)
    print("✅ Fix 1: descrição do produto vinculado")
else:
    print("⚠️  Fix 1 não encontrado")

# Fix 2: Checkboxes dentro de st.form nao atualizam corretamente
# Solucao: ler valores do session_state apos submit
OLD2 = '''        oferta    = col_of.checkbox("Oferta", value=_v_oferta, key=f"{k}_of")
            ponto_extra = col_pe.checkbox("P.Extra", value=_v_pe, key=f"{k}_pe")

        ruptura = st.checkbox("⚠️ Ruptura (sem estoque)", value=_v_ruptura, key=f"{k}_rup")'''

NEW2 = '''        oferta    = col_of.checkbox("Oferta", value=_v_oferta, key=f"{k}_of")
            ponto_extra = col_pe.checkbox("P.Extra", value=_v_pe, key=f"{k}_pe")

        ruptura = st.checkbox("⚠️ Ruptura (sem estoque)", value=_v_ruptura, key=f"{k}_rup")

        # Nota: em st.form, os valores dos checkboxes sao lidos do session_state
        # apos submit para garantir valores corretos
        _oferta_val = st.session_state.get(f"{k}_of", oferta)
        _pe_val = st.session_state.get(f"{k}_pe", ponto_extra)
        _rup_val = st.session_state.get(f"{k}_rup", ruptura)'''

if OLD2 in src:
    src = src.replace(OLD2, NEW2, 1)
    print("✅ Fix 2: leitura checkboxes do session_state")
else:
    print("⚠️  Fix 2 não encontrado")

# Fix 3: Usar _oferta_val, _pe_val, _rup_val no save
OLD3 = '''                        (preco if not ruptura else None,
                         frentes, 1 if oferta else 0,
                         1 if ponto_extra else 0,
                         1 if ruptura else 0,
                         obs.strip() or None,
                         existente[0]))
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
                         obs.strip() or None))'''

NEW3 = '''                        (preco if not _rup_val else None,
                         frentes, 1 if _oferta_val else 0,
                         1 if _pe_val else 0,
                         1 if _rup_val else 0,
                         obs.strip() or None,
                         existente[0]))
                else:
                    conn.execute(
                        "INSERT INTO pesquisa_preco_item "
                        "(pesquisa_id, produto_id, produto_concorrente_id, "
                        "preco, frentes, em_oferta, ponto_extra, ruptura, observacao) "
                        "VALUES (?,?,?,?,?,?,?,?,?)",
                        (pq_id, pid_ref, pc_id_ref,
                         preco if not _rup_val else None,
                         frentes, 1 if _oferta_val else 0,
                         1 if _pe_val else 0,
                         1 if _rup_val else 0,
                         obs.strip() or None))'''

if OLD3 in src:
    src = src.replace(OLD3, NEW3, 1)
    print("✅ Fix 3: usar valores do session_state no save")
else:
    print("⚠️  Fix 3 não encontrado")

# Fix 4: validacao de preco tambem usa _rup_val
OLD4 = '            if preco <= 0 and not ruptura:'
NEW4 = '            _oferta_val = st.session_state.get(f"{k}_of", oferta)\n            _pe_val = st.session_state.get(f"{k}_pe", ponto_extra)\n            _rup_val = st.session_state.get(f"{k}_rup", ruptura)\n            if preco <= 0 and not _rup_val:'

if OLD4 in src:
    src = src.replace(OLD4, NEW4, 1)
    print("✅ Fix 4: validação usa _rup_val")
else:
    print("⚠️  Fix 4 não encontrado")

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("Salvo")
