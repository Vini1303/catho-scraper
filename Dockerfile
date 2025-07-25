FROM python:3.11-slim-bullseye

RUN apt-get update && \
    apt-get install -y chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# 2. Copia apenas o requirements.txt primeiro (para cache eficiente)
COPY requirements.txt .

# 3. Instala dependências Python com verificação explícita
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir --default-timeout=100 -r requirements.txt || \
    { echo "Falha na instalação"; pip check; exit 1; }

# 4. Copia o restante da aplicação
COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "app:app"]
