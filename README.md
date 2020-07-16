# survey

[![Build Status](https://travis-ci.org/Ardubro/survey.svg?branch=master)](https://travis-ci.org/Ardubro/survey)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

Surveys service. Check out the project's [documentation](http://Ardubro.github.io/survey/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

# Local Development

Start the dev server for local development:
```bash
docker-compose up
```

Testing:

```bash
docker-compose run --rm web pytest
```
