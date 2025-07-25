FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
COPY . .
CMD ["python", "app.py"]
