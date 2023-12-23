from time import time
from typing import Iterator
import pytest

from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from channels.db import database_sync_to_async

from mixer.backend.django import Mixer

from apps.chat.routing import websocket_urlpatterns
from apps.chat.services.model_services import like_for_message, send_message
from apps.chat.tests.utils import tp_to_unaccurate
from apps.lobby.models import Lobby
from apps.lobby.services.model_services import (
    add_user_to_lobby_as_owner, add_user_to_lobby
)

from config.testing.api import APIClient

from conftest import create_user_by_username


pytestmark = [
    pytest.mark.django_db(transaction=True),
    pytest.mark.asyncio,
    pytest.mark.freeze_time("2023-01-01 15:00:00+00:00")
]


@pytest.fixture(autouse=True)
def lobby() -> Iterator[Lobby]:
    lobby = Lobby.objects.create(lobby_name='TestLobby')
    yield lobby


@pytest.fixture(autouse=True)
def create_lobby_and_connect_two_users(mixer: Mixer, as_user: APIClient, lobby: Lobby):
    lobby = add_user_to_lobby_as_owner(
        user=as_user.user,
        lobby=lobby,
    )
    add_user_to_lobby(
        user=create_user_by_username(mixer, 'TestUser2'),
        lobby=lobby
    )


@pytest.fixture
async def communicator_chat() -> WebsocketCommunicator:
    return WebsocketCommunicator(
        application=URLRouter(websocket_urlpatterns),
        path='ws/chat/TestLobby',
    )


@pytest.fixture
async def connected_communicator(communicator_chat: WebsocketCommunicator) -> WebsocketCommunicator:
    communicator = await communicator_chat
    connected, _ = await communicator.connect()
    if connected:
        return communicator
    

async def test_connection(communicator_chat):
    communicator = await communicator_chat
    connected, _ = await communicator.connect()
    assert connected


async def test_send_and_receive_message(connected_communicator: WebsocketCommunicator):
    communicator = await connected_communicator
    
    await communicator.send_json_to({
        'type': 'message',
        'message': 'Hello world',
        'username': 'TestUser',
    })
    
    expected_message = {
        'type': 'chat_message',
        'message': 'Hello world',
        'username': 'TestUser',
        'message_id': 1,
        'timestamp': int(time())
    }
    
    response = await communicator.receive_json_from()
    assert (
        tp_to_unaccurate(response) == tp_to_unaccurate(expected_message)
    )

    messages_count = await database_sync_to_async(Lobby.objects.all().count)()
    assert messages_count == 1
    

async def test_send_and_receive_like(connected_communicator: WebsocketCommunicator, lobby: Lobby):
    communicator = await connected_communicator
    
    message = await database_sync_to_async(send_message)(lobby, 'Hello world', 'TestUser')
    
    await communicator.send_json_to({
        'type': 'like',
        'message': 'Hello world',
        'username': 'TestUser',
        'message_id': message.pk
    })
    
    expected_message = {
        'type': 'chat_like',
        'message_id': message.pk,
        'username': 'TestUser',
    }
    response = await communicator.receive_json_from()
    
    assert response == expected_message
    
    assert await database_sync_to_async(message.user_liked.count)() == 1


async def test_delete_like(connected_communicator: WebsocketCommunicator, lobby: Lobby):
    communicator = await connected_communicator
    
    message = await database_sync_to_async(send_message)(lobby, 'Hello world', 'TestUser')
    await database_sync_to_async(like_for_message)(lobby, message.pk, 'TestUser')
    
    await communicator.send_json_to({
        'type': 'delete_like',
        'message': 'Hello world',
        'username': 'TestUser',
        'message_id': message.pk
    })
    
    expected_message = {
        'type': 'chat_delete_like',
        'message_id': message.pk,
        'username': 'TestUser',
    }
    response = await communicator.receive_json_from()
    
    assert response == expected_message
    
    assert await database_sync_to_async(message.user_liked.count)() == 0
