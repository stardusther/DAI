# Dockerfile
FROM python:3.11-alpine

WORKDIR /code
COPY . /code
RUN pip install -r requirements.txt