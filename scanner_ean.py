"""
scanner_ean.py -- Scanner de código de barras via câmera
Usa st.camera_input + zxing-cpp com pre-processamento avancado de imagem.
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

    if not _ok:
        st.error("⚠️ Biblioteca de leitura não disponível.")
        return None

    img_file = st.camera_input(
        "📷 Tire foto do código de barras",
        key=f"cam_ean_{key_suffix}"
    )

    if img_file is None:
        return None

    try:
        img_original = Image.open(io.BytesIO(img_file.getvalue()))

        # Tenta decodificar com diferentes processamentos
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

        st.warning("❌ Código não detectado. Dicas: boa iluminação, código centralizado e paralelo à câmera.")
        return None

    except Exception as e:
        st.error(f"Erro: {e}")
        return None


def _preparar_imagens(img):
    """
    Gera múltiplas versões da imagem com diferentes pré-processamentos.
    Ordem: do mais simples ao mais agressivo.
    """
    from PIL import Image, ImageEnhance, ImageFilter, ImageOps
    resultados = []

    # 1. Original convertida para RGB
    rgb = img.convert("RGB")
    resultados.append(("original", rgb))

    # 2. Escala 2x (aumenta resolução para códigos pequenos)
    w, h = rgb.size
    grande = rgb.resize((w*2, h*2), Image.LANCZOS)
    resultados.append(("2x", grande))

    # 3. Escala de cinza com alto contraste
    cinza = rgb.convert("L")
    contraste = ImageEnhance.Contrast(cinza).enhance(2.5)
    resultados.append(("cinza_contraste", contraste.convert("RGB")))

    # 4. Escala 2x + cinza + contraste
    cinza_grande = grande.convert("L")
    cinza_grande_contraste = ImageEnhance.Contrast(cinza_grande).enhance(2.5)
    resultados.append(("2x_cinza_contraste", cinza_grande_contraste.convert("RGB")))

    # 5. Binarizacao (preto e branco puro) - ajuda com codigos de baixo contraste
    bw = cinza.point(lambda x: 0 if x < 128 else 255, '1').convert("RGB")
    resultados.append(("bw", bw))

    # 6. Binarizacao 2x
    bw_grande = cinza_grande.point(lambda x: 0 if x < 128 else 255, '1').convert("RGB")
    resultados.append(("bw_2x", bw_grande))

    # 7. Sharpening (nitidez) + contraste
    nitido = rgb.filter(ImageFilter.SHARPEN)
    nitido = ImageEnhance.Contrast(nitido).enhance(2.0)
    resultados.append(("nitido", nitido))

    # 8. Recorte central (foca na area mais provavel do codigo)
    w, h = rgb.size
    margem_h = h // 4
    margem_w = w // 8
    recorte = rgb.crop((margem_w, margem_h, w-margem_w, h-margem_h))
    recorte_grande = recorte.resize((recorte.width*2, recorte.height*2), Image.LANCZOS)
    resultados.append(("recorte_central_2x", recorte_grande))

    return resultados
