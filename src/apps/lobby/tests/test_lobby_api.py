import pytest

from django.contrib.auth.models import User

from mixer.backend.django import Mixer

from config.testing.api import APIClient


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def user(mixer: Mixer) -> User:
    return mixer.blend(User, username='TestUser')


def test_all_user_lobbies(as_user: APIClient):
    result = as_user.get('/api/v1/lobby/all/')
    
    assert len(result) == 0