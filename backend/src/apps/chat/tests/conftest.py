from typing import Iterator, Optional

import pytest

from mixer.backend.django import Mixer

from rest_framework_simplejwt.tokens import AccessToken

from apps.accounts.models import User
from apps.contact.services.model_services import create_contact_by_users
from apps.contact.models import Contact
from apps.lobby.models import Lobby
from apps.lobby.services.model_services import (
    add_user_to_lobby_as_owner, add_user_to_lobby
)

from config.testing.api import APIClient


pytestmark = [pytest.mark.django_db]


def create_user_by_username(mixer: Mixer, username: str) -> Optional[User]:
    return mixer.blend('accounts.User', username=username)


def get_access_token(user: User) -> str:
    return str(AccessToken.for_user(user))


@pytest.fixture(autouse=True)
def lobby() -> Iterator[Lobby]:
    lobby, _ = Lobby.objects.get_or_create(lobby_name='TestLobby')
    yield lobby


@pytest.fixture(autouse=True)
def second_user(mixer: Mixer) -> Iterator[User]:
    second_user = create_user_by_username(mixer, 'TestUser2')
    yield second_user
    

@pytest.fixture(autouse=True)
def create_lobby_and_connect_two_users(as_user: APIClient, second_user: User, lobby: Lobby):
    lobby = add_user_to_lobby_as_owner(
        user=as_user.user,
        lobby=lobby,
    )
    add_user_to_lobby(
        user=second_user,
        lobby=lobby,
    )


@pytest.fixture(autouse=True)
def contact(as_user: APIClient, second_user) -> Iterator[Contact]:
    contact = create_contact_by_users(
        request_user=as_user.user,
        user=second_user
    )
    yield contact
