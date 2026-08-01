from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from apps.common.responses import success_response, error_response
from apps.common.permissions import IsAdminUserOrSuperAdmin
from apps.events_meetings.models import Event, EventRSVP, Meeting, MeetingMinutes, EventStatus
from apps.events_meetings.serializers import (
    EventSerializer,
    EventRSVPSerializer,
    MeetingSerializer,
    MeetingMinutesSerializer
)
from apps.events_meetings.services import EventsMeetingsService


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.filter(is_deleted=False).select_related('banner_asset', 'state', 'district')
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'is_public', 'is_featured', 'state', 'district']
    search_fields = ['title', 'description', 'venue_address']
    ordering_fields = ['start_time', 'created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        if self.action == 'rsvp':
            return [permissions.IsAuthenticated()]
        return [IsAdminUserOrSuperAdmin()]

    def get_queryset(self):
        qs = super().get_queryset()
        if not (self.request.user and self.request.user.is_authenticated and self.request.user.user_type in ['ADMIN', 'SUPERADMIN']):
            qs = qs.filter(is_public=True).exclude(status=EventStatus.CANCELLED)
        return qs

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def rsvp(self, request, pk=None):
        event = self.get_object()
        rsvp_status = request.data.get('status', 'ATTENDING')
        rsvp = EventsMeetingsService.rsvp_event(event, request.user, rsvp_status)
        return success_response(EventRSVPSerializer(rsvp).data, "RSVP updated successfully.")


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.filter(is_deleted=False).select_related('created_by', 'minutes')
    serializer_class = MeetingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['subject', 'agenda', 'venue_or_link']
    ordering_fields = ['meeting_date', 'created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsAdminUserOrSuperAdmin()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUserOrSuperAdmin])
    def add_minutes(self, request, pk=None):
        meeting = self.get_object()
        minutes_text = request.data.get('minutes_text')
        attachment_asset_id = request.data.get('attachment_asset')
        
        if not minutes_text:
            return error_response(None, "minutes_text is required.", status.HTTP_400_BAD_REQUEST)

        minutes = EventsMeetingsService.add_meeting_minutes(meeting, minutes_text, attachment_asset_id)
        return success_response(MeetingMinutesSerializer(minutes).data, "Meeting minutes added successfully.")
