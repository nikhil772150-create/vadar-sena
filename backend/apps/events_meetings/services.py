import logging
from apps.events_meetings.models import Event, EventRSVP, Meeting, MeetingInvitee, MeetingMinutes

logger = logging.getLogger(__name__)


class EventsMeetingsService:
    @staticmethod
    def rsvp_event(event: Event, user, rsvp_status='ATTENDING'):
        rsvp, created = EventRSVP.objects.update_or_create(
            event=event,
            user=user,
            defaults={'status': rsvp_status}
        )
        logger.info(f"[EVENT RSVP] User: {user.phone_number} | Event: {event.title} | Status: {rsvp_status}")
        return rsvp

    @staticmethod
    def add_meeting_minutes(meeting: Meeting, minutes_text, attachment_asset=None):
        minutes, _ = MeetingMinutes.objects.update_or_create(
            meeting=meeting,
            defaults={
                'minutes_text': minutes_text,
                'attachment_asset': attachment_asset
            }
        )
        logger.info(f"[MEETING MINUTES ADDED] Meeting ID: {meeting.id}")
        return minutes
