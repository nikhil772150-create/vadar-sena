from django.db import models
from django.conf import settings
from apps.common.models import BaseModel, MediaAsset
from apps.organization.models import State, District, Taluka, Village


class EventStatus(models.TextChoices):
    UPCOMING = 'UPCOMING', 'Upcoming'
    COMPLETED = 'COMPLETED', 'Completed'
    CANCELLED = 'CANCELLED', 'Cancelled'


class MeetingStatus(models.TextChoices):
    SCHEDULED = 'SCHEDULED', 'Scheduled'
    COMPLETED = 'COMPLETED', 'Completed'
    CANCELLED = 'CANCELLED', 'Cancelled'


class RSVPStatus(models.TextChoices):
    ATTENDING = 'ATTENDING', 'Attending'
    MAYBE = 'MAYBE', 'Maybe'
    DECLINED = 'DECLINED', 'Declined'


class Event(BaseModel):
    """Public events, rallies, and programs (events_event)."""
    title = models.CharField(max_length=255)
    description = models.TextField()
    venue_address = models.TextField()
    map_link = models.URLField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    banner_asset = models.ForeignKey(MediaAsset, on_delete=models.SET_NULL, null=True, blank=True, related_name='event_banners')
    status = models.CharField(max_length=20, choices=EventStatus.choices, default=EventStatus.UPCOMING, db_index=True)
    is_public = models.BooleanField(default=True, help_text="Show on public website")
    is_featured = models.BooleanField(default=False)

    # Scoping
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')

    class Meta:
        db_table = 'events_event'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['-start_time']

    def __str__(self):
        return self.title


class EventRSVP(models.Model):
    """Member RSVP indication for Events (events_rsvp)."""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_rsvps')
    status = models.CharField(max_length=20, choices=RSVPStatus.choices, default=RSVPStatus.ATTENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'events_rsvp'
        unique_together = [['event', 'user']]

    def __str__(self):
        return f"{self.user} - {self.event.title} ({self.status})"


class Meeting(BaseModel):
    """Internal organizational and committee meetings (meetings_meeting)."""
    subject = models.CharField(max_length=255)
    agenda = models.TextField()
    meeting_date = models.DateTimeField()
    venue_or_link = models.CharField(max_length=255, help_text="Physical venue or Video link")
    status = models.CharField(max_length=20, choices=MeetingStatus.choices, default=MeetingStatus.SCHEDULED)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_meetings')

    class Meta:
        db_table = 'meetings_meeting'
        verbose_name = 'Meeting'
        verbose_name_plural = 'Meetings'
        ordering = ['-meeting_date']

    def __str__(self):
        return self.subject


class MeetingInvitee(models.Model):
    """Invited users and attendance tracking (meetings_invitee)."""
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='invitees')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='meeting_invites')
    attended = models.BooleanField(default=False)

    class Meta:
        db_table = 'meetings_invitee'
        unique_together = [['meeting', 'user']]


class MeetingMinutes(models.Model):
    """Post-meeting recorded minutes and attachments (meetings_minutes)."""
    meeting = models.OneToOneField(Meeting, on_delete=models.CASCADE, related_name='minutes')
    minutes_text = models.TextField()
    attachment_asset = models.ForeignKey(MediaAsset, on_delete=models.SET_NULL, null=True, blank=True, related_name='meeting_minutes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'meetings_minutes'
