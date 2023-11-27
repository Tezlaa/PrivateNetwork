from django.urls import path, include


urlpatterns = [
    path('chat/', include('apps.chat.urls')),
    path('lobby/', include('apps.lobby.urls')),
    path('account/', include('apps.account.urls')),
]
