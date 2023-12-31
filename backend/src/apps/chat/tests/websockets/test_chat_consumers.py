from time import time

import pytest
from pytest_lazyfixture import lazy_fixture

from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from channels.db import database_sync_to_async

from apps.chat.permission.authentication import WSJWTAuthentication
from apps.chat.tests.utils import tp_to_unaccurate, get_access_token
from apps.chat.services.model_services import send_message_by_username, like_for_message
from apps.chat.routing import websocket_urlpatterns
from apps.contact.models import Contact
from apps.lobby.models import Lobby
from config.testing.api import APIClient


pytestmark = [
    pytest.mark.django_db(transaction=True),
    pytest.mark.asyncio,
    pytest.mark.freeze_time('2023-01-01 15:00:00+00:00')
]


@pytest.fixture
async def communicator_chat_lobby(as_user: APIClient) -> WebsocketCommunicator:
    return WebsocketCommunicator(
        application=URLRouter(websocket_urlpatterns),
        path='ws/chat/lobby/TestLobby',
        headers={
            WSJWTAuthentication.AUTH_HEADER_NAME_WEBSOCKET: get_access_token(as_user.user),
        }
    )


@pytest.fixture
async def communicator_chat_contact(as_user: APIClient,
                                    contact: Contact) -> WebsocketCommunicator:
    return WebsocketCommunicator(
        application=URLRouter(websocket_urlpatterns),
        path=f'ws/chat/contact/{contact.id}',
        headers={
            WSJWTAuthentication.AUTH_HEADER_NAME_WEBSOCKET: get_access_token(as_user.user),
        }
    )


@pytest.mark.parametrize(
    'communicator', (lazy_fixture('communicator_chat_lobby'),
                     lazy_fixture('communicator_chat_contact'))
)
async def test_connection(communicator: WebsocketCommunicator):
    communicator = await communicator
    connected, _ = await communicator.connect()
    assert connected
    await communicator.disconnect()


@pytest.mark.parametrize(
    'connected_communicator, message_id', (
        (lazy_fixture('communicator_chat_lobby'), 1),
        (lazy_fixture('communicator_chat_contact'), 2)
    )
)
async def test_send_and_receive_message(connected_communicator: WebsocketCommunicator, message_id: int):
    communicator = await connected_communicator
    await communicator.connect()
    
    await communicator.send_json_to({
        'type': 'message',
        'message': 'Hello world',
        'username': 'TestUser',
    })

    expected_message = {
        'type': 'chat_message',
        'message': 'Hello world',
        'username': 'TestUser',
        'message_id': message_id,
        'timestamp': int(time())
    }
    
    response = await communicator.receive_json_from()
    assert (
        tp_to_unaccurate(response) == tp_to_unaccurate(expected_message)
    )

    messages_count = await database_sync_to_async(Lobby.objects.all().count)()
    assert messages_count == 1
    
    await communicator.disconnect()


@pytest.mark.parametrize(
    'connected_communicator, instance_lobby', [
        (lazy_fixture('communicator_chat_lobby'), lazy_fixture('lobby')),
        (lazy_fixture('communicator_chat_contact'), lazy_fixture('contact'))
    ]
)
async def test_send_and_receive_like(connected_communicator: WebsocketCommunicator, instance_lobby: Lobby | Contact):
    communicator = await connected_communicator
    await communicator.connect()
    
    message = await database_sync_to_async(send_message_by_username)(instance_lobby, 'Hello world', 'TestUser')
    
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
    
    await communicator.disconnect()


@pytest.mark.parametrize(
    'connected_communicator, instance_lobby', [
        (lazy_fixture('communicator_chat_lobby'), lazy_fixture('lobby')),
        (lazy_fixture('communicator_chat_contact'), lazy_fixture('contact'))
    ]
)
async def test_delete_like(connected_communicator: WebsocketCommunicator, instance_lobby: Lobby | Contact):
    communicator = await connected_communicator
    await communicator.connect()
    
    message = await database_sync_to_async(send_message_by_username)(instance_lobby, 'Hello world', 'TestUser')
    await database_sync_to_async(like_for_message)(instance_lobby, message.pk, 'TestUser')
    
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

    await communicator.disconnect()
