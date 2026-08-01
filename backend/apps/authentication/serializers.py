from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.common.validators import validate_indian_phone_number

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User detail response serializer."""
    class Meta:
        model = User
        fields = ('id', 'uuid', 'phone_number', 'email', 'user_type', 'is_active', 'date_joined')
        read_only_fields = fields


class LoginSerializer(serializers.Serializer):
    """Password-based login serializer."""
    phone_number = serializers.CharField(validators=[validate_indian_phone_number])
    password = serializers.CharField(write_only=True)


class OTPRequestSerializer(serializers.Serializer):
    """OTP dispatch request serializer."""
    phone_number = serializers.CharField(validators=[validate_indian_phone_number])
    purpose = serializers.ChoiceField(choices=['LOGIN', 'REGISTER', 'RESET_PASSWORD'], default='LOGIN')


class OTPVerifySerializer(serializers.Serializer):
    """OTP verification serializer."""
    phone_number = serializers.CharField(validators=[validate_indian_phone_number])
    otp_code = serializers.CharField(max_length=6, min_length=6)
