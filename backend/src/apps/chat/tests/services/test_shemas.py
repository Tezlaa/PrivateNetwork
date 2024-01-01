from dataclasses import asdict

import base64
from time import time


import pytest


from config.testing.api import APIClient

from apps.chat.services.schemas import (
    MessageReceiveType, MessageSendType,
    ReplyMessage, FileMessageType
)


pytestmark = [
    pytest.mark.django_db
]


def test_shemas_message_sending_and_receive(as_user: APIClient):
    bytearray_voice = bytearray(open('apps/chat/tests/files/test_sound.mp3', 'rb').read())
    bytearray_file = bytearray(open('apps/chat/tests/files/test_image.png', 'rb').read())
    timestamp = str(time())
    
    voice = FileMessageType(
        file=bytearray_voice,
        file_name='test_sound'
    )
    
    file = FileMessageType(
        file=bytearray_file,
        file_name='test_image'
    )
    
    test_data_send = {
        'user': as_user.user,
        'text': 'Test Message',
        'voice_record': voice,
        'reply_message': ReplyMessage(1),
        'files': [file]
    }
    
    test_data_receive = {
        'user': as_user.user,
        'text': 'Test Message',
        'voice_record': voice,
        'reply_message': ReplyMessage(1),
        'files': [file],
        'timestamp': timestamp,
    }

    message_send = MessageSendType(**test_data_send)
    message_receive = MessageReceiveType(**test_data_receive)

    expected_json_send = {
        'user': as_user.user,
        'text': 'Test Message',
        'voice_record': {
            'file': bytearray_voice,
            'file_name': 'test_sound',
            'sign': None,
        },
        'reply_message': {'id': 1},
        'files': [{
            'file': bytearray_file,
            'file_name': 'test_image',
            'sign': None,
        }]
    }
    
    expected_json_receive = {
        **expected_json_send,
        'timestamp': timestamp
    }
    
    assert expected_json_send == asdict(message_send)
    assert expected_json_receive == asdict(message_receive)