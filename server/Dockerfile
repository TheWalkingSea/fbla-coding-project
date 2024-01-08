# syntax=docker/dockerfile:1
FROM python:3.12.1-alpine3.18
WORKDIR /app

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
ENV FLASK_DEBUG=True

EXPOSE 5000
COPY . .
CMD ["flask", "run"]