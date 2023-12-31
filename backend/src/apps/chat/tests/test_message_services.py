import pytest

from apps.lobby.models import Lobby
from apps.chat.services.model_services import send_message, send_message_by_username
from apps.chat.models import Message

from config.testing.api import APIClient


pytestmark = [pytest.mark.django_db]


def test_sending_by_username(as_user: APIClient, lobby: Lobby):
    lobby_chat = Lobby.objects.get(lobby_name=lobby.lobby_name).chat
    
    created_message = send_message_by_username(lobby, 'Test Message', as_user.username)
    assert created_message == Message.objects.first()
    assert created_message == lobby_chat.first()
    
    send_message(lobby, 'Test Message', as_user.user)
    assert lobby_chat.count() == 2
    
    
def test_sending_by_user_instance(as_user: APIClient, lobby: Lobby):
    lobby_chat = Lobby.objects.get(lobby_name=lobby.lobby_name).chat
    
    created_message = send_message(lobby, 'Test Message', as_user.user)
    assert created_message == Message.objects.first()
    assert created_message == lobby_chat.first()
    
    send_message(lobby, 'Test Message', as_user.user)
    assert lobby_chat.count() == 2