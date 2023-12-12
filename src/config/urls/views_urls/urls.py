from django.urls import path, include


urlpatterns = [
    path('', include('apps.lobby.urls')),
    path('account/', include('apps.accounts.urls')),
    path('chat/', include('apps.chat.urls')),
]