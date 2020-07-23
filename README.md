# survey

[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

Surveys service. Check out the project's [documentation](http://Ardubro.github.io/survey/).

Survey can be taken by anonymous users.

User id is stored in a user __cookie__ file and passed to the API on SurveyResponse posting, so that an anonymous user can get only his survey responses back later.

Dealing with cookies in an API service may be not what you want and I would recommend considering other options for  users identification before using this API.

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
