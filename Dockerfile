FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get --no-install-recommends install -y \
    gettext libpq-dev build-essential libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . code
WORKDIR /code

EXPOSE 8000

CMD newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT --access-logfile - survey.wsgi:application
