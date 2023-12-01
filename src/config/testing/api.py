import random
import string

from typing import Optional

from django.contrib.auth.models import User

from rest_framework.test import APIClient as DRFAPIClient


class APIClient(DRFAPIClient):
    def __init__(self, user: Optional[User] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if user:
            self._create_user(user)
            super().force_authenticate(user=self.user)
    
    def get(self, *args, expected_status_code=200, **kwargs) -> dict:
        return self._request('get', expected_status_code, *args, **kwargs)

    def post(self, *args, expected_status_code=201, **kwargs) -> dict:
        return self._request('post', expected_status_code, *args, **kwargs)
    
    def delete(self, *args, expected_status_code=200, **kwargs) -> dict:
        return self._request('delete', expected_status_code, *args, **kwargs)
    
    def _request(self, method: str, expected_status_code: int, *args, **kwargs) -> dict:
        request_method = getattr(super(), method)
        response = request_method(*args, **kwargs)
        assert response.status_code == expected_status_code
        return response.json()
    
    def _create_user(self, user: User):
        self.user = user
        self.password = "".join([random.choice(string.hexdigits) for _ in range(6)])
        self.user.set_password(self.password)
        self.user.save()
        