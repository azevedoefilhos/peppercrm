#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

# Substitui todo o bloco do ja_existe + form
OLD = '''    if _ja_existe and not st.session_state.get(_confirmar_key):
        _preco_ant = _ja_existe[0][1]
        _preco_fmt = f"R$ {_preco_ant:,.2f}".replace(",","X").replace(".",",").replace("X",".")  if _preco_ant else "Ruptura"
        st.warning(f"\u26a0\ufe0f **{label}** j\u00e1 foi pesquisado nesta visita (pre\u00e7o: {_preco_fmt}). Deseja atualizar?")
        col_s, col_n = st.columns(2)
        if col_s.button("\u2705 Sim, atualizar", key=f"{k}_sim", use_container_width=True):
            st.session_state[_confirmar_key] = True
            st.rerun()
        if col_n.button("\u274c N\u00e3o, pr\u00f3ximo", key=f"{k}_nao", use_container_width=True):
            st.session_state.pop(f"ean_input_{pq_id}", None)
            st.session_state.pop(f"campo_busca_{pq_id}", None)
            st.rerun()


    with st.form(key=f"{k}_form", border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            preco = st.number_input(
                "\U0001f4b0 Pre\u00e7o (R$) *",
                min_value=0.0, format="%.2f",
                step=0.01, key=f"{k}_preco")
        with col2:
            frentes = st.number_input(
                "Frentes", min_value=0,
                value=1, step=1, key=f"{k}_frt")'''

NEW = '''    # Busca dados ja coletados para pre-preencher o form
    _dados_anteriores = None
    if _ja_existe:
        _item_id = _ja_existe[0][0]
        _dados_ant = query("""
            SELECT preco, frentes, em_oferta, ponto_extra, ruptura, observacao
            FROM pesquisa_preco_item WHERE pesquisa_item_id=?
        """, (_item_id,))
        if _dados_ant:
            _dados_anteriores = _dados_ant[0]

    if _ja_existe:
        _preco_ant = _ja_existe[0][1]
        _preco_fmt = f"R$ {_preco_ant:,.2f}".replace(",","X").replace(".",",").replace("X",".") if _preco_ant else "Ruptura"
        st.markdown(f"### \u26a0\ufe0f Produto j\u00e1 pesquisado")
        st.warning(f"**{label}** j\u00e1 foi coletado nesta visita — pre\u00e7o anterior: **{_preco_fmt}**. Atualize abaixo ou pule.")
        if st.button("\u274c N\u00e3o atualizar — pr\u00f3ximo produto",
                     key=f"{k}_nao", use_container_width=True):
            st.session_state.pop(f"ean_input_{pq_id}", None)
            st.session_state.pop(f"campo_busca_{pq_id}", None)
            st.session_state.pop(f"nav_produto_pendente_{pq_id}", None)
            st.rerun()

    # Valores anteriores para pre-preencher
    _v_preco   = float(_dados_anteriores[0]) if _dados_anteriores and _dados_anteriores[0] else 0.0
    _v_frentes = int(_dados_anteriores[1])   if _dados_anteriores and _dados_anteriores[1] else 1
    _v_oferta  = bool(_dados_anteriores[2])  if _dados_anteriores else False
    _v_pe      = bool(_dados_anteriores[3])  if _dados_anteriores else False
    _v_ruptura = bool(_dados_anteriores[4])  if _dados_anteriores else False
    _v_obs     = _dados_anteriores[5]        if _dados_anteriores and _dados_anteriores[5] else ""

    with st.form(key=f"{k}_form", border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            preco = st.number_input(
                "\U0001f4b0 Pre\u00e7o (R$) *",
                min_value=0.0, format="%.2f",
                value=_v_preco,
                step=0.01, key=f"{k}_preco")
        with col2:
            frentes = st.number_input(
                "Frentes", min_value=0,
                value=_v_frentes, step=1, key=f"{k}_frt")'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    print("✅ Fix form redesign aplicado")
else:
    print("⚠️  Padrão não encontrado")

# Pre-preencher oferta, ponto_extra, ruptura e obs
OLD2 = '''        oferta    = col_of.checkbox("Oferta", key=f"{k}_of")
            ponto_extra = col_pe.checkbox("P.Extra", key=f"{k}_pe")

        ruptura = st.checkbox("\u26a0\ufe0f Ruptura (sem estoque)", key=f"{k}_rup")'''

NEW2 = '''        oferta    = col_of.checkbox("Oferta", value=_v_oferta, key=f"{k}_of")
            ponto_extra = col_pe.checkbox("P.Extra", value=_v_pe, key=f"{k}_pe")

        ruptura = st.checkbox("\u26a0\ufe0f Ruptura (sem estoque)", value=_v_ruptura, key=f"{k}_rup")'''

if OLD2 in src:
    src = src.replace(OLD2, NEW2, 1)
    print("✅ Fix checkboxes pre-preenchidos")
else:
    print("⚠️  Checkboxes não encontrados")

# Pre-preencher obs
OLD3 = '        obs = st.text_input("Observa\u00e7\u00e3o (opcional)", key=f"{k}_obs",\n                            placeholder="Ex: produto em destaque no fim do corredor")'
NEW3 = '        obs = st.text_input("Observa\u00e7\u00e3o (opcional)", value=_v_obs, key=f"{k}_obs",\n                            placeholder="Ex: produto em destaque no fim do corredor")'

if OLD3 in src:
    src = src.replace(OLD3, NEW3, 1)
    print("✅ Fix obs pre-preenchida")
else:
    print("⚠️  Obs não encontrada")

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("Salvo")
