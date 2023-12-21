from django.urls import path

from apps.lobby.views import LobbyMenu


urlpatterns = [
    path('', LobbyMenu.as_view(), name='lobbies')
]