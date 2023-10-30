from django.urls import path

from apps.lobby.views import LobbyReceiveCreate, LobbyActions


urlpatterns = [
    path('', LobbyReceiveCreate.as_view()),
    path('<str:lobby_name>/', LobbyActions.as_view()),
    # path('', )
    # path('', )
]