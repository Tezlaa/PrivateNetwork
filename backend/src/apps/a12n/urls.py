from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenBlacklistView
)

from apps.a12n.views import ObtainAuthStatus


urlpatterns = [
    path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view()),
    path('status/', ObtainAuthStatus.as_view())
]