# Estágio de construção
FROM python:3.11-slim-bookworm as builder

WORKDIR /app

# 1. Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    unzip \
    gcc \
    python3-dev \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# 2. Configura ambiente do Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_PATH=/usr/lib/chromium/
ENV DISPLAY=:99

# 3. Copia apenas requirements primeiro (cache eficiente)
COPY requirements.txt .

# 4. Instala dependências Python
RUN pip install --user --no-cache-dir -r requirements.txt

# Estágio final
FROM python:3.11-slim-bookworm

WORKDIR /app

# Copia apenas o necessário do builder
COPY --from=builder /root/.local /root/.local
COPY --from=builder /usr/bin/chromium /usr/bin/
COPY --from=builder /usr/lib/chromium-browser/ /usr/lib/chromium-browser/

# Copia a aplicação
COPY . .

# Configura variáveis
ENV PATH=/root/.local/bin:$PATH
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Cria volume para dados persistentes
VOLUME /app/data

# Porta do Flask
EXPOSE 5000

# Comando otimizado para produção
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "300", "--workers", "2", "app:app"]
