from rest_framework import serializers
from apps.events_meetings.models import Event, EventRSVP, Meeting, MeetingInvitee, MeetingMinutes


class EventSerializer(serializers.ModelSerializer):
    banner_url = serializers.SerializerMethodField()
    rsvps_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = (
            'id', 'uuid', 'title', 'description', 'venue_address', 'map_link',
            'start_time', 'end_time', 'banner_asset', 'banner_url', 'status',
            'is_public', 'is_featured', 'state', 'district', 'rsvps_count', 'created_at'
        )
        read_only_fields = ('id', 'uuid', 'created_at')

    def get_banner_url(self, obj):
        if obj.banner_asset and obj.banner_asset.file:
            return obj.banner_asset.file.url
        return None

    def get_rsvps_count(self, obj):
        return obj.rsvps.filter(status='ATTENDING').count()


class EventRSVPSerializer(serializers.ModelSerializer):
    user_phone = serializers.CharField(source='user.phone_number', read_only=True)

    class Meta:
        model = EventRSVP
        fields = ('id', 'event', 'user', 'user_phone', 'status', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')


class MeetingMinutesSerializer(serializers.ModelSerializer):
    attachment_url = serializers.SerializerMethodField()

    class Meta:
        model = MeetingMinutes
        fields = ('id', 'minutes_text', 'attachment_asset', 'attachment_url', 'created_at')

    def get_attachment_url(self, obj):
        if obj.attachment_asset and obj.attachment_asset.file:
            return obj.attachment_asset.file.url
        return None


class MeetingSerializer(serializers.ModelSerializer):
    minutes = MeetingMinutesSerializer(read_only=True)
    created_by_phone = serializers.CharField(source='created_by.phone_number', read_only=True)

    class Meta:
        model = Meeting
        fields = (
            'id', 'uuid', 'subject', 'agenda', 'meeting_date', 'venue_or_link',
            'status', 'created_by', 'created_by_phone', 'minutes', 'created_at'
        )
        read_only_fields = ('id', 'uuid', 'created_by', 'created_at')
