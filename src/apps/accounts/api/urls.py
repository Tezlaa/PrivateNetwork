from django.urls import path

from apps.accounts.api.views import (
    ObtainUserInfo, UserRegister
)


urlpatterns = [
    path('register/', UserRegister.as_view()),
    path('me/', ObtainUserInfo.as_view()),
]