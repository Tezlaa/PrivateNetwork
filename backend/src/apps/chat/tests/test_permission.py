import pytest

from config.testing.api import APIClient

from apps.chat.permission.authentication import WSJWTAuthentication
from apps.chat.tests.utils import get_access_token


pytestmark = [pytest.mark.django_db]


def test_permission_class(as_user: APIClient):
    access_token = get_access_token(as_user.user)
    scope = {
        'type': 'websocket',
        'path': 'ws/chat/lobby/TestLobby',
        'query_string': b'',
        'headers': {
            'WS_AUTHORIZATION': access_token,
        },
        'subprotocols': [],
        'path_remaining': '',
        'url_route': {
            'args': (),
            'kwargs': {'lobby_name': 'TestLobby'}}
    }
    user, token = WSJWTAuthentication().authenticate(scope)
    assert user == as_user.user