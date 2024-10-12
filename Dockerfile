FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY .env /app/.env

EXPOSE 5000

ENV FLASK_ENV=development

CMD flask run