FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema primeiro
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements primeiro para aproveitar cache
COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_PATH=/usr/lib/chromium/
# Instala dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o resto da aplicação
COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
