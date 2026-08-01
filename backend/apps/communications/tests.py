from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.communications.models import ContactInquiry, Notification
from apps.communications.services import CommunicationsService

User = get_user_model()


class CommunicationsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone_number="9876543210", password="password123")
        self.client = APIClient()

    def test_public_contact_form_submission(self):
        response = self.client.post('/api/v1/communications/contact/', {
            'name': 'Ramesh Kumar',
            'phone': '9876543210',
            'email': 'ramesh@example.com',
            'subject': 'Membership Enquiry',
            'message': 'How can I join the local unit?'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactInquiry.objects.count(), 1)

    def test_notification_dispatch_and_read(self):
        notification = CommunicationsService.send_notification(
            recipient_user=self.user,
            title="Meeting Scheduled",
            message="You have been invited to the district meeting."
        )
        self.assertFalse(notification.is_read)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/api/v1/communications/notifications/{notification.id}/mark_read/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)
