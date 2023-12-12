from django.urls import path

from apps.accounts.api.views import UserRegister


urlpatterns = [
    path('', UserRegister.as_view())
]