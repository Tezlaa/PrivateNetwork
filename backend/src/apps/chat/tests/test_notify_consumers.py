from time import time
from typing import Iterator

import pytest

from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from channels.db import database_sync_to_async

from apps.chat.models import Message
from apps.chat.routing import websocket_urlpatterns
from apps.chat.tests.utils import tp_to_unaccurate
from apps.contact.models import Contact
from apps.lobby.models import Lobby
from apps.lobby.services.model_services import add_user_to_lobby_as_owner

from config.testing.api import APIClient


pytestmark = [
    pytest.mark.django_db(transaction=True),
    pytest.mark.asyncio,
    pytest.mark.freeze_time("2023-01-01 15:00:00+00:00")
]


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


@pytest.fixture
async def chat_communicator() -> WebsocketCommunicator:
    return WebsocketCommunicator(
        application=URLRouter(websocket_urlpatterns),
        path='ws/chat/lobby/Lobby1',
    )


@pytest.fixture
async def chat_communicator_2() -> WebsocketCommunicator:
    return WebsocketCommunicator(
        application=URLRouter(websocket_urlpatterns),
        path='ws/chat/lobby/Lobby2',
    )


@pytest.fixture
async def contact_communicator(contact: Contact) -> WebsocketCommunicator:
    return WebsocketCommunicator(
        application=URLRouter(websocket_urlpatterns),
        path=f'ws/chat/contact/{contact.id}',
    )


@pytest.fixture
async def notify_communicator(lobbies: Iterator[list[Lobby]], contact: Contact) -> WebsocketCommunicator:
    lobbies = [lobby.lobby_name for lobby in lobbies]
    lobbies.append(contact.id)  # added contact lobby
    
    return WebsocketCommunicator(
        application=URLRouter(websocket_urlpatterns),
        path='ws/notify/',
        headers=lobbies,
    )


async def test_connection(contact_communicator):
    communicator = await contact_communicator
    connected, _ = await communicator.connect()
    assert connected
    await communicator.disconnect()


async def test_receive_message(notify_communicator: WebsocketCommunicator,
                               contact_communicator: WebsocketCommunicator,
                               chat_communicator: WebsocketCommunicator):
    
    notify_communicator = await notify_communicator
    contact_communicator = await contact_communicator
    chat_communicator = await chat_communicator
    
    assert await notify_communicator.connect() == (True, None)
    assert await contact_communicator.connect() == (True, None)
    assert await chat_communicator.connect() == (True, None)

    await chat_communicator.send_json_to({
        'type': 'message',
        'message': 'Hello world_1',
        'username': 'TestUser',
    })

    await contact_communicator.send_json_to({
        'type': 'message',
        'message': 'Hello world_2',
        'username': 'TestUser',
    })

    receivers = [
        await notify_communicator.receive_json_from(),
        await notify_communicator.receive_json_from()
    ]
    number_sequence = [1, 2]
    
    responses = []
    expected_jsons = []
    
    messages = await database_sync_to_async(Message.objects.all)()
    messages_ids: list[Message] = await database_sync_to_async(lambda messages: [m.id for m in messages])(messages)
    
    for i, json in enumerate(receivers):
        expected_jsons.append({
            'type': 'chat_message',
            'message': f'Hello world_{number_sequence[i]}',
            'username': 'TestUser',
            'message_id': messages_ids[i],
            'timestamp': str(int(time()))[:8],
        })
        responses.append(
            tp_to_unaccurate(json)
        )
    
    for response in responses:
        assert response in expected_jsons
        i = expected_jsons.index(response)
        expected_jsons.pop(i)
    
    assert len(expected_jsons) == 0