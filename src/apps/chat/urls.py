from django.urls import path

from apps.chat.views import ChatView


urlpatterns = [
    path('chat/<str:lobby_name>/', ChatView.as_view(), name='chat'),
]