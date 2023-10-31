from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from apps.account.views import SingUp


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('sign-up/', SingUp.as_view(), name='sign-up'),
]