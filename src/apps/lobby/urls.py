from django.urls import path, include

from apps.lobby.views import LobbyMenu


urlpatterns = [
    path('', LobbyMenu.as_view(), name='lobbies')
]