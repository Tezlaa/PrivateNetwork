from django.urls import path, include


urlpatterns = [
    path('chat/', include('apps.chat.urls')),
    path('api/v1/lobby/', include('apps.lobby.urls')),
]
