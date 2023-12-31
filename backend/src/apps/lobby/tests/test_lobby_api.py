from datetime import datetime

import pytest

from django.conf import settings

from pytz import timezone

from config.testing.api import APIClient

from apps.chat.tests.utils import isoformat_to_unaccurate
from apps.chat.services.model_services import send_message
from apps.lobby.models import Lobby
from apps.lobby.services.model_services import (
    add_user_to_lobby_as_owner, get_lobby, add_user_to_lobby
)


FREEZE_TIME = '2023-01-01 15:00:00+00:00'

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.freeze_time(FREEZE_TIME)
]


@pytest.fixture(autouse=True)
def user_with_lobby(as_user: APIClient) -> Lobby:
    lobby = add_user_to_lobby_as_owner(
        user=as_user.user,
        lobby=Lobby.objects.create(lobby_name='TestLobby'),
    )

    return lobby
    

def test_all_user_lobbies(as_user: APIClient):
    result = as_user.get('/api/v1/lobby/all/')
    
    assert len(result) == 1
    assert result[0]['lobby_name'] == 'TestLobby'
    assert result[0]['owner']
    assert result[0]['owners'][0]['username'] == as_user.user.username
    

def test_create_lobby(as_user: APIClient):
    post_data = {
        "lobby_name": "TestLobby1",
        "password": 1111,
        "user_limit": 2
    }
    result = as_user.post('/api/v1/lobby/create/', post_data, format='json')
    
    expected_json = {
        'lobby_name': 'TestLobby1',
        'owners': [
            {'username': 'TestUser', 'avatar': None}
        ],
        'user_limit': 2,
        'user_connected': [
            {'username': 'TestUser', 'avatar': None}
        ],
        'messages': []
    }
    assert result == expected_json


def test_all_names_lobby(as_user: APIClient):
    result = as_user.get('/api/v1/lobby/allNames/')
    
    assert len(result) == 1
    assert result[0]['lobby_name'] == 'TestLobby'
    assert result[0]['user_connected'] == 1
    assert result[0]['owner']


def test_delete_lobby(as_user: APIClient):
    as_user.delete('/api/v1/lobby/delete/TestLobby', expected_status_code=204)
    assert Lobby.objects.filter(user_connected=as_user.user).count() == 0


def test_get_lobby(as_user: APIClient):
    result = as_user.get('/api/v1/lobby/getLobby/TestLobby')
    expected_json = {
        'lobby_name': 'TestLobby',
        'owners': [
            {'username': 'TestUser', 'avatar': None}
        ],
        'owner': True,
        'user_limit': 2,
        'user_connected': [
            {'username': 'TestUser', 'avatar': None}
        ],
        'messages': []
    }
    assert result == expected_json


def test_join_to_lobby(as_user: APIClient):
    lobby = Lobby.objects.create(lobby_name='TestJoinLobby', password=1992)
    as_user.post(
        '/api/v1/lobby/action/TestJoinLobby',
        {'password': 1992},
        format='json',
        expected_status_code=201
    )
    assert get_lobby(lobby_name='TestJoinLobby', password=1992, user=as_user.user) == lobby

    
def test_disconnect_from_lobby(as_user: APIClient):
    lobby = Lobby.objects.create(lobby_name='TestDisconnectLobby', password=1992)
    add_user_to_lobby(as_user.user, lobby)
    
    assert lobby.user_connected.all()[0] == as_user.user
    
    as_user.delete(
        '/api/v1/lobby/action/TestDisconnectLobby',
        {'password': 1992},
        format='json',
        expected_status_code=204
    )
    assert lobby.user_connected.all().count() == 0
    

def test_lobby_with_messages(as_user: APIClient, user_with_lobby: Lobby):   
    send_message(user_with_lobby, 'Test message', as_user.user)
    result = as_user.get('/api/v1/lobby/getLobby/TestLobby')
    
    expected_json = {
        'lobby_name': 'TestLobby',
        'owners': [
            {'username': 'TestUser', 'avatar': None}
        ],
        'owner': True,
        'user_limit': 2,
        'user_connected': [
            {'username': 'TestUser', 'avatar': None}
        ],
        'messages': [
            {
                'created_at': datetime.now(tz=timezone(settings.TIME_ZONE)).isoformat(),
                'files': [],
                'id': 1,
                'message': 'Test message',
                'reply_message': None,
                'user': {'avatar': None,
                         'username': 'TestUser'},
                'user_liked': [],
                'voice_record': None
            }
        ],
    }
    
    expected_json['messages'][0] = isoformat_to_unaccurate(expected_json['messages'][0])
    result['messages'][0] = isoformat_to_unaccurate(result['messages'][0])
    
    assert result == expected_json