FROM python:3.11-slim

# Instala dependências do sistema incluindo libzbar
RUN apt-get update && apt-get install -y \
    libzbar0 \
    libzbar-dev \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
CMD ["sh", "-c", "python keepalive.py & streamlit run crm_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true"]
