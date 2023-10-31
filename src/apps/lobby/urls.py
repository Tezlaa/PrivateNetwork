from django.urls import path

from apps.lobby.api import GetLobbies, CreateLobby, ConnectDisconnectFromLobby, GetLobbiesNames
from apps.lobby.views import LobbyMenu


API_PREFIX_V1 = 'api/v1/'


urlpatterns = [
    path(API_PREFIX_V1 + 'all/', GetLobbies.as_view()),
    path(API_PREFIX_V1 + 'allNames/', GetLobbiesNames.as_view()),
    path(API_PREFIX_V1 + 'create/', CreateLobby.as_view()),
    path(API_PREFIX_V1 + '<str:lobby_name>/', ConnectDisconnectFromLobby.as_view()),
    path('', LobbyMenu.as_view(), name='menu')
]