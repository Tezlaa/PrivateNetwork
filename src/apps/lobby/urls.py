from django.urls import path

from apps.lobby.views import GetLobbies, CreateLobby, ConnectDisconnectFromLobby, GetLobbiesNames


urlpatterns = [
    path('all/', GetLobbies.as_view()),
    path('allNames/', GetLobbiesNames.as_view()),
    path('create/', CreateLobby.as_view()),
    path('<str:lobby_name>/', ConnectDisconnectFromLobby.as_view()),
]