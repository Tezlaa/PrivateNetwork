from django.urls import path

from apps.lobby.views import CreateLobby


urlpatterns = [
    path('', CreateLobby.as_view())
    # path('<str:lobby_name>/', LobbyActions.as_view()),
    # path('', )
    # path('', )
]