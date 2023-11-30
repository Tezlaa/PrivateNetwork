from django.urls import path, include


urlpatterns = [
    path('', include('apps.lobby.urls')),
    path('account/', include('apps.account.urls')),
    path('chat/', include('apps.chat.urls')),
]