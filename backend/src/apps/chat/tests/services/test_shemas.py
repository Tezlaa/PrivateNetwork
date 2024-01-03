from dataclasses import asdict

from time import time


import pytest


from config.testing.api import APIClient

from apps.chat.services.action_services.schemas import (
    FileUrl, MessageSendResponce, MessageSendRequest,
    ReplyMessage, FileMessageType, UserAsUsername
)


pytestmark = [
    pytest.mark.django_db
]


def test_shemas_message_sending_and_receive(as_user: APIClient):
    with open('apps/chat/tests/files/test_sound.mp3', 'rb') as f:
        bytearray_voice = f.read()
    
    with open('apps/chat/tests/files/test_image.png', 'rb') as f:
        bytearray_file = f.read()
    
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
    
    test_sending_data = {
        'user': UserAsUsername(username='TestUser'),
        'text': 'Test Message',
        'message_id': 1,
        'voice_record': FileUrl(url='test_url/url.mp3'),
        'reply_message': ReplyMessage(1),
        'files': [FileUrl(url='test_url/url.png')],
        'timestamp': timestamp,
    }

    message_send = MessageSendRequest(**test_data_send)
    message_sending = MessageSendResponce(**test_sending_data)

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
    
    expected_json_sending = {
        'user': {'username': 'TestUser'},
        'text': 'Test Message',
        'message_id': 1,
        'voice_record': {
            'url': 'test_url/url.mp3',
        },
        'reply_message': {'id': 1},
        'files': [{
            'url': 'test_url/url.png',
        }],
        'timestamp': timestamp,
    }
    
    assert expected_json_send == asdict(message_send)
    assert expected_json_sending == asdict(message_sending)
    