from django.urls import path

from apps.chat.views import index


urlpatterns = [
    path('', index, name='index')
    # path('', )
    # path('', )
    # path('', )
]