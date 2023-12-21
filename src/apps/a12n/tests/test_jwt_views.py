import pytest


from config.testing.api import APIClient

from apps.accounts.models import User


pytestmark = [pytest.mark.django_db]


ACCESS = ''
REFRESH = ''


@pytest.fixture(autouse=True)
def user_jwt() -> User:
    User.objects.create_user(
        username='TestUser1',
        password='rootrootroot'
    )
    yield


def test_obtain_token(as_anon: APIClient):
    global ACCESS, REFRESH
    
    data = {
        'username': 'TestUser1',
        'password': 'rootrootroot',
    }
    result = as_anon.post('/api/v1/token/', data, expected_status_code=200)
    
    assert result.get('access') is not None and result.get('refresh') is not None
    
    ACCESS = result.get('access')
    REFRESH = result.get('refresh')


def test_refresh_token(as_anon: APIClient):
    global ACCESS, REFRESH
    
    data = {
        'refresh': REFRESH
    }
    result = as_anon.post('/api/v1/token/refresh/', data, expected_status_code=200)
    assert result.get('access') != ACCESS
    ACCESS = result.get('access')


def test_status_api(as_anon: APIClient):
    global ACCESS, REFRESH
    
    as_anon.credentials(
        HTTP_AUTHORIZATION=f"Token {ACCESS}"
    )
    as_anon.get('/api/v1/token/status/', expected_status_code=200)


def test_logout_token(as_anon: APIClient):
    global REFRESH
    
    data = {
        'refresh': REFRESH
    }
    as_anon.post('/api/v1/token/logout/', data, expected_status_code=200)
    as_anon.get('/api/v1/token/status/', expected_status_code=401)