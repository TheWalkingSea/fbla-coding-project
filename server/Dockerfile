# syntax=docker/dockerfile:1
FROM python:3.9.18-slim-bullseye
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
ENV FLASK_DEBUG=True

EXPOSE 5000
COPY . .
CMD ["flask", "run"]