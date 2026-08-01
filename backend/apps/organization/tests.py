from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from apps.organization.models import State, District, Taluka, Village, Designation
from apps.organization.services import OrganizationService
from apps.common.enums import UserType

User = get_user_model()


class OrganizationHierarchyTest(TestCase):
    def setUp(self):
        self.state = State.objects.create(name="Maharashtra", code="MH")
        self.district = District.objects.create(state=self.state, name="Pune", code="PUN")
        self.taluka = Taluka.objects.create(district=self.district, name="Haveli")
        self.village = Village.objects.create(taluka=self.taluka, name="Khadakwasla", pin_code="411024")
        self.designation = Designation.objects.create(title="District President", level_scope="DISTRICT")

        self.admin_user = User.objects.create_user(
            phone_number="9876543210",
            password="adminpassword123",
            user_type=UserType.ADMIN,
            is_staff=True
        )

        self.client = APIClient()

    def test_state_creation_and_uniqueness(self):
        self.assertEqual(self.state.name, "Maharashtra")
        self.assertEqual(self.state.code, "MH")

        # Duplicate case-insensitive test
        with self.assertRaises(ValidationError):
            OrganizationService.validate_case_insensitive_unique(State, 'name', '  maharashtra  ')

    def test_district_parent_relationship(self):
        self.assertEqual(self.district.state, self.state)
        self.assertEqual(self.district.name, "Pune")

    def test_deletion_rules_prevent_orphans(self):
        # State cannot be deleted while active District exists
        with self.assertRaises(ValidationError):
            OrganizationService.delete_state(self.state)

        # District cannot be deleted while active Taluka exists
        with self.assertRaises(ValidationError):
            OrganizationService.delete_district(self.district)

        # Taluka cannot be deleted while active Village exists
        with self.assertRaises(ValidationError):
            OrganizationService.delete_taluka(self.taluka)

    def test_soft_delete_cascade_protection(self):
        # Soft delete village first
        OrganizationService.delete_village(self.village)
        self.assertTrue(self.village.is_deleted)

        # Now taluka can be deleted
        OrganizationService.delete_taluka(self.taluka)
        self.assertTrue(self.taluka.is_deleted)

    def test_public_read_access_apis(self):
        response = self.client.get('/api/v1/organization/states/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Maharashtra')

    def test_admin_write_access_apis(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post('/api/v1/organization/states/', {
            'name': 'Karnataka',
            'code': 'KA'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(State.objects.filter(code='KA').exists())
