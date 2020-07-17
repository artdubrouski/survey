import json

from django.contrib.auth.models import User

import pytest

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

pytestmark = [pytest.mark.django_db]


def test_admin_can_auth():
    api = APIClient()
    user = User.objects.create_superuser('oleg', 'oleg@ok.com', 'Oleg12345')
    data = {'username': 'oleg', 'password': 'Oleg12345'}
    response = api.post('/api-token-auth/', data=data, format='json')
    content = response.content.decode('utf-8', errors='ignore')
    got = json.loads(content)
    assert Token.objects.get(user=user).key == got['token']
