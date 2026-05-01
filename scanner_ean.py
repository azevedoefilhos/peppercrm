"""
scanner_ean.py -- Scanner de código de barras via câmera
Usa st.camera_input + pyzbar para decodificação.
"""

def scanner_ean(key_suffix=""):
    """
    Abre câmera e decodifica código de barras.
    Retorna EAN como string ou None.
    """
    import streamlit as st

    try:
        from pyzbar.pyzbar import decode as pyzbar_decode
        from PIL import Image
        import io
    except ImportError:
        st.error("⚠️ pyzbar não instalado.")
        return None

    img_file = st.camera_input(
        "📷 Tire foto do código de barras",
        key=f"cam_ean_{key_suffix}"
    )

    if img_file is None:
        return None

    try:
        img = Image.open(io.BytesIO(img_file.getvalue()))
        codigos = pyzbar_decode(img)

        if not codigos:
            st.warning("❌ Código não detectado. Tente novamente com boa iluminação e centralizado.")
            return None

        ean = codigos[0].data.decode("utf-8")
        tipo = codigos[0].type
        st.success(f"✅ **{ean}** ({tipo})")
        return ean

    except Exception as e:
        st.error(f"Erro: {e}")
        return None
