from django.urls import path, include


urlpatterns = [
    path('lobby/', include('apps.lobby.api.urls')),
    path('register/', include('apps.accounts.api.urls')),
    path('token/', include('apps.a12n.urls')),
]