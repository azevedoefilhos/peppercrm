#!/usr/bin/env python3
import pathlib

CAMINHO = pathlib.Path("pesquisa.py")
src = CAMINHO.read_text(encoding="utf-8")
original = src

# 1. Adiciona import do scanner no topo
if "from scanner_ean import" not in src:
    src = src.replace(
        "import streamlit as st\n",
        "import streamlit as st\nfrom scanner_ean import scanner_ean\n",
        1
    )
    print("✅ Import scanner adicionado")

# 2. Substitui o bloco do campo EAN
ANTIGO = """    # ── Campo EAN ────────────────────────────────────────────────────────
    col_ean, col_btn = st.columns([4,1])
    with col_ean:
        ean_input = st.text_input(
            "EAN-13",
            placeholder="7891234567890",
            key=f"ean_input_{pq_id}",
            label_visibility="collapsed",
            max_chars=14
        )
    with col_btn:
        buscar = st.button("🔍", key=f"ean_buscar_{pq_id}",
                           use_container_width=True,
                           help="Buscar produto")"""

NOVO = """    # ── Campo EAN + Scanner de câmera ──────────────────────────────────
    # Se scanner retornou EAN, injeta no campo de texto
    _scan_key = f"scan_ean_{pq_id}"
    if _scan_key in st.session_state and st.session_state[_scan_key]:
        st.session_state[f"ean_input_{pq_id}"] = st.session_state.pop(_scan_key)

    # Linha com campo EAN + botão buscar + botão câmera
    col_ean, col_btn, col_cam = st.columns([3, 1, 1])
    with col_ean:
        ean_input = st.text_input(
            "EAN-13",
            placeholder="7891234567890 ou use 📷",
            key=f"ean_input_{pq_id}",
            label_visibility="collapsed",
            max_chars=14
        )
    with col_btn:
        buscar = st.button("🔍", key=f"ean_buscar_{pq_id}",
                           use_container_width=True,
                           help="Buscar produto")
    with col_cam:
        _cam_aberta = st.session_state.get(f"cam_{pq_id}", False)
        if st.button("📷" if not _cam_aberta else "✖️",
                     key=f"btn_cam_{pq_id}",
                     use_container_width=True,
                     help="Abrir câmera para ler código de barras"):
            st.session_state[f"cam_{pq_id}"] = not _cam_aberta
            st.rerun()

    # Scanner de câmera (abre/fecha)
    if st.session_state.get(f"cam_{pq_id}", False):
        st.info("📷 Aponte a câmera para o código de barras")
        ean_cam = scanner_ean(altura=340)
        if ean_cam:
            st.session_state[_scan_key] = str(ean_cam)
            st.session_state[f"cam_{pq_id}"] = False
            st.rerun()"""

if ANTIGO in src:
    src = src.replace(ANTIGO, NOVO, 1)
    print("✅ Scanner integrado no campo EAN")
else:
    print("⚠️  Padrão não encontrado")

if src != original:
    CAMINHO.write_text(src, encoding="utf-8")
    print("Arquivo salvo")
