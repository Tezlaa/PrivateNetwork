import pytest


from config.testing.api import APIClient

from apps.accounts.models import User


pytestmark = [pytest.mark.django_db]


def test_register(as_user: APIClient):
    register_data = {
        'username': 'TestUser1',
        'password': 'rootrootroot'
    }
    result = as_user.post('/api/v1/account/register/', register_data)
    expected_json = {
        'username': 'TestUser1',
        'avatar': None,
    }
    assert result == expected_json
    assert User.objects.filter(username='TestUser1').count() == 1


def test_obtaining_info_about_user(as_user: APIClient):
    result = as_user.get('/api/v1/account/me/')
    expected_json = {
        'username': 'TestUser',
        'avatar': None,
    }
    assert result == expected_json
    