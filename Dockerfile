FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y wget chromium chromium-driver

COPY . .

RUN pip install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0:5000", "app:app"]
