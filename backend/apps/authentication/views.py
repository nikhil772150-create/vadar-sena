from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView as SimpleJWTTokenRefreshView
from django.contrib.auth import get_user_model, authenticate

from apps.common.responses import success_response, error_response
from apps.authentication.serializers import (
    UserSerializer,
    LoginSerializer,
    OTPRequestSerializer,
    OTPVerifySerializer
)
from apps.authentication.services import OTPService

User = get_user_model()


class LoginView(APIView):
    """
    POST /api/v1/auth/login/
    Password authentication returning JWT tokens.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer.errors, "Invalid login credentials", status.HTTP_400_BAD_REQUEST)

        phone_number = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']

        user = authenticate(username=phone_number, password=password)
        if not user:
            return error_response(None, "Invalid phone number or password", status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return error_response(None, "Account is disabled", status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)

        return success_response({
            "user": UserSerializer(user).data,
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        }, "Login successful")


class OTPRequestView(APIView):
    """
    POST /api/v1/auth/send-otp/
    Dispatches a 6-digit OTP code to specified phone number.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer.errors, "Validation error", status.HTTP_400_BAD_REQUEST)

        phone_number = serializer.validated_data['phone_number']
        purpose = serializer.validated_data['purpose']

        result = OTPService.send_otp(phone_number, purpose)
        return success_response(result, "OTP sent successfully")


class OTPVerifyView(APIView):
    """
    POST /api/v1/auth/verify-otp/
    Verifies 6-digit OTP code and returns JWT token (or creates account if registering).
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer.errors, "Validation error", status.HTTP_400_BAD_REQUEST)

        phone_number = serializer.validated_data['phone_number']
        otp_code = serializer.validated_data['otp_code']

        if not OTPService.verify_otp(phone_number, otp_code):
            return error_response(None, "Invalid or expired OTP code", status.HTTP_400_BAD_REQUEST)

        # Get or create user
        user, created = User.objects.get_or_create(
            phone_number=phone_number,
            defaults={'is_active': True}
        )

        refresh = RefreshToken.for_user(user)

        return success_response({
            "is_new_user": created,
            "user": UserSerializer(user).data,
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        }, "OTP verified successfully")


class TokenRefreshView(SimpleJWTTokenRefreshView):
    """
    POST /api/v1/auth/token/refresh/
    Exchanges refresh token for new access token.
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return success_response(response.data, "Token refreshed successfully")
        return response


class UserProfileView(APIView):
    """
    GET /api/v1/auth/me/
    Returns current authenticated user details.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return success_response(UserSerializer(request.user).data, "User profile retrieved")
