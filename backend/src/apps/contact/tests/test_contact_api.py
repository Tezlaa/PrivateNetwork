from typing import Iterable
import pytest

from mixer.backend.django import Mixer

from apps.accounts.models import User
from apps.contact.models import Contact
from apps.contact.services.model_services import create_contact_by_users

from config.testing.api import APIClient


pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def create_second_user(mixer: Mixer) -> Iterable[User]:
    user = mixer.blend(User, username='TestSecondUser')
    yield user


@pytest.fixture(autouse=True)
def create_third_user(mixer: Mixer) -> Iterable[User]:
    user = mixer.blend(User, username='TestThirdUser')
    yield user


def test_get_contact_and_create_services(as_user: APIClient, create_third_user, create_second_user):
    create_contact_by_users(
        request_user=as_user.user,
        user=create_second_user
    )
    
    create_contact_by_users(
        request_user=as_user.user,
        user=create_second_user
    )
    
    assert Contact.objects.count() == 1
    
    create_contact_by_users(
        request_user=as_user.user,
        user=create_third_user
    )

    assert Contact.objects.count() == 2
    
    result = as_user.get('/api/v1/contact/')
    
    expected_json = [
        {
            'connect': [
                {'username': 'TestSecondUser'}, {'username': 'TestUser'}
            ],
            'messages': [],
            'connect_user': 'TestSecondUser'
        },
        {
            'connect': [
                {'username': 'TestThirdUser'}, {'username': 'TestUser'}
            ],
            'messages': [],
            'connect_user': 'TestThirdUser'
        }
    ]
    assert result == expected_json

    
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
    assert Contact.objects.count() == 1

