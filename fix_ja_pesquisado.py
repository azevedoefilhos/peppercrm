#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

OLD = '''    k = f"ean_coleta_{pq_id}_{ean}"

    with st.container(border=True):'''

NEW = '''    k = f"ean_coleta_{pq_id}_{ean}"

    # Verifica se produto ja foi pesquisado hoje nesta pesquisa
    _ja_existe = query("""
        SELECT ppi.pesquisa_item_id, ppi.preco
        FROM pesquisa_preco_item ppi
        WHERE ppi.pesquisa_id=?
          AND (
              (? IS NOT NULL AND ppi.produto_concorrente_id=?)
              OR
              (? IS NOT NULL AND ppi.produto_id=? AND ppi.produto_concorrente_id IS NULL)
          )
        LIMIT 1
    """, (pq_id, pc_id, pc_id, produto_id, produto_id))

    if _ja_existe:
        _preco_ant = _ja_existe[0][1]
        _preco_fmt = f"R$ {_preco_ant:,.2f}".replace(",","X").replace(".",",").replace("X",".") if _preco_ant else "Ruptura"
        _confirmar_key = f"{k}_confirmar_update"
        st.warning(f"⚠️ **{label}** já foi pesquisado nesta visita (preço: {_preco_fmt}). Deseja atualizar?")
        col_s, col_n = st.columns(2)
        if col_s.button("✅ Sim, atualizar", key=f"{k}_sim", use_container_width=True):
            st.session_state[_confirmar_key] = True
        if col_n.button("❌ Não, próximo", key=f"{k}_nao", use_container_width=True):
            st.session_state.pop(f"ean_input_{pq_id}", None)
            st.rerun()
        if not st.session_state.get(_confirmar_key):
            return

    with st.container(border=True):'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    print("✅ Verificação de produto já pesquisado adicionada")
else:
    print("⚠️  Padrão não encontrado")

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("Salvo")
