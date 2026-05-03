"""
scanner_ean.py -- Scanner EAN com camera traseira forcada via JS injection.
Injeta JS no contexto principal do Streamlit para interceptar getUserMedia
e forcar facingMode: environment antes do camera_input abrir a camera.
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

    # Injeta JS que sobrescreve getUserMedia ANTES do camera_input
    # para forcar sempre camera traseira
    st.markdown(f"""
    <script>
    (function() {{
        // Sobrescreve getUserMedia para forcar camera traseira
        var _origGetUserMedia = navigator.mediaDevices.getUserMedia.bind(navigator.mediaDevices);
        navigator.mediaDevices.getUserMedia = function(constraints) {{
            if (constraints && constraints.video) {{
                if (typeof constraints.video === 'object') {{
                    constraints.video.facingMode = {{ ideal: 'environment' }};
                }} else {{
                    constraints.video = {{ facingMode: {{ ideal: 'environment' }} }};
                }}
            }}
            return _origGetUserMedia(constraints);
        }};

        // Aplica tambem em iframes filhos
        var observer = new MutationObserver(function(mutations) {{
            document.querySelectorAll('iframe').forEach(function(iframe) {{
                try {{
                    var iWin = iframe.contentWindow;
                    if (iWin && iWin.navigator && iWin.navigator.mediaDevices) {{
                        var orig = iWin.navigator.mediaDevices.getUserMedia.bind(iWin.navigator.mediaDevices);
                        iWin.navigator.mediaDevices.getUserMedia = function(c) {{
                            if (c && c.video && typeof c.video === 'object') {{
                                c.video.facingMode = {{ ideal: 'environment' }};
                            }}
                            return orig(c);
                        }};
                    }}
                }} catch(e) {{}}
            }});
        }});
        observer.observe(document.body, {{ childList: true, subtree: true }});
    }})();
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
