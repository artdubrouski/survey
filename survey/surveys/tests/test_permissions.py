import pytest

from .utils import CustomSurveyResponse


pytestmark = [pytest.mark.django_db]


def test_user_cant_delete_survey(api_admin, api_user, surv_active):
    got = api_admin.post('/api/v1/surveys/', data=surv_active)
    api_user.delete(
        f'/api/v1/surveys/{got["pk"]}/',
        expected_status_code=401,
    )


def test_user_cant_delete_questions(api_admin, api_user, surv_active):
    api_admin.post('/api/v1/surveys/', data=surv_active)
    got = api_admin.get('/api/v1/questions/')
    question_pk = got['results'][0]['pk']
    api_user.delete(
        f'/api/v1/questions/{question_pk}/',
        expected_status_code=401,
    )


def test_user_cant_add_survey(api_user, surv_active):
    api_user.post(
        '/api/v1/surveys/',
        data=surv_active,
        expected_status_code=401,
    )


def test_user_cant_update_survey(api_admin, api_user, surv_active):
    got = api_admin.post('/api/v1/surveys/', data=surv_active)
    updated_survey = surv_active
    updated_survey['title'] = 'UPD'
    api_user.put(
        f'/api/v1/surveys/{got["pk"]}/',
        data=updated_survey,
        expected_status_code=401,
    )


def test_user_cant_update_survey_response(api_admin, api_user, surv_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=surv_active)
    surv_resp = CustomSurveyResponse(admin_got['pk']).get_valid_sr()
    user_got = api_user.post('/api/v1/survey-responses/', data=surv_resp)
    survey_resp_upd = CustomSurveyResponse(admin_got['pk']).get_another_valid_sr()
    survey_resp_upd['user_id'] = user_got['user_id']
    api_user.put(
        f'/api/v1/survey-responses/{user_got["pk"]}/',
        data=survey_resp_upd, expected_status_code=405,
    )
