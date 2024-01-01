import os
import time
import shutil

import pytest

from apps.lobby.models import Lobby
from apps.chat.services.model_services import send_message, send_message_by_username
from apps.chat.services.message import LobbyAction
from apps.chat.services.utils import get_path_for_file_message, get_path_for_voice_message
from apps.chat.models import Message
from apps.chat.services.schemas import (
    MessageReceiveType, MessageSendType,
    ReplyMessage, FileMessageType
)


from config.testing.api import APIClient


pytestmark = [
    pytest.mark.django_db,
    pytest.mark.freeze_time('2023-01-01 15:00:00+00:00')
]


def test_send_message_class(as_user: APIClient, lobby: Lobby):
    with open('apps/chat/tests/files/test_sound.mp3', 'rb') as f:
        bytearray_voice = f.read()
    
    with open('apps/chat/tests/files/test_image.png', 'rb') as f:
        bytearray_file = f.read()
    
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
    
    message = MessageSendType(**test_data_send)
    
    action = LobbyAction(lobby)
    message_instance = action.send_message(message)
    assert (
        get_path_for_voice_message(
            message_instance, voice.file_name
        ) == action.get_madia_path(message_instance.voice_record)
    )

    file_path = message_instance.files.first().file
    
    assert (
        get_path_for_file_message(
            message_instance, file.file_name
        ) == file_path
    )

    message_instance.files.first().file.delete()
    message_instance.voice_record.delete()


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