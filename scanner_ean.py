"""
scanner_ean.py -- Scanner EAN
Usa st.camera_input (confiavel) + CSS para label customizado.
O postMessage do iframe nao funciona com Streamlit - usa camera_input nativo.
"""

def scanner_ean(key_suffix=""):
    import streamlit as st

    try:
        import zxingcpp
        from PIL import Image, ImageEnhance, ImageFilter
        import io
        import numpy as np
        _ok = True
    except ImportError:
        st.error("Biblioteca nao disponivel.")
        return None

    # CSS para customizar o botao da camera
    st.markdown("""
    <style>
    [data-testid="stCameraInputButton"] {
        background-color: #FF4B4B !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        width: 100% !important;
    }
    [data-testid="stCameraInput"] label { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    img_file = st.camera_input(
        "📷 Abrir câmera",
        key=f"cam_ean_{key_suffix}",
        label_visibility="collapsed"
    )

    if img_file is None:
        return None

    try:
        img = Image.open(io.BytesIO(img_file.getvalue()))

        with st.spinner("🔍 Decodificando..."):
            for _, img_proc in _preparar_imagens(img):
                try:
                    res = zxingcpp.read_barcodes(np.array(img_proc))
                    if res:
                        ean = res[0].text
                        st.success(f"✅ **{ean}**")
                        return ean
                except Exception:
                    continue

        st.warning("❌ Não detectado. Tente: 20-30cm, boa luz, código centralizado.")
        return None

    except Exception as e:
        st.error(f"Erro: {e}")
        return None


def _preparar_imagens(img):
    from PIL import Image, ImageEnhance, ImageFilter
    rgb = img.convert("RGB")
    w, h = rgb.size
    grande = rgb.resize((w*2, h*2), Image.LANCZOS)
    cinza = rgb.convert("L")
    cinza_c = ImageEnhance.Contrast(cinza).enhance(2.5)
    cinza_g = grande.convert("L")
    cinza_gc = ImageEnhance.Contrast(cinza_g).enhance(2.5)
    bw = cinza.point(lambda x: 0 if x < 128 else 255, '1').convert("RGB")
    bw_g = cinza_g.point(lambda x: 0 if x < 128 else 255, '1').convert("RGB")
    nitido = ImageEnhance.Contrast(rgb.filter(ImageFilter.SHARPEN)).enhance(2.0)
    mh, mw = h//4, w//8
    rec = rgb.crop((mw, mh, w-mw, h-mh))
    rec_g = rec.resize((rec.width*2, rec.height*2), Image.LANCZOS)
    return [
        ("orig", rgb), ("2x", grande),
        ("cinza", cinza_c.convert("RGB")), ("2x_cinza", cinza_gc.convert("RGB")),
        ("bw", bw), ("bw_2x", bw_g), ("nitido", nitido), ("recorte", rec_g),
    ]
