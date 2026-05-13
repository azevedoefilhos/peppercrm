"""
keepalive.py -- PepperCRM
Faz ping no proprio app a cada 4 minutos para manter o Railway container ativo.
Roda em paralelo com o Streamlit via Procfile.
"""
import time
import os
import requests

# URL do proprio app no Railway
APP_URL = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "")
if APP_URL and not APP_URL.startswith("http"):
    APP_URL = f"https://{APP_URL}"

INTERVALO = 240  # 4 minutos em segundos

def ping():
    if not APP_URL:
        return
    try:
        requests.get(APP_URL, timeout=10)
    except Exception:
        pass  # falha silenciosa — o objetivo e so manter o container vivo

if __name__ == "__main__":
    # Aguarda 30s para o Streamlit subir antes do primeiro ping
    time.sleep(30)
    while True:
        ping()
        time.sleep(INTERVALO)
