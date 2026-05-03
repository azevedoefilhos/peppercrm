#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

# Substitui todo o bloco entre _ja_existe e with st.form
lines = src.splitlines()
start = None
end = None

for i, l in enumerate(lines):
    if 'if _ja_existe and not st.session_state.get(_confirmar_key):' in l:
        start = i
    if start and 'with st.form(key=f"{k}_form"' in l:
        end = i
        break

if start and end:
    print(f"Substituindo linhas {start+1} a {end+1}")
    novo_bloco = '''    # Busca dados ja coletados para pre-preencher
    _dados_anteriores = None
    if _ja_existe:
        _item_id = _ja_existe[0][0]
        _r = query("""SELECT preco, frentes, em_oferta, ponto_extra, ruptura, observacao
            FROM pesquisa_preco_item WHERE pesquisa_item_id=?""", (_item_id,))
        if _r: _dados_anteriores = _r[0]

    # Valores para pre-preencher (anteriores ou padrao)
    _v_preco   = float(_dados_anteriores[0]) if _dados_anteriores and _dados_anteriores[0] else 0.0
    _v_frentes = int(_dados_anteriores[1])   if _dados_anteriores and _dados_anteriores[1] else 1
    _v_oferta  = bool(_dados_anteriores[2])  if _dados_anteriores else False
    _v_pe      = bool(_dados_anteriores[3])  if _dados_anteriores else False
    _v_ruptura = bool(_dados_anteriores[4])  if _dados_anteriores else False
    _v_obs     = str(_dados_anteriores[5])   if _dados_anteriores and _dados_anteriores[5] else ""

    if _ja_existe:
        _preco_fmt = f"R$ {_v_preco:,.2f}".replace(",","X").replace(".",",").replace("X",".") if _v_preco else "Ruptura"
        st.markdown(f"### ⚠️ Produto já pesquisado")
        st.warning(f"**{label}** já coletado nesta visita — preço anterior: **{_preco_fmt}**. Atualize abaixo ou pule.")
        if st.button("❌ Não atualizar — próximo produto",
                     key=f"{k}_nao", use_container_width=True):
            st.session_state.pop(f"ean_input_{pq_id}", None)
            st.session_state.pop(f"campo_busca_{pq_id}", None)
            st.session_state.pop(f"nav_produto_pendente_{pq_id}", None)
            st.rerun()

    with st.form(key=f"{k}_form", border=True):'''

    new_lines = lines[:start] + novo_bloco.splitlines() + lines[end+1:]
    src2 = '\n'.join(new_lines)

    # Corrige preco e frentes para usar _v_preco e _v_frentes
    src2 = src2.replace(
        '            preco = st.number_input(\n                "💰 Preço (R$) *",\n                min_value=0.0, format="%.2f",\n                step=0.01, key=f"{k}_preco")',
        '            preco = st.number_input(\n                "💰 Preço (R$) *",\n                min_value=0.0, format="%.2f",\n                value=_v_preco,\n                step=0.01, key=f"{k}_preco")'
    )
    src2 = src2.replace(
        '            frentes = st.number_input(\n                "Frentes", min_value=0,\n                value=1, step=1, key=f"{k}_frt")',
        '            frentes = st.number_input(\n                "Frentes", min_value=0,\n                value=_v_frentes, step=1, key=f"{k}_frt")'
    )
    # obs
    src2 = src2.replace(
        'obs = st.text_input("Observação (opcional)", key=f"{k}_obs",',
        'obs = st.text_input("Observação (opcional)", value=_v_obs, key=f"{k}_obs",'
    )

    pathlib.Path("pesquisa.py").write_text(src2, encoding="utf-8")
    print("✅ Fix aplicado e salvo")
else:
    print(f"⚠️  start={start} end={end}")
