from unittest import result
import pytest

from config.testing.api import APIClient

from apps.lobby.models import Lobby
from apps.lobby.services.model_services import add_user_to_lobby_as_owner, get_lobby


pytestmark = [pytest.mark.django_db]


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
            {'username': 'TestUser'}
        ],
        'user_limit': 2,
        'user_connected': [
            {'username': 'TestUser'}
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
            {'username': 'TestUser'}
        ],
        'user_limit': 2,
        'user_connected': [
            {'username': 'TestUser'}
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
    
