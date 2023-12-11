from django.urls import path

from apps.account.api.views import UserRegister


urlpatterns = [
    path('', UserRegister.as_view())
]