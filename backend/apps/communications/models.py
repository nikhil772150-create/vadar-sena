from django.db import models
from django.conf import settings
from apps.common.models import BaseModel
from apps.common.enums import VerificationStatus
from apps.common.validators import validate_indian_phone_number


class ContactInquiryStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    RESOLVED = 'RESOLVED', 'Resolved'
    SPAM = 'SPAM', 'Spam'


class NotificationChannel(models.TextChoices):
    IN_APP = 'IN_APP', 'In-App Notification'
    SMS = 'SMS', 'SMS Alert'
    EMAIL = 'EMAIL', 'Email Alert'


class ContactInquiry(BaseModel):
    """Public Contact Form inquiries and resolution tracking (comm_contact_inquiries)."""
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, validators=[validate_indian_phone_number])
    email = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=ContactInquiryStatus.choices, default=ContactInquiryStatus.PENDING)
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_inquiries')

    class Meta:
        db_table = 'comm_contact_inquiries'
        verbose_name = 'Contact Inquiry'
        verbose_name_plural = 'Contact Inquiries'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.status})"


class Notification(models.Model):
    """Targeted in-app and broadcast system alerts (comm_notifications)."""
    recipient_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    link_url = models.CharField(max_length=255, blank=True, null=True)
    channel = models.CharField(max_length=20, choices=NotificationChannel.choices, default=NotificationChannel.IN_APP)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comm_notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"To: {self.recipient_user} - {self.title}"
