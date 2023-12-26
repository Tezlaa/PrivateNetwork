from django.urls import path

from apps.contact.api.views import RetrieveAndListContact


urlpatterns = [
    path('', RetrieveAndListContact.as_view())
]