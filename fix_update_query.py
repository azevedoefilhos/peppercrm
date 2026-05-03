#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

# Fix 1: where_ex deve priorizar pc_id_ref quando disponivel
OLD1 = '            where_ex  = "pesquisa_id=? AND " +                         ("produto_id=?" if pid_ref else "produto_concorrente_id=?")\n            val_ex    = (pq_id, pid_ref if pid_ref else pc_id_ref)'

NEW1 = '            # Busca por pc_id_ref primeiro (mais especifico), depois produto_id\n            if pc_id_ref:\n                where_ex = "pesquisa_id=? AND produto_concorrente_id=?"\n                val_ex   = (pq_id, pc_id_ref)\n            else:\n                where_ex = "pesquisa_id=? AND produto_id=? AND produto_concorrente_id IS NULL"\n                val_ex   = (pq_id, pid_ref)'

if OLD1 in src:
    src = src.replace(OLD1, NEW1, 1)
    print("✅ Fix 1: where_ex corrigido")
else:
    print("⚠️  Fix 1 não encontrado")

# Fix 2: UPDATE malformado - WHERE deve estar fora das aspas triplas
OLD2 = '''            if existente:
                conn.execute("""UPDATE pesquisa_preco_item SET
                    preco=?, frentes=?, em_oferta=?, ponto_extra=?,
                    ruptura=?, observacao=?
                    WHERE pesquisa_item_id=?""",
                    (preco if not ruptura else None,
                     frentes, 1 if oferta else 0,
                     1 if ponto_extra else 0,
                     1 if ruptura else 0,
                     obs.strip() or None,
                     existente[0]))'''

NEW2 = '''            if existente:
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
                     existente[0]))'''

if OLD2 in src:
    src = src.replace(OLD2, NEW2, 1)
    print("✅ Fix 2: UPDATE reformatado")
else:
    print("⚠️  Fix 2 não encontrado")

# Fix 3: limpar nav_produto_pendente apos salvar
OLD3 = '            st.session_state.pop(f"ean_input_{pq_id}", None)\n            st.session_state.pop(f"ean_buscar_off_{pq_id}", None)\n            st.session_state[f"ean_ultimo_{pq_id}"] = label\n            st.success(f"\u2705 **{label}** \u2014 salvo! Digite o pr\u00f3ximo EAN.")\n            st.rerun()'

NEW3 = '            st.session_state.pop(f"ean_input_{pq_id}", None)\n            st.session_state.pop(f"ean_buscar_off_{pq_id}", None)\n            st.session_state.pop(f"nav_produto_pendente_{pq_id}", None)\n            st.session_state.pop(f"campo_busca_{pq_id}", None)\n            st.session_state.pop(f"{k}_confirmar_update", None)\n            st.session_state[f"ean_ultimo_{pq_id}"] = label\n            st.success(f"\u2705 **{label}** \u2014 salvo!")\n            st.rerun()'

if OLD3 in src:
    src = src.replace(OLD3, NEW3, 1)
    print("✅ Fix 3: limpar estados apos salvar")
else:
    # Tenta variacao
    idx = src.find('st.session_state.pop(f"ean_input_{pq_id}", None)\n            st.session_state.pop(f"ean_buscar_off_')
    if idx >= 0:
        print("ℹ️  Fix 3: padrão parcialmente encontrado, verificar manualmente")
    else:
        print("⚠️  Fix 3 não encontrado")

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("Salvo")
