from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshSlidingView
)


urlpatterns = [
    path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshSlidingView.as_view(), name='token_refresh')
]