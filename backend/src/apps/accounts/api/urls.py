from django.urls import path

from apps.accounts.api.views import (
    ObtainUserInfo, UserRegister, UpdateUserInfo
)


urlpatterns = [
    path('register/', UserRegister.as_view()),
    path('me/', ObtainUserInfo.as_view()),
    path('update/', UpdateUserInfo.as_view()),
]