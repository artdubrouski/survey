from django.db.models import Q

from survey.surveys.models import Response

from .utils import CustomSurveyResponse

import pytest


pytestmark = [pytest.mark.django_db]


def test_cant_response_without_survey_id(api_admin, api_user, surv_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=surv_active)
    survey_response = CustomSurveyResponse(admin_got['pk']).get_valid_sr()
    survey_response.pop('survey')
    api_user.post(
        '/api/v1/survey-responses/',
        data=survey_response,
        expected_status_code=400,
    )


def test_cant_response_without_question_id(api_admin, api_user, surv_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=surv_active)
    survey_response = CustomSurveyResponse(admin_got['pk']).get_valid_sr()
    survey_response['responses'][0].pop('question')
    api_user.post(
        '/api/v1/survey-responses/',
        data=survey_response,
        expected_status_code=400,
    )


def test_cant_response_without_responses(api_admin, api_user, surv_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=surv_active)
    survey_response = CustomSurveyResponse(admin_got['pk']).get_valid_sr()
    no_responses = survey_response
    no_responses.pop('responses')
    api_user.post(
        '/api/v1/survey-responses/',
        data=no_responses,
        expected_status_code=400,
    )
    survey_response['responses'] = []
    api_user.post(
        '/api/v1/survey-responses/',
        data=survey_response,
        expected_status_code=400,
    )


def test_cant_resp_with_unrelated_resp_options(api_admin, api_user, surv_active, surv_active2):
    admin_got1 = api_admin.post('/api/v1/surveys/', data=surv_active)
    admin_got2 = api_admin.post('/api/v1/surveys/', data=surv_active2)
    custom_sr = CustomSurveyResponse(admin_got1['pk'])
    surv_resp = custom_sr.get_invalid_sr_unrelated_resp_options(admin_got2['pk'])
    api_user.post(
        '/api/v1/survey-responses/',
        data=surv_resp,
        expected_status_code=400,
    )


def test_cant_answer_unrelated_question(api_admin, api_user, surv_active, surv_active2):
    admin_got1 = api_admin.post('/api/v1/surveys/', data=surv_active)
    admin_got2 = api_admin.post('/api/v1/surveys/', data=surv_active2)
    custom_sr = CustomSurveyResponse(admin_got1['pk'])
    surv_resp = custom_sr.get_invalid_sr_unrelated_questions(admin_got2['pk'])
    api_user.post(
        '/api/v1/survey-responses/',
        data=surv_resp,
        expected_status_code=400,
    )


def test_resp_opts_popped_if_qtype_is_text(api_admin, api_user, surv_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=surv_active)
    custom_sr = CustomSurveyResponse(admin_got['pk'])
    survey_response = custom_sr.get_invalid_sr_redundant_select_for_text()
    api_user.post('/api/v1/survey-responses/', data=survey_response)
    resp_obj = Response.objects.get(response_text='textt')
    assert resp_obj.response_select.count() == 0


def test_txtresp_popped_if_qtype_is_select(api_admin, api_user, surv_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=surv_active)
    custom_sr = CustomSurveyResponse(admin_got['pk'])
    survey_response = custom_sr.get_valid_sr_redundant_text_for_select()
    api_user.post('/api/v1/survey-responses/', data=survey_response)
    resp_objects = Response.objects.filter(
        Q(response_text='text_sel') | Q(response_text='text_selmult')
    )
    assert resp_objects.count() == 0


def test_invalidate_empty_resp_opts_for_qtype_select(api_admin, api_user, surv_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=surv_active)
    custom_sr = CustomSurveyResponse(admin_got['pk'])
    survey_response = custom_sr.get_invalid_sr_empty_resp_opts_for_select()
    api_user.post(
        '/api/v1/survey-responses/',
        data=survey_response,
        expected_status_code=400,
    )


def test_invalidate_single_resp_opt_for_selectmult(api_admin, api_user, surv_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=surv_active)
    custom_sr = CustomSurveyResponse(admin_got['pk'])
    surv_resp = custom_sr.get_invalid_sr_singleselect_for_selectmult()
    api_user.post(
        '/api/v1/survey-responses/',
        data=surv_resp,
        expected_status_code=400,
    )


def test_invalidate_mult_choices_for_qtype_select(api_admin, api_user, surv_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=surv_active)
    custom_sr = CustomSurveyResponse(admin_got['pk'])
    survey_response = custom_sr.get_invalid_sr_mutselect_for_select()
    api_user.post(
        '/api/v1/survey-responses/',
        data=survey_response,
        expected_status_code=400,
    )


def test_responses_cnt_equal_to_questions_cnt(api_admin, api_user, surv_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=surv_active)
    custom_sr = CustomSurveyResponse(admin_got['pk'])
    survey_response = custom_sr.get_invalid_sr_responses_lt_questions()
    api_user.post(
        '/api/v1/survey-responses/',
        data=survey_response,
        expected_status_code=400,
    )
    surv_resp = custom_sr.get_invalid_sr_responses_gt_questions()
    api_user.post(
        '/api/v1/survey-responses/',
        data=surv_resp,
        expected_status_code=400,
    )

def test_user_can_take_survey_only_once(api_admin, api_user, surv_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=surv_active)
    survey_response = CustomSurveyResponse(admin_got['pk']).get_valid_sr()
    api_user.post(
        '/api/v1/survey-responses/',
        data=survey_response,
        expected_status_code=201,
    )
    api_user.post(
        '/api/v1/survey-responses/',
        data=survey_response,
        expected_status_code=400,
    )
