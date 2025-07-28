# Usa imagem Python 3.11.9 slim (otimizada para tamanho)
FROM python:3.11.9-slim-bookworm

# Configurações de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Cria e define o diretório de trabalho
WORKDIR /app

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copia TODO o código para o container
COPY . .

# Cria pasta para logs
RUN mkdir -p /app/logs

# Comando padrão de execução
CMD ["python", "src/main.py"]
