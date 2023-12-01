import pytest

from django.contrib.auth.models import User

from config.testing.api import APIClient

from apps.lobby.models import Lobby


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def user_with_lobby(user: User) -> Lobby:
    lobby = Lobby.objects.create(lobby_name='TestLobby')
    lobby.user_connected.add(user)
    lobby.save()
    return lobby
    

def test_all_user_lobbies(as_user: APIClient, user_with_lobby: Lobby):
    result = as_user.get('/api/v1/lobby/all/')
    
    assert len(result) == 1
    assert result[0]['lobby_name'] == 'TestLobby'
    assert not result[0]['owner']
    

def test_create_lobby(as_user: APIClient):
    post_data = {
        "lobby_name": "TestLobby",
        "password": 1111,
        "user_limit": 2
    }
    result = as_user.post('/api/v1/lobby/create/', post_data, format='json')
    
    assert result['lobby_name'] == 'TestLobby'
    assert len(result['owners']) == 1
    assert result['owners'][0]['username'] == 'TestUser'
    assert result['user_limit'] == 2
    assert len(result['user_connected']) == 1
    assert result['user_connected'][0]['username'] == 'TestUser'
    assert len(result['messages']) == 0


def test_all_names_lobby(as_user: APIClient, user_with_lobby: Lobby):
    result = as_user.get('/api/v1/lobby/allNames/')
    
    assert len(result) == 1
    assert result[0]['lobby_name'] == 'TestLobby'
    assert result[0]['user_connected'] == 1
    assert not result[0]['owner']