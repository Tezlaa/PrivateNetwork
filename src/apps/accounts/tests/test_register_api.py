import pytest


from config.testing.api import APIClient

from apps.accounts.models import User


pytestmark = [pytest.mark.django_db]


def test_register(as_user: APIClient):
    register_data = {
        'username': 'TestUser1',
        'password': 'rootrootroot'
    }
    result = as_user.post('/api/v1/register/', register_data)
    expected_json = {
        'username': 'TestUser1'
    }
    assert result == expected_json
    assert User.objects.filter(username='TestUser1').count() == 1
    