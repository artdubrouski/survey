from django.db.models import Q

from fabrique_survey.surveys.models import Response

import pytest

from .utils import *

pytestmark = [pytest.mark.django_db]


def test_cant_response_without_survey_id(api_admin, api_user, survey_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=survey_active)
    survey_response = get_survey_response(survey_pk=admin_got['pk'])
    survey_response.pop('survey')
    api_user.post('/api/v1/survey-responses/', data=survey_response, expected_status_code=400)


def test_cant_response_without_responses(api_admin, api_user, survey_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=survey_active)
    survey_response = get_survey_response(survey_pk=admin_got['pk'])
    no_responses = survey_response
    no_responses.pop('responses')
    api_user.post('/api/v1/survey-responses/', data=no_responses, expected_status_code=400)
    survey_response['responses'] = []
    api_user.post('/api/v1/survey-responses/', data=survey_response, expected_status_code=400)


def test_cant_response_with_unrelated_response_options(api_admin, api_user,
                                                       survey_active, survey_active_another):
    admin_got1 = api_admin.post('/api/v1/surveys/', data=survey_active)
    admin_got2 = api_admin.post('/api/v1/surveys/', data=survey_active_another)
    survey_response = get_sr_responses_with_unrelated_responseoptions(admin_got1['pk'], admin_got2['pk'])
    api_user.post('/api/v1/survey-responses/', data=survey_response, expected_status_code=400)


def test_cannot_answer_question_not_in_current_survey(api_admin, api_user,
                                                      survey_active, survey_active_another):
    admin_got1 = api_admin.post('/api/v1/surveys/', data=survey_active)
    admin_got2 = api_admin.post('/api/v1/surveys/', data=survey_active_another)
    survey_response = get_sr_responses_on_questions_not_in_survey(admin_got1['pk'], admin_got2['pk'])
    api_user.post('/api/v1/survey-responses/', data=survey_response, expected_status_code=400)


def test_response_options_popped_if_questiontype_is_text(api_admin, api_user, survey_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=survey_active)
    survey_response = get_surv_resp_with_select_for_text(survey_pk=admin_got['pk'])
    api_user.post('/api/v1/survey-responses/', data=survey_response)
    resp_obj = Response.objects.get(response_text='textt')
    assert resp_obj.response_select.count() == 0


def test_txtresponse_popped_if_questtype_is_select(api_admin, api_user, survey_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=survey_active)
    survey_response = get_survey_response_text_for_select(survey_pk=admin_got['pk'])
    api_user.post('/api/v1/survey-responses/', data=survey_response)
    resp_objects = Response.objects.filter(Q(response_text='text_sel') | Q(response_text='text_selmult'))
    assert resp_objects.count() == 0


def test_invalidate_empty_response_options_for_select_question(api_admin, api_user, survey_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=survey_active)
    survey_response = get_surv_resp_empty_resp_select_for_select(survey_pk=admin_got['pk'])
    api_user.post('/api/v1/survey-responses/', data=survey_response, expected_status_code=400)


def test_invalidate_single_response_option_for_selectmultiquestion(api_admin, api_user, survey_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=survey_active)
    survey_response = get_surv_resp_singleselect_for_selectmutli(survey_pk=admin_got['pk'])
    api_user.post('/api/v1/survey-responses/', data=survey_response, expected_status_code=400)


def test_invalidate_multiple_choices_for_select_question(api_admin, api_user, survey_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=survey_active)
    survey_response = get_sr_mutselect_for_select(survey_pk=admin_got['pk'])
    api_user.post('/api/v1/survey-responses/', data=survey_response, expected_status_code=400)


def test_responses_cnt_must_be_not_lessthan_questions_cnt(api_admin, api_user, survey_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=survey_active)
    survey_response = get_sr_responses_less_than_questions(survey_pk=admin_got['pk'])
    api_user.post('/api/v1/survey-responses/', data=survey_response, expected_status_code=400)


def test_responses_cnt_must_be_no_morethan_questions_cnt(api_admin, api_user, survey_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=survey_active)
    survey_response = get_sr_responses_more_than_questions(survey_pk=admin_got['pk'])
    api_user.post('/api/v1/survey-responses/', data=survey_response, expected_status_code=400)
