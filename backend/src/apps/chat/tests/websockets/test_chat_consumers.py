import base64

from datetime import datetime

from time import time

import pytest
from pytest_lazyfixture import lazy_fixture

from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from channels.db import database_sync_to_async

from apps.chat.models import Message
from apps.chat.permission.authentication import WSJWTAuthentication
from apps.chat.services.action_services.lobby_action import AsyncLobbyAction
from apps.chat.services.action_services.schemas import MessageSendRequest
from apps.chat.tests.utils import (
    tp_to_unaccurate, get_access_token, delete_temp_files_from_message_instance
)
from apps.chat.services.model_services import (
    send_message_by_username, like_for_message,
)
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
        },
    )


@pytest.fixture
async def communicator_chat_contact(as_user: APIClient,
                                    contact: Contact) -> WebsocketCommunicator:
    return WebsocketCommunicator(
        application=URLRouter(websocket_urlpatterns),
        path=f'ws/chat/contact/{contact.id}',
        headers={
            WSJWTAuthentication.AUTH_HEADER_NAME_WEBSOCKET: get_access_token(as_user.user),
        },
    )


@pytest.mark.parametrize(
    'communicator', (
        lazy_fixture('communicator_chat_lobby'),
        lazy_fixture('communicator_chat_contact')
    )
)
async def test_connection(communicator: WebsocketCommunicator):
    communicator = await communicator
    connected, _ = await communicator.connect(2)
    assert connected
    await communicator.disconnect()


@pytest.mark.parametrize(
    'connected_communicator, message_id', (
        (lazy_fixture('communicator_chat_lobby'), 1),
        (lazy_fixture('communicator_chat_contact'), 2)
    )
)
async def test_send_and_receive_message(connected_communicator: WebsocketCommunicator, message_id,
                                        bytearray_voice, bytearray_file):
    communicator = await connected_communicator
    await communicator.connect()
    
    base64_voice = base64.b64encode(bytearray_voice).decode('utf-8')
    base64_file = base64.b64encode(bytearray_file).decode('utf-8')
    
    await communicator.send_json_to({
        'type': 'message',
        'text': 'Test Message',
        'reply_message': None,
        'voice_record': {'file': base64_voice, 'file_name': 'test_sound.mp3'},
        'files': [{'file': base64_file, 'file_name': 'test_image.png'}]
    })
    response = await communicator.receive_json_from()
    message = await database_sync_to_async(Message.objects.first)()
    expected_receive_json = {
        'type': 'chat_message',
        'user': {'username': 'TestUser'},
        'text': 'Test Message',
        'message_id': message_id,
        'reply_message': None,
        'voice_record': {'url': '/media/voice_messages/TestUser/test_sound.mp3'},
        'files': [{'url': f'/media/files/{datetime.now().strftime("%m.%d.%Y")}/test_image.png'}],
        'timestamp': int(round(message.created_at.timestamp()))
    }
    assert expected_receive_json == response
    
    messages_count = await database_sync_to_async(Message.objects.all().count)()
    assert messages_count == 1
    
    await database_sync_to_async(delete_temp_files_from_message_instance)()
    
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
        'message_id': message.pk,
        'status': True
    })
    
    expected_message = {
        'type': 'chat_like',
        'message_id': message.pk,
        'user': {'username': 'TestUser'},
        'status': True,
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
        'type': 'like',
        'message_id': message.pk,
        'status': False
    })
    
    expected_message = {
        'type': 'chat_like',
        'message_id': message.pk,
        'user': {'username': 'TestUser'},
        'status': False,
    }
    response = await communicator.receive_json_from()
    
    assert response == expected_message
    
    assert await database_sync_to_async(message.user_liked.count)() == 0
    
    await communicator.disconnect()