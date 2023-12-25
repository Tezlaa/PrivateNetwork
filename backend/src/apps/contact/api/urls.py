from django.urls import path

from apps.contact.api.views import CreateContact


urlpatterns = [
    path('', CreateContact.as_view())
]