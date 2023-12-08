import json
import random
import string

from typing import Optional

from django.contrib.auth.models import User

from rest_framework.test import APIClient as DRFAPIClient
from rest_framework.response import Response


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
    
    def _request(self, method: str,
                 expected_status_code: int,
                 *args, **kwargs) -> dict:
        request_method = getattr(super(), method)
        response: Response = request_method(*args, **kwargs)
        
        content = self._decode(response)
        assert response.status_code == expected_status_code
        return content
    
    def _create_user(self, user: User):
        self.user = user
        self.password = "".join([random.choice(string.hexdigits) for _ in range(6)])
        self.user.set_password(self.password)
        self.user.save()
    
    def _decode(self, response: Response):
        if response.status_code == 204:
            return {}
        
        content = response.content.decode("utf-8", errors="ignore")
        
        if self.is_json(response):
            return json.loads(content)
        else:
            return content
    
    @staticmethod
    def is_json(response: Response):
        if response.has_header('content-type'):
            return 'json' in response.get('content-type')
        
        return False