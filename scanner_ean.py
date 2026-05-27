"""
scanner_ean.py -- Scanner EAN usando OpenCV + câmera traseira.
Não depende de libzbar ou zxingcpp.
"""

def scanner_ean(key_suffix=""):
    import streamlit as st

    try:
        import cv2
        import numpy as np
        from PIL import Image
        import io
    except ImportError as e:
        st.error(f"Biblioteca nao disponivel: {e}")
        return None

    # Força câmera traseira via JS
    st.markdown("""
    <script>
    (function() {
        var _orig = navigator.mediaDevices.getUserMedia.bind(navigator.mediaDevices);
        navigator.mediaDevices.getUserMedia = function(c) {
            if (c && c.video) {
                if (typeof c.video === 'object') {
                    c.video.facingMode = { ideal: 'environment' };
                } else {
                    c.video = { facingMode: { ideal: 'environment' } };
                }
            }
            return _orig(c);
        };
    })();
    </script>
    """, unsafe_allow_html=True)

    img_file = st.camera_input(
        "📷 Abrir câmera",
        key=f"cam_ean_{key_suffix}",
        label_visibility="collapsed"
    )

    if img_file is None:
        return None

    try:
        with st.spinner("🔍 Decodificando..."):
            img = Image.open(io.BytesIO(img_file.getvalue()))
            for _, img_proc in _preparar_imagens(img):
                arr = np.array(img_proc)
                detector = cv2.QRCodeDetector()
                # Tenta QR Code
                data, _, _ = detector.detectAndDecode(arr)
                if data:
                    st.success(f"✅ **{data}**")
                    return data
                # Tenta código de barras
                bd = cv2.barcode.BarcodeDetector()
                ok, decoded, _, _ = bd.detectAndDecodeWithType(arr)
                if ok and decoded:
                    ean = decoded[0]
                    if ean:
                        st.success(f"✅ **{ean}**")
                        return ean

        st.warning("❌ Não detectado. Tente: 20-30cm, boa luz, código centralizado.")
        return None
    except Exception as e:
        st.error(f"Erro: {e}")
        return None


def _preparar_imagens(img):
    from PIL import Image, ImageEnhance, ImageFilter
    rgb    = img.convert("RGB")
    w, h   = rgb.size
    grande = rgb.resize((w*2, h*2), Image.LANCZOS)
    cinza  = rgb.convert("L")
    cinza_c = ImageEnhance.Contrast(cinza).enhance(2.5)
    nitido  = ImageEnhance.Contrast(rgb.filter(ImageFilter.SHARPEN)).enhance(2.0)
    mh, mw  = h//4, w//8
    rec     = rgb.crop((mw, mh, w-mw, h-mh))
    rec_g   = rec.resize((rec.width*2, rec.height*2), Image.LANCZOS)
    return [
        ("orig", rgb), ("2x", grande),
        ("cinza", cinza_c.convert("RGB")),
        ("nitido", nitido), ("recorte", rec_g),
    ]
