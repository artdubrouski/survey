# Surveys

Surveys API service.

## Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)

## Initialize the project

Start the dev server for local development:

```sh
docker-compose up
```

Create a superuser to login to the admin:

```sh
docker-compose run --rm web ./manage.py createsuperuser
```
