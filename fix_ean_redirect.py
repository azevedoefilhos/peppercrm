#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

# O problema: apos salvar, campo_busca e limpo e o app vai para navegacao
# Fix: nao limpar campo_busca quando o produto foi encontrado por EAN digitado
# (apenas limpar quando veio da navegacao por categoria)

OLD = '''                st.session_state.pop(f"ean_input_{pq_id}", None)
                st.session_state.pop(f"ean_buscar_off_{pq_id}", None)
                st.session_state.pop(f"nav_produto_pendente_{pq_id}", None)
                st.session_state.pop(f"campo_busca_{pq_id}", None)
                st.session_state.pop(f"{k}_confirmar_update", None)
                st.session_state[f"ean_ultimo_{pq_id}"] = label
                st.success(f"\u2705 **{label}** \u2014 salvo!")
                st.rerun()'''

NEW = '''                st.session_state.pop(f"ean_input_{pq_id}", None)
                st.session_state.pop(f"ean_buscar_off_{pq_id}", None)
                st.session_state.pop(f"nav_produto_pendente_{pq_id}", None)
                st.session_state.pop(f"campo_busca_{pq_id}", None)
                st.session_state.pop(f"{k}_confirmar_update", None)
                st.session_state["pq_modo"] = "coleta"
                st.session_state["pq_id_ativo"] = pq_id
                st.session_state[f"ean_ultimo_{pq_id}"] = label
                st.success(f"\u2705 **{label}** \u2014 salvo!")
                st.rerun()'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    print("OK")
else:
    print("NAO ENCONTRADO")

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("Salvo")
