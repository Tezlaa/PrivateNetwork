import pytest


@pytest.fixture
def bytearray_voice():
    with open('apps/chat/tests/files/test_sound.mp3', 'rb') as f:
        return f.read()
    

@pytest.fixture
def bytearray_file():
    with open('apps/chat/tests/files/test_image.png', 'rb') as f:
        return f.read()