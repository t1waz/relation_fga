FROM python:3.12-alpine

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

RUN apk update \
    && apk upgrade \
    && apk add bash

WORKDIR /app

COPY ./compose/overseer_backend/requirements.txt /app

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY ./src /app

RUN find /app -type d -name .pytest_cache -exec rm -rf {} +
