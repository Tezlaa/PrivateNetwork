from typing import Iterable
import pytest

from mixer.backend.django import Mixer

from apps.accounts.models import User

from config.testing.api import APIClient


pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def create_second_user(mixer: Mixer) -> Iterable[User]:
    user = mixer.blend(User, username='TestSecondUser')
    yield user


def test_create_contact(as_user: APIClient):
    data = {'username': 'TestSecondUser'}
    result = as_user.post('/api/v1/contact/', data)
    expected_json = {
        'connect': [
            {'username': 'TestSecondUser'},
            {'username': 'TestUser'},
        ],
        'messages': []
    }
    assert result == expected_json