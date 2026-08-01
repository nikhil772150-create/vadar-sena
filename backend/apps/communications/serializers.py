from rest_framework import serializers
from apps.common.validators import validate_indian_phone_number
from apps.communications.models import ContactInquiry, Notification


class ContactInquirySerializer(serializers.ModelSerializer):
    phone = serializers.CharField(validators=[validate_indian_phone_number])

    class Meta:
        model = ContactInquiry
        fields = ('id', 'uuid', 'name', 'phone', 'email', 'subject', 'message', 'status', 'created_at')
        read_only_fields = ('id', 'uuid', 'status', 'created_at')


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'title', 'message', 'link_url', 'channel', 'is_read', 'created_at')
        read_only_fields = ('id', 'created_at')
