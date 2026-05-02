"""
scanner_ean.py -- Scanner EAN com camera traseira forcada
Usa componente HTML5 com capture=environment + zxing-cpp.
"""
import streamlit as st
import streamlit.components.v1 as components


def scanner_ean(key_suffix=""):
    try:
        import zxingcpp
        from PIL import Image, ImageEnhance, ImageFilter
        import io, base64
        import numpy as np
        _ok = True
    except ImportError:
        _ok = False

    if not _ok:
        st.error("Biblioteca de leitura nao disponivel.")
        return None

    # Chave unica para este scanner
    img_key = f"scanner_img_data_{key_suffix}"

    # Componente HTML com input que forca camera traseira
    html = f"""
    <div style="text-align:center; padding:4px;">
        <label for="cam_{key_suffix}" style="
            display:inline-block;
            background:#FF4B4B;
            color:white;
            padding:14px 28px;
            border-radius:10px;
            font-size:17px;
            font-weight:bold;
            cursor:pointer;
            box-shadow:0 2px 6px rgba(0,0,0,0.2);
        ">
            📷 Fotografar código de barras
        </label>
        <input
            type="file"
            id="cam_{key_suffix}"
            accept="image/*"
            capture="environment"
            style="display:none"
            onchange="sendImg(this)"
        />
        <div id="status_{key_suffix}" style="margin-top:8px; font-size:13px; color:#666;"></div>
        <canvas id="canvas_{key_suffix}" style="display:none;"></canvas>
    </div>
    <script>
    function sendImg(input) {{
        if (!input.files || !input.files[0]) return;
        var status = document.getElementById('status_{key_suffix}');
        status.textContent = '⏳ Processando...';
        var reader = new FileReader();
        reader.onload = function(e) {{
            // Comprime a imagem antes de enviar
            var img = new Image();
            img.onload = function() {{
                var canvas = document.getElementById('canvas_{key_suffix}');
                var ctx = canvas.getContext('2d');
                // Reduz para max 1200px mantendo proporcao
                var maxW = 1200;
                var ratio = Math.min(maxW / img.width, maxW / img.height, 1);
                canvas.width = img.width * ratio;
                canvas.height = img.height * ratio;
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                var dataUrl = canvas.toDataURL('image/jpeg', 0.9);
                status.textContent = '📤 Enviando para análise...';
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    value: dataUrl
                }}, '*');
            }};
            img.src = e.target.result;
        }};
        reader.readAsDataURL(input.files[0]);
    }}
    </script>
    """

    resultado = components.html(html, height=100)

    if resultado and isinstance(resultado, str) and resultado.startswith('data:image'):
        # Decodifica a imagem base64
        try:
            header, b64data = resultado.split(',', 1)
            img_bytes = base64.b64decode(b64data)
            img = Image.open(io.BytesIO(img_bytes))

            st.image(img, caption="Foto capturada", width=300)

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

            st.warning("❌ Código não detectado. Tente a 20-30cm, boa luz, código centralizado.")
        except Exception as e:
            st.error(f"Erro ao processar: {e}")

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
        ("original", rgb),
        ("2x", grande),
        ("cinza_contraste", cinza_c.convert("RGB")),
        ("2x_cinza_contraste", cinza_gc.convert("RGB")),
        ("bw", bw),
        ("bw_2x", bw_g),
        ("nitido", nitido),
        ("recorte_2x", rec_g),
    ]
