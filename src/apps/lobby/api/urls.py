from django.urls import path

from apps.lobby.api.views import (
    GetLobbies, CreateLobby, ConnectDisconnectFromLobby,
    GetLobbiesNames, DeleteLobby, GetLobby
)


urlpatterns = [
    path('all/', GetLobbies.as_view()),
    path('getLobby/<str:lobby_name>', GetLobby.as_view()),
    path('allNames/', GetLobbiesNames.as_view()),
    path('create/', CreateLobby.as_view()),
    path('action/<str:lobby_name>', ConnectDisconnectFromLobby.as_view()),
    path('delete/<str:lobby_name>', DeleteLobby.as_view()),
]