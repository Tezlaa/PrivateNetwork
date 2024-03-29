from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from apps.accounts.views import SingUp, Profile


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('sign-up/', SingUp.as_view(), name='sign-up'),
    path('', Profile.as_view(), name='profile')
]