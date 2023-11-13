from django.urls import path, include


urlpatterns = [
    path('chat/', include('apps.chat.urls')),
    path('', include('apps.lobby.urls')),
    path('account/', include('apps.account.urls')),
]
