"""
scanner_ean.py -- Scanner EAN com camera traseira.
Interface simples: botao abrir camera -> video ao vivo -> botao fotografar -> analise.
"""

def scanner_ean(key_suffix=""):
    import streamlit as st
    import streamlit.components.v1 as components

    try:
        import zxingcpp
        from PIL import Image, ImageEnhance, ImageFilter
        import io, base64
        import numpy as np
        _ok = True
    except ImportError:
        st.error("Biblioteca nao disponivel.")
        return None

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ font-family:sans-serif; padding:6px; background:transparent; }}
button {{
    width:100%; padding:13px; border:none; border-radius:8px;
    font-size:15px; font-weight:bold; cursor:pointer; color:white;
}}
#btnAbrir {{ background:#FF4B4B; }}
#btnFoto  {{ background:#00aa44; margin-top:6px; display:none; }}
#btnNova  {{ background:#888; margin-top:6px; display:none; }}
video {{ width:100%; border-radius:8px; display:none; margin-top:6px; max-height:220px; object-fit:cover; }}
#msg {{ text-align:center; font-size:13px; color:#444; margin-top:4px; min-height:18px; }}
canvas {{ display:none; }}
</style>
</head>
<body>
<button id="btnAbrir" onclick="abrirCamera()">📷 Abrir câmera traseira</button>
<video id="vid" autoplay playsinline muted></video>
<button id="btnFoto" onclick="fotografar()">📸 Fotografar código</button>
<button id="btnNova" onclick="novafoto()">🔄 Nova foto</button>
<canvas id="cv"></canvas>
<div id="msg"></div>

<script>
var stream = null;

function abrirCamera() {{
    document.getElementById('msg').textContent = 'Abrindo câmera...';
    navigator.mediaDevices.getUserMedia({{
        video: {{
            facingMode: {{ ideal: 'environment' }},
            width: {{ ideal: 1280 }},
            height: {{ ideal: 720 }}
        }}
    }}).then(function(s) {{
        stream = s;
        var vid = document.getElementById('vid');
        vid.srcObject = s;
        vid.style.display = 'block';
        document.getElementById('btnAbrir').style.display = 'none';
        document.getElementById('btnFoto').style.display = 'block';
        document.getElementById('msg').textContent = 'Centralize o código e fotografe';
    }}).catch(function(e) {{
        document.getElementById('msg').textContent = '❌ ' + e.message;
    }});
}}

function fotografar() {{
    var vid = document.getElementById('vid');
    var cv  = document.getElementById('cv');
    cv.width  = vid.videoWidth  || 1280;
    cv.height = vid.videoHeight || 720;
    cv.getContext('2d').drawImage(vid, 0, 0);
    if (stream) stream.getTracks().forEach(t => t.stop());
    vid.style.display = 'none';
    document.getElementById('btnFoto').style.display = 'none';
    document.getElementById('btnNova').style.display = 'block';
    document.getElementById('msg').textContent = '⏳ Analisando...';
    var data = cv.toDataURL('image/jpeg', 0.92);
    window.parent.postMessage({{
        isStreamlitMessage: true,
        type: 'streamlit:setComponentValue',
        value: data
    }}, '*');
}}

function novafoto() {{
    document.getElementById('btnNova').style.display = 'none';
    document.getElementById('btnAbrir').style.display = 'block';
    document.getElementById('msg').textContent = '';
    window.parent.postMessage({{
        isStreamlitMessage: true,
        type: 'streamlit:setComponentValue',
        value: null
    }}, '*');
}}
</script>
</body>
</html>"""

    result = components.html(html, height=340, scrolling=False)

    if result and isinstance(result, str) and result.startswith('data:image'):
        try:
            _, b64 = result.split(',', 1)
            img = Image.open(io.BytesIO(base64.b64decode(b64)))

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

            st.warning("❌ Não detectado. Tente: 20-30cm de distância, boa luz.")
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
