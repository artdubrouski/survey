from survey.surveys.models import Question

import pytest


pytestmark = [pytest.mark.django_db]


def test_admin_can_delete_question(api_admin, surv_active):
    api_admin.post('/api/v1/surveys/', data=surv_active)
    got = api_admin.get('/api/v1/questions/')
    assert got['count'] == 3
    question_pk = got['results'][0]['pk']
    api_admin.delete(f'/api/v1/questions/{question_pk}/')
    got = api_admin.get('/api/v1/questions/')
    assert got['count'] == 2


@pytest.mark.parametrize('question_type', ['select', 'select multiple'])
def test_opts_cleared_on_qtype_change_to_text(api_admin, surv_active, question_type):
    api_admin.post('/api/v1/surveys/', data=surv_active)
    question_pk = Question.objects.get(question_type=question_type).pk
    got = api_admin.get(f'/api/v1/questions/{question_pk}/')
    assert len(got['response_options']) > 0
    got = api_admin.patch(
        f'/api/v1/questions/{question_pk}/',
        data={'question_type': 'text'},
    )
    assert got['response_options'] == []


@pytest.mark.parametrize('question_type', ['text', 'select', 'select multiple'])
def test_can_update_questions(api_admin, surv_active, question_type):
    api_admin.post('/api/v1/surveys/', data=surv_active)
    q_pk = Question.objects.get(question_type=question_type).pk
    api_admin.patch(f'/api/v1/questions/{q_pk}/', data={'title': 'new question'})


def test_can_add_question_to_survey(api_admin, surv_active):
    got = api_admin.post('/api/v1/surveys/', data=surv_active)
    api_admin.post(
        '/api/v1/questions/',
        data={'survey': got['pk'], 'title': 'new question'},
    )
    got_detail = api_admin.get(f'/api/v1/surveys/{got["pk"]}/')
    assert len(got_detail['questions']) == 4  # initially was 3


def test_can_delete_question_from_survey(api_admin, surv_active):
    got = api_admin.post('/api/v1/surveys/', data=surv_active)
    q_pk = Question.objects.get(question_type='text').pk
    api_admin.delete(f'/api/v1/questions/{q_pk}/')
    got_detail = api_admin.get(f'/api/v1/surveys/{got["pk"]}/')
    assert len(got_detail['questions']) == 2  # initially was 3
