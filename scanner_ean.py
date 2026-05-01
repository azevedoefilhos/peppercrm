"""
scanner_ean.py -- Componente de leitura de código de barras via câmera
Usa QuaggaJS para leitura de EAN-8, EAN-13 e outros formatos.
Integrado ao Streamlit via st.components.v1.html + st.session_state.
"""

SCANNER_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://cdnjs.cloudflare.com/ajax/libs/quagga/0.12.1/quagga.min.js"></script>
<style>
  body { margin: 0; padding: 0; background: #000; font-family: sans-serif; }
  #scanner-container {
    position: relative;
    width: 100%;
    max-width: 400px;
    margin: 0 auto;
  }
  #interactive {
    width: 100%;
    height: 250px;
    overflow: hidden;
    position: relative;
    background: #000;
  }
  #interactive video {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  #interactive canvas {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
  }
  .mira {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 80%; height: 60px;
    border: 2px solid #00ff00;
    border-radius: 4px;
    pointer-events: none;
    z-index: 10;
  }
  .mira::before {
    content: '';
    position: absolute;
    top: 50%; left: 0; right: 0;
    height: 2px;
    background: rgba(255, 0, 0, 0.7);
  }
  #resultado {
    padding: 12px;
    text-align: center;
    background: #1a1a1a;
    color: #fff;
    font-size: 14px;
    min-height: 40px;
  }
  #ean-value {
    font-size: 22px;
    font-weight: bold;
    color: #00ff00;
    letter-spacing: 2px;
  }
  #btn-area {
    display: flex;
    gap: 8px;
    padding: 8px;
    background: #1a1a1a;
    justify-content: center;
  }
  button {
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
  }
  #btn-confirmar {
    background: #00aa00;
    color: white;
    display: none;
  }
  #btn-limpar {
    background: #aa4400;
    color: white;
    display: none;
  }
  #status {
    font-size: 12px;
    color: #aaa;
    padding: 4px 12px;
    text-align: center;
    background: #1a1a1a;
  }
</style>
</head>
<body>
<div id="scanner-container">
  <div id="interactive">
    <div class="mira"></div>
  </div>
  <div id="resultado">
    <div id="status">📷 Aponte a câmera para o código de barras</div>
    <div id="ean-value"></div>
  </div>
  <div id="btn-area">
    <button id="btn-confirmar" onclick="confirmar()">✅ Usar este EAN</button>
    <button id="btn-limpar" onclick="limpar()">🔄 Ler outro</button>
  </div>
</div>

<script>
var lastEan = null;
var scanning = true;
var detected_count = {};

function iniciarScanner() {
  Quagga.init({
    inputStream: {
      name: "Live",
      type: "LiveStream",
      target: document.querySelector("#interactive"),
      constraints: {
        facingMode: "environment",  // câmera traseira
        width: { min: 400 },
        height: { min: 250 },
        aspectRatio: { min: 1, max: 2 }
      }
    },
    locator: {
      patchSize: "medium",
      halfSample: true
    },
    numOfWorkers: 2,
    frequency: 10,
    decoder: {
      readers: ["ean_reader", "ean_8_reader", "upc_reader", "upc_e_reader",
                "code_128_reader", "code_39_reader"]
    },
    locate: true
  }, function(err) {
    if (err) {
      document.getElementById("status").textContent = "❌ Erro: " + err;
      return;
    }
    Quagga.start();
    document.getElementById("status").textContent = "📷 Escaneando...";
  });

  Quagga.onDetected(function(result) {
    if (!scanning) return;
    var code = result.codeResult.code;
    if (!code || code.length < 8) return;

    // Confirma o mesmo EAN 3 vezes antes de aceitar (evita leituras erradas)
    detected_count[code] = (detected_count[code] || 0) + 1;
    if (detected_count[code] >= 3) {
      aceitar(code);
    } else {
      document.getElementById("status").textContent =
        "🔍 Detectando... (" + detected_count[code] + "/3)";
    }
  });

  Quagga.onProcessed(function(result) {
    var drawingCtx = Quagga.canvas.ctx.overlay;
    var drawingCanvas = Quagga.canvas.dom.overlay;
    if (result) {
      if (result.boxes) {
        drawingCtx.clearRect(0, 0,
          parseInt(drawingCanvas.getAttribute("width")),
          parseInt(drawingCanvas.getAttribute("height")));
        result.boxes.filter(function(box) {
          return box !== result.box;
        }).forEach(function(box) {
          Quagga.ImageDebug.drawPath(box, {x: 0, y: 1}, drawingCtx,
            {color: "green", lineWidth: 2});
        });
      }
      if (result.box) {
        Quagga.ImageDebug.drawPath(result.box, {x: 0, y: 1}, drawingCtx,
          {color: "#00F", lineWidth: 2});
      }
      if (result.codeResult && result.codeResult.code) {
        Quagga.ImageDebug.drawPath(result.line, {x: 'x', y: 'y'}, drawingCtx,
          {color: "red", lineWidth: 3});
      }
    }
  });
}

function aceitar(code) {
  scanning = false;
  lastEan = code;
  Quagga.stop();
  document.getElementById("ean-value").textContent = code;
  document.getElementById("status").textContent = "✅ Código lido com sucesso!";
  document.getElementById("btn-confirmar").style.display = "inline-block";
  document.getElementById("btn-limpar").style.display = "inline-block";

  // Vibra o celular como feedback
  if (navigator.vibrate) navigator.vibrate(200);
}

function confirmar() {
  // Envia o EAN para o Streamlit
  window.parent.postMessage({
    type: "streamlit:setComponentValue",
    value: lastEan
  }, "*");
}

function limpar() {
  lastEan = null;
  scanning = true;
  detected_count = {};
  document.getElementById("ean-value").textContent = "";
  document.getElementById("status").textContent = "📷 Aponte a câmera para o código de barras";
  document.getElementById("btn-confirmar").style.display = "none";
  document.getElementById("btn-limpar").style.display = "none";
  iniciarScanner();
}

// Inicia automaticamente
iniciarScanner();
</script>
</body>
</html>
"""


def scanner_ean(altura=340):
    """
    Renderiza o componente de scanner de EAN.
    Retorna o EAN lido ou None.
    """
    import streamlit.components.v1 as components
    resultado = components.html(SCANNER_HTML, height=altura)
    return resultado
