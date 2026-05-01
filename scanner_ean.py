"""
scanner_ean.py -- Scanner de código de barras via câmera
Usa st.camera_input + zxing-cpp (puro Python, sem dependencias de sistema).
"""

def scanner_ean(key_suffix=""):
    import streamlit as st

    try:
        import zxingcpp
        from PIL import Image
        import io
        import numpy as np
        _ok = True
    except ImportError:
        _ok = False

    if not _ok:
        st.error("⚠️ Biblioteca de leitura não disponível.")
        return None

    img_file = st.camera_input(
        "📷 Tire foto do código de barras",
        key=f"cam_ean_{key_suffix}"
    )

    if img_file is None:
        return None

    try:
        img = Image.open(io.BytesIO(img_file.getvalue()))
        img_array = np.array(img)
        resultados = zxingcpp.read_barcodes(img_array)

        if not resultados:
            st.warning("❌ Código não detectado. Tente com boa iluminação e código centralizado.")
            return None

        ean = resultados[0].text
        formato = str(resultados[0].format)
        st.success(f"✅ **{ean}** ({formato})")
        return ean

    except Exception as e:
        st.error(f"Erro: {e}")
        return None
