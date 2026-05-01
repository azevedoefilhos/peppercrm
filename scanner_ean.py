"""
scanner_ean.py -- Scanner de código de barras via câmera
Usa st.camera_input do Streamlit + pyzbar para decodificação.
Funciona nativamente no celular sem componentes externos.
"""
import streamlit as st


def scanner_ean(altura=None, key_suffix=""):
    """
    Abre a câmera do celular e decodifica o código de barras.
    Retorna o EAN como string ou None.
    """
    try:
        from pyzbar.pyzbar import decode as pyzbar_decode
        from PIL import Image
        import io
        _pyzbar_ok = True
    except ImportError:
        _pyzbar_ok = False

    if not _pyzbar_ok:
        st.error("⚠️ Biblioteca pyzbar não instalada. Contate o suporte.")
        return None

    st.markdown(
        "📷 **Tire uma foto do código de barras** — centralize o código na imagem",
        help="Segure o celular a 15-20cm do produto. O código deve estar bem iluminado."
    )

    img_file = st.camera_input(
        "Fotografar código de barras",
        key=f"cam_ean_{key_suffix}",
        label_visibility="collapsed"
    )

    if img_file is None:
        st.caption("👆 Clique acima para abrir a câmera")
        return None

    # Decodifica a imagem
    try:
        img = Image.open(io.BytesIO(img_file.getvalue()))
        codigos = pyzbar_decode(img)

        if not codigos:
            st.warning("❌ Nenhum código detectado. Tente novamente com melhor iluminação.")
            return None

        # Pega o primeiro código encontrado
        codigo = codigos[0]
        ean = codigo.data.decode("utf-8")
        tipo = codigo.type

        st.success(f"✅ Código lido: **{ean}** ({tipo})")
        return ean

    except Exception as e:
        st.error(f"Erro ao processar imagem: {e}")
        return None
