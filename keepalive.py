"""
keepalive.py -- PepperCRM
Faz ping no proprio app a cada 4 minutos para manter o Railway container ativo.
"""
import time
import os
import requests
import threading

# URL hardcoded como fallback garantido
FALLBACK_URL = "https://peppercrm-production.up.railway.app"
_domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "")
APP_URL = f"https://{_domain}" if _domain and not _domain.startswith("http") else (
          _domain if _domain else FALLBACK_URL)

INTERVALO = 240  # 4 minutos

def ping():
    try:
        r = requests.get(APP_URL, timeout=15, allow_redirects=True)
        print(f"[keepalive] ping OK {r.status_code} — {APP_URL}", flush=True)
    except Exception as e:
        print(f"[keepalive] ping falhou: {e}", flush=True)

def loop():
    print(f"[keepalive] iniciado — URL: {APP_URL}", flush=True)
    time.sleep(30)  # aguarda Streamlit subir
    while True:
        ping()
        time.sleep(INTERVALO)

if __name__ == "__main__":
    loop()
