#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

# === FIX 1: Modo clássico - adicionar UN/Kg ao lado do preço ===
OLD_CLASSICO = '''            with st.form(f"form_{key_prefix}"):
                col1, col2 = st.columns(2)
                with col1:
                    preco    = st.number_input("? Pre\u00e7o (R$) *", min_value=0.0,
                                               value=float(preco_d or 0),
                                               step=0.01, format="%.2f",
                                               key=f"preco_{key_prefix}")
                    em_oferta = st.checkbox("?? Em oferta", value=bool(oferta_d),
                                            key=f"oferta_{key_prefix}")
                    frentes  = st.number_input("? Frentes de g\u00f4ndola",
                                               min_value=0, value=int(frentes_d or 0),
                                               key=f"frentes_{key_prefix}")'''

NEW_CLASSICO = '''            with st.form(f"form_{key_prefix}"):
                col1, col2 = st.columns(2)
                with col1:
                    _cp, _cu = st.columns([2, 1])
                    preco    = _cp.number_input("\U0001f4b0 Pre\u00e7o (R$) *", min_value=0.0,
                                               value=float(preco_d or 0),
                                               step=0.01, format="%.2f",
                                               key=f"preco_{key_prefix}")
                    unidade_coleta = _cu.selectbox("Unidade", ["UN", "Kg"],
                                               key=f"un_{key_prefix}")
                    em_oferta = st.checkbox("\U0001f3f7\ufe0f Em oferta", value=bool(oferta_d),
                                            key=f"oferta_{key_prefix}")
                    frentes  = st.number_input("\U0001f4ca Frentes de g\u00f4ndola",
                                               min_value=0, value=int(frentes_d or 0),
                                               key=f"frentes_{key_prefix}")
                    peso_coleta = None
                    preco_kg = None
                    if unidade_coleta == "Kg" and preco > 0:
                        peso_coleta = st.number_input("Peso (Kg)",
                            min_value=0.001, value=1.0, step=0.001,
                            format="%.3f", key=f"peso_{key_prefix}")
                        if peso_coleta:
                            preco_kg = round(preco / peso_coleta, 2)
                            st.caption(f"= R$ {preco_kg:.2f}/Kg")'''

if OLD_CLASSICO in src:
    src = src.replace(OLD_CLASSICO, NEW_CLASSICO, 1)
    print("OK Fix 1: modo clássico")
else:
    print("NAO Fix 1")

# Fix save do modo classico - incluir unidade_coleta
OLD_SAVE = '''                    on_save((preco or None, 1 if em_oferta else 0,
                             frentes or None, 1 if ruptura else 0,
                             1 if pe else 0, tpe if pe else None, obs or None))'''
NEW_SAVE = '''                    on_save((preco or None, 1 if em_oferta else 0,
                             frentes or None, 1 if ruptura else 0,
                             1 if pe else 0, tpe if pe else None, obs or None,
                             unidade_coleta if 'unidade_coleta' in dir() else 'UN',
                             peso_coleta if 'peso_coleta' in dir() else None,
                             preco_kg if 'preco_kg' in dir() else None))'''

if OLD_SAVE in src:
    src = src.replace(OLD_SAVE, NEW_SAVE, 1)
    print("OK Fix 2: save classico")
else:
    print("NAO Fix 2")

# Fix _upsert_item para incluir unidade_coleta
OLD_UPSERT = '''def _upsert_item(pq_id, prod_id, pc_id, dados):
    preco, oferta, frentes, ruptura, pe, tpe, obs = dados
    conn = conectar()
    conn.execute("""DELETE FROM pesquisa_preco_item
        WHERE pesquisa_id=? AND produto_id=? AND produto_concorrente_id=?""",
        (pq_id, prod_id, pc_id))
    conn.execute("""INSERT INTO pesquisa_preco_item
        (pesquisa_id, produto_id, produto_concorrente_id,
         preco, em_oferta, frentes, ruptura, ponto_extra, tipo_ponto_extra, observacao)
        VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (pq_id, prod_id, pc_id, preco, oferta, frentes, ruptura, pe, tpe, obs))
    conn.commit(); conn.close()'''

NEW_UPSERT = '''def _upsert_item(pq_id, prod_id, pc_id, dados):
    if len(dados) == 10:
        preco, oferta, frentes, ruptura, pe, tpe, obs, unidade_coleta, peso_coleta, preco_kg = dados
    else:
        preco, oferta, frentes, ruptura, pe, tpe, obs = dados
        unidade_coleta, peso_coleta, preco_kg = 'UN', None, None
    conn = conectar()
    conn.execute("""DELETE FROM pesquisa_preco_item
        WHERE pesquisa_id=? AND produto_id=? AND produto_concorrente_id=?""",
        (pq_id, prod_id, pc_id))
    conn.execute("""INSERT INTO pesquisa_preco_item
        (pesquisa_id, produto_id, produto_concorrente_id,
         preco, em_oferta, frentes, ruptura, ponto_extra, tipo_ponto_extra, observacao,
         unidade_coleta, peso_coleta, preco_kg)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (pq_id, prod_id, pc_id, preco, oferta, frentes, ruptura, pe, tpe, obs,
         unidade_coleta, peso_coleta, preco_kg))
    conn.commit(); conn.close()'''

if OLD_UPSERT in src:
    src = src.replace(OLD_UPSERT, NEW_UPSERT, 1)
    print("OK Fix 3: _upsert_item")
else:
    print("NAO Fix 3")

# === FIX 4: Modo rápido - mover toggle para ficar ao lado do preço ===
# Remove toggle da posição atual e coloca ao lado do preço
OLD_POS = '''        with col1:
            preco = st.number_input(
                "? Pre?o (R$) *",
                min_value=0.0, format="%.2f",
                value=_v_preco,
                step=0.01, key=f"{k}_preco")'''

NEW_POS = '''        with col1:
            _cp2, _cu2 = st.columns([2, 1])
            preco = _cp2.number_input(
                "\U0001f4b0 Pre\u00e7o (R$) *",
                min_value=0.0, format="%.2f",
                value=_v_preco,
                step=0.01, key=f"{k}_preco")
            unidade_coleta = _cu2.selectbox("Unidade", ["UN", "Kg"], key=f"{k}_un")'''

# Remove o bloco antigo do toggle (que estava depois dos checkboxes)
OLD_TOGGLE_ANTIGO = '''        # Coleta por Kg
        _col_un, _col_peso, _col_pkg = st.columns([1, 1.5, 1.5])
        unidade_coleta = _col_un.selectbox("Unidade", ["UN", "Kg"], key=f"{k}_un")
        peso_coleta = None
        preco_kg = None
        if unidade_coleta == "Kg":
            peso_coleta = _col_peso.number_input("Peso (Kg)",
                min_value=0.001, value=1.0, step=0.001,
                format="%.3f", key=f"{k}_peso")
            if peso_coleta and preco > 0:
                preco_kg = round(preco / peso_coleta, 2)
                _col_pkg.metric("Preco/Kg", f"R$ {preco_kg:.2f}")'''

NEW_TOGGLE_NOVO = '''        # Coleta por Kg - peso aparece abaixo quando Kg selecionado
        peso_coleta = None
        preco_kg = None
        if unidade_coleta == "Kg":
            _cp3, _cu3 = st.columns([2, 1])
            peso_coleta = _cp3.number_input("Peso (Kg)",
                min_value=0.001, value=1.0, step=0.001,
                format="%.3f", key=f"{k}_peso")
            if peso_coleta and preco > 0:
                preco_kg = round(preco / peso_coleta, 2)
                _cu3.metric("R$/Kg", f"{preco_kg:.2f}")'''

# Aplica fixes no modo rápido (segunda instância)
count = 0
for old, new in [(OLD_POS, NEW_POS), (OLD_TOGGLE_ANTIGO, NEW_TOGGLE_NOVO)]:
    occurrences = src.count(old)
    if occurrences >= 2:
        # Substitui apenas a segunda ocorrência
        idx = src.find(old)
        idx2 = src.find(old, idx+1)
        src = src[:idx2] + new + src[idx2+len(old):]
        count += 1
        print(f"OK Fix {4+count}: modo rapido segunda instancia")
    elif occurrences == 1:
        src = src.replace(old, new, 1)
        count += 1
        print(f"OK Fix {4+count}: modo rapido unica instancia")
    else:
        print(f"NAO Fix {4+count}")

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("Salvo!")
