from django.urls import path
from apps.authentication.views import (
    LoginView,
    OTPRequestView,
    OTPVerifyView,
    TokenRefreshView,
    UserProfileView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth-login'),
    path('send-otp/', OTPRequestView.as_view(), name='auth-send-otp'),
    path('verify-otp/', OTPVerifyView.as_view(), name='auth-verify-otp'),
    path('token/refresh/', TokenRefreshView.as_view(), name='auth-token-refresh'),
    path('me/', UserProfileView.as_view(), name='auth-me'),
]
