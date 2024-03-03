FROM rust:1-alpine

RUN apk update \
    && apk add --no-cache gcc musl-dev libffi-dev openssl-dev \
    && apk add --no-cache python3 python3-dev py3-pip

RUN python3 -m venv /venv

ENV PATH="/venv/bin:$PATH"

WORKDIR /app

COPY ./compose/backend/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/backend /app/backend

EXPOSE 8000
