from datetime import datetime

import pytest

from apps.lobby.models import Lobby
from apps.chat.services.model_services import send_message, send_message_by_username
from apps.chat.services.action_services.lobby_action import LobbyAction
from apps.chat.services.utils import get_path_for_file_message, get_path_for_voice_message
from apps.chat.models import Message
from apps.chat.tests.utils import delete_temp_files_from_message_instance
from apps.chat.services.action_services.schemas import (
    MessageLikeRequest, MessageSendResponce, MessageSendRequest,
    ReplyMessage, FileMessageType, FileUrl, UserAsUsername
)
from config.testing.api import APIClient


pytestmark = [
    pytest.mark.django_db,
    pytest.mark.freeze_time('2023-01-01 15:00:00+00:00')
]


def test_send_message_class(as_user: APIClient, lobby: Lobby, bytearray_voice, bytearray_file):   
    voice = FileMessageType(
        file=bytearray_voice,
        file_name='test_sound.mp3'
    )
    file = FileMessageType(
        file=bytearray_file,
        file_name='test_image.png'
    )
    test_data_send = {
        'user': as_user.user,
        'text': 'Test Message',
        'voice_record': voice,
        'reply_message': ReplyMessage(1),
        'files': [file]
    }
    
    message = MessageSendRequest(**test_data_send)
    
    action = LobbyAction(lobby)
    sending_message = action.send_message(message)

    expected_dataclass = MessageSendResponce(
        user=UserAsUsername(username='TestUser'),
        text='Test Message',
        message_id=1,
        voice_record=FileUrl(url='/media/voice_messages/TestUser/test_sound.mp3'),
        reply_message=ReplyMessage(id=1),
        files=[
            FileUrl(url=f'/media/files/{datetime.now().strftime("%m.%d.%Y")}/test_image.png')
        ],
        timestamp=int(round(Message.objects.first().created_at.timestamp()))
    )
    
    assert sending_message == expected_dataclass
    
    assert Message.objects.count() == 1

    delete_temp_files_from_message_instance()


def test_decode_json(as_user: APIClient, lobby: Lobby, bytearray_voice, bytearray_file):
    action = LobbyAction(lobby)
    test_data_send = {
        'user': as_user.user,
        'text': 'Test Message',
        'voice_record': action.encode_to_base64_utf8(FileMessageType(file=bytearray_voice, file_name='test_sound.mp3')),
        'reply_message': {'id': 1},
        'files': [action.encode_to_base64_utf8(FileMessageType(file=bytearray_file, file_name='test_image.png'))]
    }
    
    expected_typed_message = {
        'user': as_user.user,
        'text': 'Test Message',
        'voice_record': FileMessageType(file=bytearray_voice, file_name='test_sound.mp3'),
        'reply_message': ReplyMessage(1),
        'files': [
            FileMessageType(file=bytearray_file, file_name='test_image.png'),
        ]
    }
    
    assert action.decode_json(test_data_send, MessageSendRequest) == MessageSendRequest(**expected_typed_message)
    
    expected_typed_message.pop('reply_message')
    test_data_send.pop('reply_message')
    assert action.decode_json(test_data_send, MessageSendRequest) == MessageSendRequest(**expected_typed_message)
    
    expected_typed_message.pop('files')
    test_data_send.pop('files')
    assert action.decode_json(test_data_send, MessageSendRequest) == MessageSendRequest(**expected_typed_message)

    expected_typed_message.pop('voice_record')
    test_data_send.pop('voice_record')
    assert action.decode_json(test_data_send, MessageSendRequest) == MessageSendRequest(**expected_typed_message)


def test_like_service(as_user: APIClient, lobby: Lobby):
    action = LobbyAction(lobby)
    message = action.send_message(MessageSendRequest(user=as_user.user, text='Test Message'))
    action.like_message(
        MessageLikeRequest(
            user=as_user.user,
            message_id=message.message_id,
            status=True
        )
    )
    assert Message.objects.get(id=message.message_id).user_liked.all().count() == 1
    assert Message.objects.get(id=message.message_id, user_liked__in=[as_user.user])
    
    action.like_message(
        MessageLikeRequest(
            user=as_user.user,
            message_id=message.message_id,
            status=False
        )
    )

    assert Message.objects.get(id=message.message_id).user_liked.all().count() == 0


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