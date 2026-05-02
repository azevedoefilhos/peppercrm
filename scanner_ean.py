"""
scanner_ean.py -- Scanner EAN com camera traseira via componente dedicado.
Usa declare_component para comunicacao bidirecional confiavel.
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
        _ok = False
        st.error("Biblioteca nao disponivel.")
        return None

    # Estado: imagem capturada aguardando processamento
    img_key = f"_scanner_pending_{key_suffix}"

    # Componente com camera traseira + upload de imagem como fallback
    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {{ margin:0; padding:8px; font-family:sans-serif; background:transparent; }}
#btn {{ 
    width:100%; padding:14px; background:#FF4B4B; color:white;
    border:none; border-radius:10px; font-size:16px; font-weight:bold;
    cursor:pointer; 
}}
#btn:active {{ background:#cc3333; }}
video {{ width:100%; border-radius:8px; display:none; }}
canvas {{ display:none; }}
#snap {{ width:100%; padding:12px; background:#00aa00; color:white;
    border:none; border-radius:8px; font-size:15px; font-weight:bold;
    cursor:pointer; margin-top:8px; display:none; }}
#msg {{ text-align:center; margin-top:6px; font-size:13px; color:#555; }}
</style>
</head>
<body>
<button id="btn" onclick="startCamera()">📷 Abrir câmera traseira</button>
<video id="vid" autoplay playsinline></video>
<button id="snap" onclick="capture()">📸 Fotografar</button>
<canvas id="cv"></canvas>
<div id="msg"></div>

<script>
var stream = null;

function startCamera() {{
    document.getElementById('msg').textContent = 'Abrindo câmera...';
    navigator.mediaDevices.getUserMedia({{
        video: {{ facingMode: {{ ideal: 'environment' }}, width: {{ ideal: 1280 }}, height: {{ ideal: 720 }} }}
    }}).then(function(s) {{
        stream = s;
        var vid = document.getElementById('vid');
        vid.srcObject = s;
        vid.style.display = 'block';
        document.getElementById('snap').style.display = 'block';
        document.getElementById('btn').style.display = 'none';
        document.getElementById('msg').textContent = 'Centralize o código e fotografe';
    }}).catch(function(e) {{
        document.getElementById('msg').textContent = 'Erro: ' + e.message + '. Verifique permissão de câmera.';
    }});
}}

function capture() {{
    var vid = document.getElementById('vid');
    var cv = document.getElementById('cv');
    cv.width = vid.videoWidth;
    cv.height = vid.videoHeight;
    cv.getContext('2d').drawImage(vid, 0, 0);
    document.getElementById('msg').textContent = '⏳ Analisando...';
    
    // Para o stream
    if (stream) stream.getTracks().forEach(t => t.stop());
    vid.style.display = 'none';
    document.getElementById('snap').style.display = 'none';
    document.getElementById('btn').style.display = 'block';
    document.getElementById('btn').textContent = '📷 Nova foto';
    
    // Envia para Streamlit
    var data = cv.toDataURL('image/jpeg', 0.92);
    window.parent.postMessage({{
        isStreamlitMessage: true,
        type: 'streamlit:setComponentValue',
        value: data
    }}, '*');
}}

// Escuta confirmacao do Streamlit
window.addEventListener('message', function(e) {{
    if (e.data && e.data.type === 'streamlit:render') {{
        document.getElementById('msg').textContent = '';
    }}
}});
</script>
</body>
</html>
"""

    result = components.html(html, height=320, scrolling=False)

    if result and isinstance(result, str) and result.startswith('data:image'):
        try:
            _, b64 = result.split(',', 1)
            img = Image.open(io.BytesIO(base64.b64decode(b64)))
            st.image(img, width=250, caption="Foto capturada")

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

            st.warning("❌ Não detectado. Tente a 20-30cm, boa luz, código centralizado.")
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
        ("orig", rgb), ("2x", grande), ("cinza", cinza_c.convert("RGB")),
        ("2x_cinza", cinza_gc.convert("RGB")), ("bw", bw), ("bw_2x", bw_g),
        ("nitido", nitido), ("recorte", rec_g),
    ]
