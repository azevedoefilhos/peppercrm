#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

OLD = '''    # Botao câmera no topo
    col_btn_cam, col_info = st.columns([1, 3])
    with col_btn_cam:
        if st.button("📷 Câmera" if not _cam_aberta else "✖️ Fechar",
                     key=f"btn_cam_{pq_id}",
                     use_container_width=True):
            st.session_state[f"cam_{pq_id}"] = not _cam_aberta
            st.rerun()
    with col_info:
        if not _cam_aberta:
            st.caption("Escaneie o código ou digite o EAN abaixo")
        else:
            st.caption("📸 Tire a foto centralizando o código de barras")

    # Scanner — aparece no topo quando ativo
    if _cam_aberta:
        # Preserva estado da pesquisa durante rerun da camera
        st.session_state["pq_modo"] = "coleta"
        st.session_state["pq_id_ativo"] = pq_id
        ean_cam = scanner_ean(key_suffix=str(pq_id))
        if ean_cam:
            st.session_state[_scan_key] = str(ean_cam)
            st.session_state[f"cam_{pq_id}"] = False
            st.rerun()'''

NEW = '''    # Scanner sempre visivel no topo — sem botao intermediario
    st.session_state["pq_modo"] = "coleta"
    st.session_state["pq_id_ativo"] = pq_id
    ean_cam = scanner_ean(key_suffix=str(pq_id))
    if ean_cam:
        st.session_state[_scan_key] = str(ean_cam)
        st.rerun()

    st.caption("Ou digite o EAN manualmente abaixo")'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    print("✅ Botao intermediario removido - scanner direto")
else:
    print("⚠️  Padrão não encontrado")

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("Salvo")

# Verifica resultado
import pathlib
src2 = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
for i, l in enumerate(src2.splitlines(), 1):
    if 'scanner_ean' in l or 'btn_cam' in l or 'cam_aberta' in l:
        print(i, l[:80])
