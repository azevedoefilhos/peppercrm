#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

# Fix 1: Reverter pq_modo que causa loop
OLD1 = '''                st.session_state.pop(f"campo_busca_{pq_id}", None)
                st.session_state.pop(f"{k}_confirmar_update", None)
                st.session_state["pq_modo"] = "coleta"
                st.session_state["pq_id_ativo"] = pq_id
                st.session_state[f"ean_ultimo_{pq_id}"] = label'''

NEW1 = '''                st.session_state.pop(f"campo_busca_{pq_id}", None)
                st.session_state.pop(f"{k}_confirmar_update", None)
                st.session_state[f"ean_ultimo_{pq_id}"] = label'''

if OLD1 in src:
    src = src.replace(OLD1, NEW1, 1)
    print("✅ Fix 1: pq_modo removido")
else:
    print("⚠️  Fix 1 nao encontrado")

# Fix 2: Descricao duplicada - remover peso e unidade
OLD2 = '        st.info(f"Concorrente encontrado: {_m3} \u2014 {_d3} {_p3}{_u3} | {aud_label}")'
NEW2 = '        st.info(f"Concorrente encontrado: {_m3} \u2014 {_d3} | {aud_label}")'

if OLD2 in src:
    src = src.replace(OLD2, NEW2, 1)
    print("✅ Fix 2: descricao duplicada corrigida")
else:
    print("⚠️  Fix 2 nao encontrado")

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("Salvo")
