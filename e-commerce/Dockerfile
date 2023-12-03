# Dockerfile
FROM python:3.11-alpine

WORKDIR /e-commerce
COPY .. /e-commerce
RUN apk update && \
    apk add --no-cache build-base && \
    apk add --no-cache libffi-dev && \
    pip install -r requirements.txt