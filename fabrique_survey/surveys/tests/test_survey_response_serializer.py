from django.db.models import Q

from fabrique_survey.surveys.models import Response

import pytest

from .utils import *

pytestmark = [pytest.mark.django_db]


def test_cant_response_without_survey_id(api_admin, api_user, survey_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=survey_active)
    survey_response = get_survey_response(survey_pk=admin_got['pk'])
    survey_response.pop('survey')
    api_user.post(
        '/api/v1/survey-responses/',
        data=survey_response,
        expected_status_code=400,
    )


def test_cant_response_without_responses(api_admin, api_user, survey_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=survey_active)
    survey_response = get_survey_response(survey_pk=admin_got['pk'])
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


def test_cant_resp_with_unrelated_resp_options(api_admin,
                                               api_user,
                                               survey_active,
                                               survey_active_another):
    admin_got1 = api_admin.post(
        '/api/v1/surveys/',
        data=survey_active,
    )
    admin_got2 = api_admin.post(
        '/api/v1/surveys/',
        data=survey_active_another,
    )
    survey_response = get_sr_unrelated_resp_options(admin_got1['pk'],
                                                    admin_got2['pk'])
    api_user.post(
        '/api/v1/survey-responses/',
        data=survey_response,
        expected_status_code=400,
    )


def test_cant_answer_unrelated_question(api_admin, api_user,
                                        survey_active, survey_active_another):
    admin_got1 = api_admin.post('/api/v1/surveys/', data=survey_active)
    admin_got2 = api_admin.post('/api/v1/surveys/', data=survey_active_another)
    survey_response = get_sr_resp_unrelated_questions(admin_got1['pk'],
                                                      admin_got2['pk'])
    api_user.post(
        '/api/v1/survey-responses/',
        data=survey_response,
        expected_status_code=400,
    )


def test_resp_opts_popped_if_qtype_is_text(api_admin, api_user, survey_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=survey_active)
    survey_response = get_surv_resp_with_select_for_text(survey_pk=admin_got['pk'])
    api_user.post('/api/v1/survey-responses/', data=survey_response)
    resp_obj = Response.objects.get(response_text='textt')
    assert resp_obj.response_select.count() == 0


def test_txtresp_popped_if_qtype_is_select(api_admin, api_user, survey_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=survey_active)
    survey_response = get_survey_response_text_for_select(survey_pk=admin_got['pk'])
    api_user.post('/api/v1/survey-responses/', data=survey_response)
    resp_objects = Response.objects.filter(
        Q(response_text='text_sel') | Q(response_text='text_selmult')
    )
    assert resp_objects.count() == 0


def test_invalidate_empty_resp_opts_for_qtype_select(api_admin, api_user, survey_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=survey_active)
    survey_response = get_sr_empty_resp_opts_for_select(survey_pk=admin_got['pk'])
    api_user.post(
        '/api/v1/survey-responses/',
        data=survey_response,
        expected_status_code=400,
    )


def test_invalidate_single_resp_opt_for_selectmult(api_admin, api_user, survey_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=survey_active)
    survey_response = get_surv_resp_singleselect_for_selectmutli(survey_pk=admin_got['pk'])
    api_user.post(
        '/api/v1/survey-responses/',
        data=survey_response,
        expected_status_code=400,
    )


def test_invalidate_mult_choices_for_qtype_select(api_admin, api_user, survey_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=survey_active)
    survey_response = get_sr_mutselect_for_select(survey_pk=admin_got['pk'])
    api_user.post(
        '/api/v1/survey-responses/',
        data=survey_response,
        expected_status_code=400,
    )


def test_responses_cnt_equal_to_questions_cnt(api_admin, api_user, survey_active):
    admin_got = api_admin.post('/api/v1/surveys/', data=survey_active)
    survey_response = get_sr_responses_lt_questions(survey_pk=admin_got['pk'])
    api_user.post(
        '/api/v1/survey-responses/',
        data=survey_response,
        expected_status_code=400,
    )
    survey_response = get_sr_responses_gt_questions(survey_pk=admin_got['pk'])
    api_user.post(
        '/api/v1/survey-responses/',
        data=survey_response,
        expected_status_code=400,
    )
