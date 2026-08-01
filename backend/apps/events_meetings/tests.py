from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from apps.common.enums import UserType
from apps.events_meetings.models import Event, EventRSVP, Meeting, MeetingStatus
from apps.events_meetings.services import EventsMeetingsService

User = get_user_model()


class EventsMeetingsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone_number="9876543210", password="password123")
        self.admin = User.objects.create_user(phone_number="9999988888", password="password123", user_type=UserType.ADMIN)
        self.event = Event.objects.create(
            title="Grand Youth Rally",
            description="Statewide rally",
            venue_address="Central Ground, Pune",
            start_time=timezone.now() + timedelta(days=5),
            status="UPCOMING",
            is_public=True
        )
        self.client = APIClient()

    def test_public_event_list(self):
        response = self.client.get('/api/v1/events-meetings/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_event_rsvp_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/api/v1/events-meetings/events/{self.event.id}/rsvp/', {'status': 'ATTENDING'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(EventRSVP.objects.count(), 1)

    def test_meeting_creation_and_minutes(self):
        meeting = Meeting.objects.create(
            subject="Executive Committee Meeting",
            agenda="Q3 Strategy",
            meeting_date=timezone.now() + timedelta(days=2),
            venue_or_link="HQ Conference Room",
            created_by=self.admin
        )
        minutes = EventsMeetingsService.add_meeting_minutes(meeting, "Decided to expand youth wing.")
        self.assertEqual(meeting.minutes.minutes_text, "Decided to expand youth wing.")
