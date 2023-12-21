from typing import Optional

import pytest

from mixer.backend.django import Mixer
from mixer.backend.django import mixer as _mixer

from django.contrib.auth import get_user_model

from apps.accounts.models import User

from config.testing.api import APIClient


@pytest.fixture
def user(mixer: Mixer) -> Optional[User]:
    return mixer.blend('accounts.User', username='TestUser')


@pytest.fixture
def as_anon() -> APIClient:
    return APIClient()


@pytest.fixture
def as_user(user: User) -> APIClient:
    return APIClient(user=user)


@pytest.fixture
def mixer() -> Mixer:
    return _mixer