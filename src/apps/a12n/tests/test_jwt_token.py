import pytest


from config.testing.api import APIClient

from apps.accounts.models import User


pytestmark = [pytest.mark.django_db]


ACCESS = ''
REFRESH = ''


def test_obtain_token(as_anon: APIClient):
    global ACCESS, REFRESH
    
    User.objects.create_user('TestUser1', password='rootrootroot')
    data = {
        'username': 'TestUser1',
        'password': 'rootrootroot'
    }
    result = as_anon.post('/api/v1/token/', data, expected_status_code=200)
    
    assert result.get('access') is not None and result.get('refresh') is not None
    
    ACCESS = result.get('access')
    REFRESH = result.get('refresh')


def test_refresh_token(as_anon: APIClient):
    data = {
        'refresh': REFRESH
    }
    result = as_anon.post('/api/v1/token/refresh/', data, expected_status_code=200)
    assert result.get('access') != ACCESS