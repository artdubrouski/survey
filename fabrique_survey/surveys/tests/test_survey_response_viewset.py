import pytest

from rest_framework.test import APIClient

from .utils import *

pytestmark = [pytest.mark.django_db]


def test_user_id_created(api_admin, survey_active, api_user):
    admin_got = api_admin.post('/api/v1/surveys/', data=survey_active)
    survey_response = get_survey_response(admin_got['pk'])
    user_got = api_user.post(
        '/api/v1/survey-responses/',
        data=survey_response,
    )
    assert len(user_got['user_id']) == 36  # uuid4 key len


def test_user_cookie_created(api_admin, survey_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=survey_active)
    survey_response = get_survey_response(admin_got['pk'])
    api_user = APIClient()
    response = api_user.post(
        '/api/v1/survey-responses/',
        data=survey_response,
        format='json',
    )
    assert len(response.cookies['user_id'].value) == 36


def test_user_can_add_survey_response(api_admin, api_user, survey_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=survey_active)
    survey_response = get_survey_response(survey_pk=admin_got['pk'])
    api_user.post('/api/v1/survey-responses/', data=survey_response)


def test_no_deleted_question_in_surv_resp(api_admin, api_user, survey_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=survey_active)
    surv_response = get_survey_response(admin_got['pk'])
    user_got = api_user.post('/api/v1/survey-responses/', data=surv_response)

    admin_got = api_admin.get('/api/v1/questions/')
    question_pk = admin_got['results'][0]['pk']
    api_admin.delete(f'/api/v1/questions/{question_pk}/')

    user_got = api_user.get(f'/api/v1/survey-responses/{user_got["pk"]}/')
    responses = [
        response['question_title'] for response in user_got['responses']
    ]
    assert 'deleted' in responses
