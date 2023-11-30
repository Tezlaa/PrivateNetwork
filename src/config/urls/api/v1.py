from django.urls import path, include


urlpatterns = [
    path('lobby/', include('apps.lobby.api_urls')),
]