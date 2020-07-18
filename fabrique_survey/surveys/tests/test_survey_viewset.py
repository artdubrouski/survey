from datetime import datetime, timedelta

from django.utils import timezone

from fabrique_survey.surveys.models import Question

import pytest


pytestmark = [pytest.mark.django_db]


def test_can_add_survey(api_admin, surv_active):
    api_admin.post('/api/v1/surveys/', data=surv_active)


def test_can_get_survey(api_admin, api_user, surv_active):
    api_admin.post('/api/v1/surveys/', data=surv_active)
    got = api_user.get('/api/v1/surveys/')
    assert got['count'] == 1


def test_user_get_only_active_surveys(api_admin, api_user, survey_overdue):
    api_admin.post('/api/v1/surveys/', data=survey_overdue)
    got = api_user.get('/api/v1/surveys/')
    assert got['count'] == 0


def test_admin_can_get_all_surveys(api_admin, api_user,
                                   survey_overdue, surv_active):
    api_admin.post('/api/v1/surveys/', data=survey_overdue)
    api_admin.post('/api/v1/surveys/', data=surv_active)
    got = api_admin.get('/api/v1/surveys/')
    assert got['count'] == 2


def test_questions_instances_created_with_survey(api_admin, surv_active):
    api_admin.post('/api/v1/surveys/', data=surv_active)
    assert Question.objects.count() == 3


def test_admin_can_delete_survey(api_admin, surv_active):
    got = api_admin.post('/api/v1/surveys/', data=surv_active)
    api_admin.delete(f'/api/v1/surveys/{got["pk"]}/')


def test_admin_can_patch_survey(api_admin, surv_active):
    got = api_admin.post('/api/v1/surveys/', data=surv_active)
    data = {'title': 'new title'}
    got_patch = api_admin.patch(
        f'/api/v1/surveys/{got["pk"]}/',
        data=data,
    )
    assert got_patch['title'] == 'new title'


def test_admin_can_patch_survey_end_date(api_admin, surv_active):
    got = api_admin.post('/api/v1/surveys/', data=surv_active)
    new_end_date = datetime.now(tz=timezone.utc) + timedelta(days=2)
    data = {'end_date': new_end_date}
    got_patch = api_admin.patch(f'/api/v1/surveys/{got["pk"]}/', data=data)
    assert got_patch['end_date'] == new_end_date.strftime('%Y-%m-%dT%H:%M:%S')


def test_cant_update_survey_with_invalid_end_date(api_admin, surv_active):
    got = api_admin.post('/api/v1/surveys/', data=surv_active)
    new_end_date = datetime.now(tz=timezone.utc) - timedelta(days=100)
    data = {'end_date': new_end_date}
    api_admin.patch(
        f'/api/v1/surveys/{got["pk"]}/',
        data=data,
        expected_status_code=400,
    )
