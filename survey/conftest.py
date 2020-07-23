import json
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.utils import timezone

import pytest

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class DRFClient(APIClient):
    def __init__(self, user=None, anon=True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not anon:
            self.auth(user)

    def auth(self, user=None):
        self.user = user or self.create_superuser()
        token = Token.objects.create(user=self.user)
        self.credentials(
            HTTP_AUTHORIZATION=f'Token {token}',
            HTTP_X_GM_CLIENT='testing',
        )

    def create_superuser(self):
        user = User.objects.create_superuser('ardubro', 'ar@du.bro', 'Ardu12345bro')
        return user

    def logout(self):
        self.credentials()
        super().logout()

    def get(self, *args, **kwargs):
        return self._api_call('get', kwargs.get('expected_status_code', 200), *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._api_call('post', kwargs.get('expected_status_code', 201), *args, **kwargs)

    def put(self, *args, **kwargs):
        return self._api_call('put', kwargs.get('expected_status_code', 200), *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self._api_call('patch', kwargs.get('expected_status_code', 200), *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._api_call('delete', kwargs.get('expected_status_code', 204), *args, **kwargs)

    def _api_call(self, method, expected, *args, **kwargs):
        kwargs['format'] = kwargs.get('format', 'json')  # by default submit all data in JSON
        as_response = kwargs.pop('as_response', False)

        method = getattr(super(), method)
        response = method(*args, **kwargs)

        if as_response:
            return response

        content = self._decode(response)

        assert response.status_code == expected, content

        return content

    def _decode(self, response):
        if not len(response.content):
            return

        content = response.content.decode('utf-8', errors='ignore')
        if 'application/json' in response._headers['content-type'][1]:
            return json.loads(content)
        else:
            return content


@pytest.fixture
def api_user():
    return DRFClient(anon=True)


@pytest.fixture
def api_admin():
    return DRFClient(anon=False)


class CustomSurvey:
    def __init__(self):
        self.title = 'A Survey'
        self.description = 'A survey description'
        self.question_txt = {"title": "Question Text"}
        self.question_sel = {
            "title": "Question Select",
            "question_type": "select",
            "response_options": [
                {"title": "one"},
                {"title": "two"}
            ]
        }
        self.question_selmult = {
            "title": "Question Select Multiple",
            "question_type": "select multiple",
            "response_options": [
                {"title": "one"},
                {"title": "two"},
                {"title": "three"}
            ]
        }

    def generate_survey(self, title=None, description=None, start_date=None, end_date=None):
        survey = {
            'title': title or self.title,
            'description': description or self.description,
            'start_date': start_date or str(datetime.now(tz=timezone.utc)),
            'end_date': end_date or str(datetime.now(tz=timezone.utc) + timedelta(days=1)),
            'questions': [self.question_txt, self.question_sel, self.question_selmult]
        }
        return survey


@pytest.fixture
def surv_active():
    survey = CustomSurvey().generate_survey()
    return survey


@pytest.fixture
def surv_active2():
    survey = CustomSurvey().generate_survey(title='Survey 2')
    return survey


@pytest.fixture
def survey_overdue():
    start_date = str(datetime.now(tz=timezone.utc) - timedelta(days=1))
    end_date = str(datetime.now(tz=timezone.utc) - timedelta(seconds=1))
    return CustomSurvey().generate_survey(start_date=start_date, end_date=end_date)


@pytest.fixture
def survey_invalid_end_date():
    start_date = str(datetime.now(tz=timezone.utc))
    end_date = str(datetime.now(tz=timezone.utc) - timedelta(minutes=1))
    return CustomSurvey().generate_survey(start_date=start_date, end_date=end_date)
