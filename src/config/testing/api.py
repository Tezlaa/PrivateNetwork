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
    
    def get(self, *args, expected_status_code=200, **kwargs):
        response = super().get(*args, **kwargs)

        assert response.status_code == expected_status_code
        return response.json()
    
    def _create_user(self, user: User):
        self.user = user
        self.password = "".join([random.choice(string.hexdigits) for _ in range(6)])
        self.user.set_password(self.password)
        self.user.save()