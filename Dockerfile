FROM python:3.11-slim-bullseye

WORKDIR /app

# Instala dependências críticas
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Configura Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_PATH=/usr/lib/chromium/

# Copia arquivos necessários
COPY requirements.txt .
COPY app.py .
COPY templates/ ./templates/

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Porta da aplicação
EXPOSE 5000

# Comando de inicialização
CMD ["python", "app.py"]
