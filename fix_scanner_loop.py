#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

OLD = '''    # Scanner sempre visivel no topo — sem botao intermediario
    st.session_state["pq_modo"] = "coleta"
    st.session_state["pq_id_ativo"] = pq_id
    ean_cam = scanner_ean(key_suffix=str(pq_id))
    if ean_cam:
        st.session_state[_scan_key] = str(ean_cam)
        st.rerun()

    st.caption("Ou digite o EAN manualmente abaixo")'''

NEW = '''    # Scanner so aparece quando nao ha EAN digitado/capturado
    st.session_state["pq_modo"] = "coleta"
    st.session_state["pq_id_ativo"] = pq_id

    # Verifica se ja tem EAN no campo (evita loop)
    _ean_atual = st.session_state.get(f"ean_input_{pq_id}", "").strip()
    if not _ean_atual:
        ean_cam = scanner_ean(key_suffix=str(pq_id))
        if ean_cam:
            st.session_state[_scan_key] = str(ean_cam)
            st.rerun()

    st.caption("Ou digite o EAN manualmente abaixo")'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    print("OK")
else:
    print("NAO ENCONTRADO")

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("Salvo")
