import logging
from apps.communications.models import ContactInquiry, Notification, ContactInquiryStatus

logger = logging.getLogger(__name__)


class CommunicationsService:
    @staticmethod
    def create_inquiry(name, phone, subject, message, email=None):
        inquiry = ContactInquiry.objects.create(
            name=name.strip(),
            phone=phone.strip(),
            email=email.strip() if email else None,
            subject=subject.strip(),
            message=message.strip()
        )
        logger.info(f"[CONTACT INQUIRY RECEIVED] From: {name} | Subject: {subject}")
        return inquiry

    @staticmethod
    def resolve_inquiry(inquiry: ContactInquiry, admin_user):
        inquiry.status = ContactInquiryStatus.RESOLVED
        inquiry.resolved_by = admin_user
        inquiry.save(update_fields=['status', 'resolved_by', 'updated_at'])
        logger.info(f"[CONTACT INQUIRY RESOLVED] ID: {inquiry.id} | Admin: {admin_user}")
        return inquiry

    @staticmethod
    def send_notification(recipient_user, title, message, link_url=None):
        notification = Notification.objects.create(
            recipient_user=recipient_user,
            title=title,
            message=message,
            link_url=link_url
        )
        logger.info(f"[NOTIFICATION DISPATCHED] User: {recipient_user.phone_number} | Title: {title}")
        return notification
