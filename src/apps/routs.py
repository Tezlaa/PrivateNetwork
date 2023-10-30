from django.urls import path, include


urlpatterns = [
    path('chat/', include('apps.chat.urls')),
]
