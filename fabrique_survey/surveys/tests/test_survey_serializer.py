from datetime import datetime, timedelta

from django.utils import timezone

import pytest


pytestmark = [pytest.mark.django_db]


def test_cant_update_survey_start_date(api_admin, survey_active):
    got = api_admin.post('/api/v1/surveys/', data=survey_active)
    survey_active['start_date'] = str(datetime.now(tz=timezone.utc) + timedelta(seconds=1))
    api_admin.put(
        f'/api/v1/surveys/{got["pk"]}/',
        data=survey_active,
        expected_status_code=400,
    )


def test_cant_add_survey_with_invalid_end_date(api_admin, survey_invalid_end_date):
    api_admin.post(
        '/api/v1/surveys/',
        data=survey_invalid_end_date,
        expected_status_code=400,
    )


def test_cant_add_survey_without_questions(api_admin, survey_active):
    survey_active['questions'] = []
    api_admin.post(
        '/api/v1/surveys/',
        data=survey_active,
        expected_status_code=400,
    )


@pytest.mark.parametrize('data',
                         [{'title': 'new title'},
                          {'description': 'newdescr'},
                          {'end_date': str(datetime.now(tz=timezone.utc) + timedelta(days=100500))}])
def test_can_update_survey_fields(api_admin, survey_active, data):
    got = api_admin.post('/api/v1/surveys/', data=survey_active)
    api_admin.patch(f'/api/v1/surveys/{got["pk"]}/', data=data)


def test_can_update_questions_field(api_admin, survey_active):
    got = api_admin.post('/api/v1/surveys/', data=survey_active)
    data = {'questions': [{'title': 'W?'}]}
    got_questions = api_admin.get('/api/v1/questions/')
    assert got_questions['count'] == 3
    api_admin.patch(f'/api/v1/surveys/{got["pk"]}/', data=data)
    got_questions = api_admin.get('/api/v1/questions/')
    assert got_questions['count'] == 1  # unlinked questions are deleted
