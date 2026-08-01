from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.common.enums import UserType
from apps.donations.models import Donation, VerificationStatus
from apps.donations.services import DonationService

User = get_user_model()


class DonationTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(phone_number="9999988888", password="adminpassword", user_type=UserType.ADMIN)
        self.donation = Donation.objects.create(
            donor_name="Siddharth Rao",
            phone_number="9876543210",
            amount=5000.00,
            transaction_id="TXN987654321",
            payment_method="UPI",
            status=VerificationStatus.PENDING
        )
        self.client = APIClient()

    def test_donation_creation_service(self):
        donation = DonationService.create_donation({
            'donor_name': 'Anil Deshmukh',
            'phone_number': '9876543211',
            'amount': 2500.00,
            'transaction_id': 'TXN11223344',
            'payment_method': 'UPI'
        })
        self.assertEqual(donation.status, VerificationStatus.PENDING)
        self.assertEqual(donation.amount, 2500.00)

    def test_donation_verification_service(self):
        verified = DonationService.verify_donation(self.donation, self.admin)
        self.assertEqual(verified.status, VerificationStatus.VERIFIED)
        self.assertEqual(verified.verified_by, self.admin)

    def test_public_donation_submission_api(self):
        response = self.client.post('/api/v1/donations/', {
            'donor_name': 'Kavita Sharma',
            'phone_number': '9876543212',
            'amount': 1000.00,
            'transaction_id': 'TXN99887766',
            'payment_method': 'UPI'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Donation.objects.filter(transaction_id='TXN99887766').exists())
