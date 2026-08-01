from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.common.enums import UserType
from apps.reports_analytics.services import AnalyticsReportService

User = get_user_model()


class ReportsAnalyticsTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            phone_number="9999988888",
            password="adminpassword123",
            user_type=UserType.ADMIN,
            is_staff=True
        )
        self.client = APIClient()

    def test_dashboard_summary_service(self):
        summary = AnalyticsReportService.get_dashboard_summary()
        self.assertIn('counters', summary)
        self.assertIn('total_members', summary['counters'])
        self.assertIn('financials', summary)
        self.assertIn('breakdowns', summary)

    def test_dashboard_api_authenticated(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/v1/analytics/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('counters', response.data['data'])

    def test_member_report_api(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/v1/reports/members/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

    def test_donation_report_api(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/v1/reports/donations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
