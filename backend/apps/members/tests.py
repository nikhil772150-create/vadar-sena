from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from datetime import date

from apps.common.enums import UserType, MemberStatus
from apps.organization.models import State, District, Taluka, Village
from apps.members.models import Member, MembershipCard, MemberTransferRequest
from apps.members.services import MemberService

User = get_user_model()


class MemberManagementTest(TestCase):
    def setUp(self):
        self.state = State.objects.create(name="Maharashtra", code="MH")
        self.district = District.objects.create(state=self.state, name="Pune", code="PUN")
        self.taluka = Taluka.objects.create(district=self.district, name="Haveli")
        self.village_a = Village.objects.create(taluka=self.taluka, name="Village A", pin_code="411001")
        self.village_b = Village.objects.create(taluka=self.taluka, name="Village B", pin_code="411002")

        self.admin_user = User.objects.create_user(
            phone_number="9999988888",
            password="adminpassword123",
            user_type=UserType.ADMIN,
            is_staff=True
        )

        self.client = APIClient()

    def test_member_registration_service(self):
        reg_data = {
            'first_name': 'Rahul',
            'last_name': 'Vadar',
            'gender': 'MALE',
            'date_of_birth': date(1995, 5, 15),
            'phone_number': '9876543210',
            'email': 'rahul@example.com',
            'state': self.state,
            'district': self.district,
            'taluka': self.taluka,
            'village': self.village_a,
            'occupation': 'Software Engineer'
        }

        member = MemberService.register_member(reg_data)
        self.assertEqual(member.status, MemberStatus.PENDING)
        self.assertIsNotNone(member.profile)
        self.assertEqual(member.profile.occupation, 'Software Engineer')
        self.assertEqual(member.status_history.count(), 1)
        self.assertFalse(member.membership_card.is_active)

    def test_member_approval_and_card_issuance(self):
        reg_data = {
            'first_name': 'Amit',
            'last_name': 'Patil',
            'gender': 'MALE',
            'date_of_birth': date(1990, 8, 20),
            'phone_number': '9876543211',
            'state': self.state,
            'district': self.district,
            'taluka': self.taluka,
            'village': self.village_a
        }
        member = MemberService.register_member(reg_data)
        
        # Approve member
        approved_member = MemberService.approve_member(member, admin_user=self.admin_user)
        approved_member.membership_card.refresh_from_db()
        self.assertEqual(approved_member.status, MemberStatus.APPROVED)
        self.assertTrue(approved_member.membership_number.startswith("BVS-MH-PUN-"))
        self.assertTrue(approved_member.membership_card.is_active)
        self.assertEqual(approved_member.membership_card.card_number, approved_member.membership_number)

    def test_member_rejection_and_suspension(self):
        member = MemberService.register_member({
            'first_name': 'Suresh',
            'last_name': 'Kumar',
            'date_of_birth': date(1992, 1, 1),
            'phone_number': '9876543212',
            'state': self.state,
            'district': self.district,
            'taluka': self.taluka,
            'village': self.village_a
        })
        
        MemberService.approve_member(member, self.admin_user)
        member.membership_card.refresh_from_db()
        self.assertTrue(member.membership_card.is_active)

        # Suspend member
        MemberService.suspend_member(member, self.admin_user)
        member.membership_card.refresh_from_db()
        self.assertEqual(member.status, MemberStatus.SUSPENDED)
        self.assertFalse(member.membership_card.is_active)

    def test_member_transfer_request(self):
        member = MemberService.register_member({
            'first_name': 'Vikas',
            'last_name': 'Shinde',
            'date_of_birth': date(1996, 3, 10),
            'phone_number': '9876543213',
            'state': self.state,
            'district': self.district,
            'taluka': self.taluka,
            'village': self.village_a
        })

        transfer_req = MemberService.request_transfer(member, self.village_b, reason="Job Relocation")
        self.assertEqual(transfer_req.from_village, self.village_a)
        self.assertEqual(transfer_req.to_village, self.village_b)

    def test_public_qr_card_verification_api(self):
        member = MemberService.register_member({
            'first_name': 'Pooja',
            'last_name': 'Deshmukh',
            'date_of_birth': date(1998, 7, 25),
            'phone_number': '9876543214',
            'state': self.state,
            'district': self.district,
            'taluka': self.taluka,
            'village': self.village_a
        })
        MemberService.approve_member(member, self.admin_user)
        member.membership_card.refresh_from_db()

        qr_token = member.membership_card.qr_token
        url = f'/api/v1/members/verify-card/{qr_token}/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertTrue(response.data['data']['is_valid'])
        self.assertEqual(response.data['data']['member_name'], 'Pooja Deshmukh')
