from typing import Optional

import pytest

from mixer.backend.django import Mixer
from mixer.backend.django import mixer as _mixer

from apps.accounts.models import User

from config.testing.api import APIClient


def create_user_by_username(mixer: Mixer, username: str) -> Optional[User]:
    return mixer.blend('accounts.User', username=username)


@pytest.fixture
def user(mixer: Mixer) -> Optional[User]:
    return create_user_by_username(mixer, 'TestUser')


@pytest.fixture
def as_anon() -> APIClient:
    return APIClient()


@pytest.fixture
def as_user(user: User) -> APIClient:
    return APIClient(user=user)


@pytest.fixture
def mixer() -> Mixer:
    return _mixer