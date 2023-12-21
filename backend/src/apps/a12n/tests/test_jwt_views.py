from dataclasses import dataclass
import pytest


from config.testing.api import APIClient

from apps.accounts.models import User


pytestmark = [pytest.mark.django_db]


@dataclass
class Token:
    access: str
    refresh: str


@pytest.fixture(autouse=True)
def user_jwt() -> User:
    User.objects.create_user(
        username='TestUser1',
        password='rootrootroot'
    )
    yield


@pytest.fixture(autouse=True)
def tokens() -> Token:
    token = Token('', '')
    yield token


def test_obtain_token(as_anon: APIClient):
   
    data = {
        'username': 'TestUser1',
        'password': 'rootrootroot',
    }
    result = as_anon.post('/api/v1/token/', data, expected_status_code=200)
    
    assert result.get('access') is not None and result.get('refresh') is not None
    
    tokens.access = result.get('access')
    tokens.refresh = result.get('refresh')


def test_refresh_token(as_anon: APIClient):
    
    data = {
        'refresh': tokens.refresh
    }
    
    result = as_anon.post('/api/v1/token/refresh/', data, expected_status_code=200)
    assert result.get('access') != tokens.access
    tokens.access = result.get('access')


def test_status_api(as_anon: APIClient):
    
    as_anon.credentials(
        HTTP_AUTHORIZATION=f"Token {tokens.access}"
    )
    as_anon.get('/api/v1/token/status/', expected_status_code=200)


def test_logout_token(as_anon: APIClient):

    data = {
        'refresh': tokens.refresh
    }
    as_anon.post('/api/v1/token/logout/', data, expected_status_code=200)
    as_anon.get('/api/v1/token/status/', expected_status_code=401)