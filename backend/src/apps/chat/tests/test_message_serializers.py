from collections import OrderedDict

from datetime import datetime

from pytz import timezone

import pytest

from django.conf import settings

from apps.chat.serializers import MessageSerializer
from apps.chat.services.model_services import send_message
from apps.chat.tests.utils import isoformat_to_unaccurate

from config.testing.api import APIClient

from apps.lobby.models import Lobby


pytestmark = [
    pytest.mark.django_db,
    pytest.mark.freeze_time('2023-01-01 15:00:00+00:00')
]


def test_message_serializer(as_user: APIClient, lobby: Lobby):
    created_message = send_message(lobby, 'Test Message', as_user.user)
    serialize_data = MessageSerializer(instance=created_message).data
    expected_json = {
        'id': 1,
        'user': OrderedDict([('username', 'TestUser'), ('avatar', None)]),
        'user_liked': [],
        'reply_message': None,
        'message': 'Test Message',
        'voice_record': None,
        'created_at': datetime.now(tz=timezone(settings.TIME_ZONE)).isoformat(),
        'files': [],
    }
    assert (
        isoformat_to_unaccurate(serialize_data) == isoformat_to_unaccurate(expected_json)
    )
