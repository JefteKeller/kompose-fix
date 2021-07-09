# imagem base
FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code
COPY . /code/

RUN apt update \
    && apt install -y libpq-dev gcc

RUN pip install psycopg2

RUN pip install -r requirements.txt

