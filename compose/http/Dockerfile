FROM rust:1-alpine

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

RUN apk update \
    && apk upgrade \
    && apk add python3 python3-dev py3-pip gcc libc-dev bash \
    && apk add bash

WORKDIR /app

COPY ./compose/http/requirements.txt /app

RUN pip install --upgrade pip \
    && pip install -r requirements.txt
