FROM python:3.11-slim

RUN mkdir /app

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["echo", "Hello world!"]