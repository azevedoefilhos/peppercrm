"""
scanner_ean.py -- Scanner EAN
Usa st.camera_input com atributo environment injetado via JS.
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
        _ok = False
        st.error("Biblioteca de leitura nao disponivel.")
        return None

    # Injeta JS para trocar camera para traseira apos renderizacao
    st.components.v1.html("""
    <script>
    function fixCamera() {
        var videos = window.parent.document.querySelectorAll('video');
        videos.forEach(function(v) {
            if (v.srcObject) {
                v.srcObject.getTracks().forEach(function(t) { t.stop(); });
            }
        });
        var inputs = window.parent.document.querySelectorAll('input[type=file]');
        inputs.forEach(function(inp) {
            inp.setAttribute('capture', 'environment');
        });
        navigator.mediaDevices.getUserMedia({
            video: { facingMode: { exact: 'environment' } }
        }).then(function(stream) {
            var vids = window.parent.document.querySelectorAll('video');
            vids.forEach(function(v) { v.srcObject = stream; });
        }).catch(function(e) { console.log('cam error:', e); });
    }
    setTimeout(fixCamera, 500);
    setTimeout(fixCamera, 1500);
    </script>
    """, height=0)

    img_file = st.camera_input(
        "📷 Código de barras",
        key=f"cam_ean_{key_suffix}",
        label_visibility="collapsed"
    )

    if img_file is None:
        st.caption("👆 Clique acima para fotografar o código de barras")
        return None

    try:
        img = Image.open(io.BytesIO(img_file.getvalue()))
        tentativas = _preparar_imagens(img)

        for nome, img_proc in tentativas:
            try:
                arr = np.array(img_proc)
                res = zxingcpp.read_barcodes(arr)
                if res:
                    ean = res[0].text
                    fmt = str(res[0].format)
                    st.success(f"✅ **{ean}** ({fmt})")
                    return ean
            except Exception:
                continue

        st.warning("❌ Não detectado. Tente: 20-30cm de distância, boa luz, código centralizado.")
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
    recorte = rgb.crop((mw, mh, w-mw, h-mh))
    rec_g = recorte.resize((recorte.width*2, recorte.height*2), Image.LANCZOS)
    return [
        ("original", rgb), ("2x", grande),
        ("cinza_c", cinza_c.convert("RGB")), ("2x_cinza_gc", cinza_gc.convert("RGB")),
        ("bw", bw), ("bw_2x", bw_g), ("nitido", nitido), ("recorte_2x", rec_g),
    ]
