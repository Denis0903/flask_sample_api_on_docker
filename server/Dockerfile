# FROM python:3.8.1-slim
FROM python:3.9.0-slim

WORKDIR /usr/src/api
COPY . .
RUN apt-get update && apt-get install -y gcc libpcre3-dev libpq-dev && pip install poetry && poetry install

RUN useradd -r appuser
RUN chown -R appuser .
USER appuser

CMD ["poetry", "run", "uwsgi", "--ini", "uwsgi.ini"]
