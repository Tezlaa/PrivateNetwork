from django.urls import path, include

from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('chat/', include('apps.chat.urls')),
    path('', include('apps.lobby.urls')),
    path('account/', include('apps.account.urls')),
]


urlpatterns = format_suffix_patterns(urlpatterns)