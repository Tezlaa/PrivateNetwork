from time import time
from typing import Iterator
from urllib import response
import pytest

from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter

from apps.chat.routing import websocket_urlpatterns
from apps.chat.tests.utils import tp_to_unaccurate
from apps.lobby.models import Lobby
from apps.lobby.services.model_services import add_user_to_lobby_as_owner

from config.testing.api import APIClient


pytestmark = [
    pytest.mark.django_db(transaction=True),
    pytest.mark.asyncio,
    pytest.mark.freeze_time("2023-01-01 15:00:00+00:00")
]


@pytest.fixture
async def chat_communicator() -> WebsocketCommunicator:
    return WebsocketCommunicator(
        application=URLRouter(websocket_urlpatterns),
        path='ws/chat/Lobby1',
    )


@pytest.fixture
async def notify_communicator(lobbies: Iterator[list[Lobby]]) -> WebsocketCommunicator:
    return WebsocketCommunicator(
        application=URLRouter(websocket_urlpatterns),
        path='ws/notify/',
        headers=[lobby.lobby_name for lobby in lobbies],
    )


@pytest.fixture(autouse=True)
def lobbies(as_user: APIClient) -> Iterator[list[Lobby]]:
    lobbies = [Lobby.objects.create(lobby_name=lobby_name) for lobby_name in [
        'Lobby1', 'Lobby2', 'Lobby3', 'Lobby4', 'Lobby5'
    ]]
    
    lobbies_with_user = []
        
    for lobby in lobbies:
        lobbies_with_user.append(
            add_user_to_lobby_as_owner(
                user=as_user.user,
                lobby=lobby,
            )
        )
    
    yield lobbies_with_user


async def test_connection(notify_communicator):
    communicator = await notify_communicator
    
    connected, _ = await communicator.connect()
    assert connected


async def test_receive_message(notify_communicator: WebsocketCommunicator,
                               chat_communicator: WebsocketCommunicator):
    
    notify_communicator = await notify_communicator
    chat_communicator = await chat_communicator
    
    await notify_communicator.connect()
    await chat_communicator.connect()
    
    await chat_communicator.send_json_to({
        'type': 'message',
        'message': 'Hello world',
        'username': 'TestUser',
    })
    
    expected_json = {
        'type': 'chat_message',
        'message': 'Hello world',
        'username': 'TestUser',
        'message_id': 4,
        'timestamp': int(time())
    }
    response = await notify_communicator.receive_json_from()
    
    assert (
        tp_to_unaccurate(response) == tp_to_unaccurate(expected_json)
    )
    
    