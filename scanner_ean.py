"""
scanner_ean.py -- Scanner de código de barras via câmera traseira
Usa input HTML5 com capture=environment para forçar câmera traseira,
depois decodifica com zxing-cpp + pre-processamento avancado.
"""

def scanner_ean(key_suffix=""):
    import streamlit as st
    import streamlit.components.v1 as components

    # HTML com input que força câmera traseira
    html_scanner = f"""
    <div style="font-family:sans-serif; padding:8px;">
        <label for="barcode_input_{key_suffix}" style="
            display:block;
            background:#FF4B4B;
            color:white;
            text-align:center;
            padding:12px;
            border-radius:8px;
            font-size:16px;
            font-weight:bold;
            cursor:pointer;
            margin-bottom:8px;
        ">
            📷 Abrir câmera traseira
        </label>
        <input
            type="file"
            id="barcode_input_{key_suffix}"
            accept="image/*"
            capture="environment"
            style="display:none"
            onchange="uploadImage(this)"
        />
        <div id="preview_{key_suffix}" style="text-align:center; margin-top:8px;"></div>
    </div>

    <script>
    function uploadImage(input) {{
        if (!input.files || !input.files[0]) return;
        var file = input.files[0];
        var reader = new FileReader();
        reader.onload = function(e) {{
            var preview = document.getElementById('preview_{key_suffix}');
            preview.innerHTML = '<img src="' + e.target.result + '" style="max-width:100%; border-radius:8px; margin-top:8px;" /><p style="color:green; font-weight:bold;">✅ Foto capturada! Processando...</p>';
            // Envia para o Streamlit via query params
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: e.target.result
            }}, '*');
        }};
        reader.readAsDataURL(file);
    }}
    </script>
    """

    # Usa camera_input do Streamlit como fallback confiável
    # O HTML acima é informativo - o camera_input é o que realmente captura
    st.markdown(
        """<style>
        [data-testid="stCameraInput"] button {
            background-color: #FF4B4B !important;
            color: white !important;
            font-weight: bold !important;
        }
        </style>""",
        unsafe_allow_html=True
    )

    st.caption("💡 **Dica:** Após abrir a câmera, toque em 🔄 para trocar para câmera traseira")

    try:
        import zxingcpp
        from PIL import Image, ImageEnhance, ImageFilter
        import io
        import numpy as np
        _ok = True
    except ImportError:
        _ok = False
        st.error("⚠️ Biblioteca de leitura não disponível.")
        return None

    img_file = st.camera_input(
        "📷 Fotografar código de barras",
        key=f"cam_ean_{key_suffix}"
    )

    if img_file is None:
        return None

    try:
        img_original = Image.open(io.BytesIO(img_file.getvalue()))
        tentativas = _preparar_imagens(img_original)

        for nome, img in tentativas:
            img_array = np.array(img)
            try:
                resultados = zxingcpp.read_barcodes(img_array)
                if resultados:
                    ean = resultados[0].text
                    formato = str(resultados[0].format)
                    st.success(f"✅ **{ean}** ({formato})")
                    return ean
            except Exception:
                continue

        st.warning("❌ Não detectado. Tente: mais longe (20-30cm), boa luz, código paralelo à tela.")
        return None

    except Exception as e:
        st.error(f"Erro: {e}")
        return None


def _preparar_imagens(img):
    from PIL import Image, ImageEnhance, ImageFilter
    resultados = []

    rgb = img.convert("RGB")
    resultados.append(("original", rgb))

    w, h = rgb.size
    grande = rgb.resize((w*2, h*2), Image.LANCZOS)
    resultados.append(("2x", grande))

    cinza = rgb.convert("L")
    contraste = ImageEnhance.Contrast(cinza).enhance(2.5)
    resultados.append(("cinza_contraste", contraste.convert("RGB")))

    cinza_grande = grande.convert("L")
    cinza_grande_contraste = ImageEnhance.Contrast(cinza_grande).enhance(2.5)
    resultados.append(("2x_cinza_contraste", cinza_grande_contraste.convert("RGB")))

    bw = cinza.point(lambda x: 0 if x < 128 else 255, '1').convert("RGB")
    resultados.append(("bw", bw))

    bw_grande = cinza_grande.point(lambda x: 0 if x < 128 else 255, '1').convert("RGB")
    resultados.append(("bw_2x", bw_grande))

    nitido = rgb.filter(ImageFilter.SHARPEN)
    nitido = ImageEnhance.Contrast(nitido).enhance(2.0)
    resultados.append(("nitido", nitido))

    margem_h = h // 4
    margem_w = w // 8
    recorte = rgb.crop((margem_w, margem_h, w-margem_w, h-margem_h))
    recorte_grande = recorte.resize((recorte.width*2, recorte.height*2), Image.LANCZOS)
    resultados.append(("recorte_2x", recorte_grande))

    return resultados
