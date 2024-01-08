import os

import pytest

from django.conf import settings

from apps.accounts.models import User

from config.testing.api import APIClient


pytestmark = [pytest.mark.django_db]


def test_register(as_user: APIClient):
    register_data = {
        'username': 'TestUser1',
        'password': 'rootrootroot'
    }
    result = as_user.post('/api/v1/account/register/', register_data)
    expected_json = {
        'username': 'TestUser1',
        'avatar': None,
    }
    assert result == expected_json
    assert User.objects.filter(username='TestUser1').count() == 1


def test_obtaining_info_about_user(as_user: APIClient):
    result = as_user.get('/api/v1/account/me/')
    expected_json = {
        'username': 'TestUser',
        'avatar': None,
    }
    assert result == expected_json


def test_download_avatart(as_user: APIClient):
    file_name = 'test_img.png'
    test_pictures_path = 'apps/accounts/tests/files/{}'.format(file_name)
    
    data = {
        'avatar': (file_name, open(test_pictures_path, 'rb'))
    }
    
    result = as_user.patch(
        '/api/v1/account/update/',
        data=data,
    )

    assert result.get('avatar') is not None, "Avatar update failed"
    result['avatar'] = result['avatar'].split('/media/avatars/')[1]
    assert result == {
        'username': as_user.username,
        'avatar': f'{as_user.username}/{file_name}'
    }
    os.remove(os.path.join(settings.MEDIA_ROOT, f'avatars\\{as_user.username}\\{file_name}'))