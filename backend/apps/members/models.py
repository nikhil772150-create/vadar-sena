import secrets
import uuid
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date

from apps.common.models import BaseModel, MediaAsset
from apps.common.enums import MemberStatus, VerificationStatus
from apps.common.validators import validate_indian_phone_number
from apps.organization.models import State, District, Taluka, Village


class DocumentType(models.TextChoices):
    PHOTO = 'PHOTO', 'Profile Photo'
    AADHAAR = 'AADHAAR', 'Aadhaar Card'
    PAN = 'PAN', 'PAN Card'
    ADDRESS_PROOF = 'ADDRESS_PROOF', 'Address Proof'
    EDUCATION_CERT = 'EDUCATION_CERT', 'Education Certificate'
    OTHER = 'OTHER', 'Other Document'


class GenderChoices(models.TextChoices):
    MALE = 'MALE', 'Male'
    FEMALE = 'FEMALE', 'Female'
    OTHER = 'OTHER', 'Other'


class Member(BaseModel):
    """
    Primary Member entity (members_member).
    Represents an onboarded community member linked to organizational hierarchy nodes.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='member_profile',
        null=True,
        blank=True,
        help_text="Linked authentication identity account"
    )
    membership_number = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        help_text="Unique Member Serial ID (e.g., BVS-MH-PUN-001001)"
    )
    first_name = models.CharField(
        max_length=100,
        help_text="First Name"
    )
    last_name = models.CharField(
        max_length=100,
        help_text="Last Name"
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
        default=GenderChoices.MALE
    )
    date_of_birth = models.DateField(
        help_text="Birth Date (Must be age >= 18)"
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        db_index=True,
        validators=[validate_indian_phone_number],
        help_text="10-digit Indian phone number"
    )
    email = models.EmailField(
        max_length=254,
        null=True,
        blank=True,
        help_text="Optional member email"
    )
    state = models.ForeignKey(
        State,
        on_delete=models.PROTECT,
        related_name='members',
        help_text="State node"
    )
    district = models.ForeignKey(
        District,
        on_delete=models.PROTECT,
        related_name='members',
        help_text="District node"
    )
    taluka = models.ForeignKey(
        Taluka,
        on_delete=models.PROTECT,
        related_name='members',
        help_text="Taluka node"
    )
    village = models.ForeignKey(
        Village,
        on_delete=models.PROTECT,
        related_name='members',
        help_text="Village node"
    )
    status = models.CharField(
        max_length=20,
        choices=MemberStatus.choices,
        default=MemberStatus.PENDING,
        db_index=True,
        help_text="Membership approval status"
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_members'
    )

    class Meta:
        db_table = 'members_member'
        verbose_name = 'Member'
        verbose_name_plural = 'Members'
        ordering = ['-created_at']

    def clean(self):
        super().clean()
        if self.first_name:
            self.first_name = self.first_name.strip()
        if self.last_name:
            self.last_name = self.last_name.strip()
            
        # Age validation (>= 18)
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
            if age < 18:
                raise ValidationError("Member must be at least 18 years old.")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.membership_number or 'Pending'})"


class MemberProfile(models.Model):
    """Extended personal and background details for a Member (members_profile)."""
    member = models.OneToOneField(
        Member,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    photo_asset = models.ForeignKey(
        MediaAsset,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='member_photos'
    )
    father_husband_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )
    blood_group = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )
    education = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    occupation = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    address_line = models.TextField(
        blank=True,
        null=True
    )
    pincode = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )
    emergency_contact_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    emergency_contact_phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'members_profile'

    def __str__(self):
        return f"Profile for {self.member}"


class MemberDocument(models.Model):
    """Uploaded verification documents for a Member (members_document)."""
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    document_type = models.CharField(
        max_length=30,
        choices=DocumentType.choices,
        default=DocumentType.AADHAAR
    )
    document_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Reference/Masked Document Number"
    )
    file_asset = models.ForeignKey(
        MediaAsset,
        on_delete=models.PROTECT,
        related_name='member_documents'
    )
    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'members_document'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.document_type} for {self.member}"


class MemberStatusHistory(models.Model):
    """Audit history log of member status transitions (members_status_history)."""
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='status_history'
    )
    previous_status = models.CharField(
        max_length=20,
        choices=MemberStatus.choices
    )
    new_status = models.CharField(
        max_length=20,
        choices=MemberStatus.choices
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    remarks = models.TextField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'members_status_history'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.member}: {self.previous_status} -> {self.new_status}"


class MembershipCard(models.Model):
    """Issued digital membership card & QR token record (members_card)."""
    member = models.OneToOneField(
        Member,
        on_delete=models.CASCADE,
        related_name='membership_card'
    )
    card_number = models.CharField(
        max_length=40,
        unique=True,
        db_index=True
    )
    qr_token = models.CharField(
        max_length=128,
        unique=True,
        db_index=True
    )
    issued_at = models.DateTimeField(
        null=True,
        blank=True
    )
    expires_at = models.DateTimeField(
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = 'members_card'

    @classmethod
    def generate_unique_qr_token(cls):
        """Generates a secure 64-char hexadecimal token for QR code verification."""
        return secrets.token_hex(32)

    def __str__(self):
        return f"Card {self.card_number} ({'Active' if self.is_active else 'Inactive'})"


class MemberTransferRequest(models.Model):
    """Member regional transfer request record (members_transfer_request)."""
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='transfer_requests'
    )
    from_village = models.ForeignKey(
        Village,
        on_delete=models.PROTECT,
        related_name='transfers_from'
    )
    to_village = models.ForeignKey(
        Village,
        on_delete=models.PROTECT,
        related_name='transfers_to'
    )
    reason = models.TextField(
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING
    )
    requested_at = models.DateTimeField(
        auto_now_add=True
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'members_transfer_request'
        ordering = ['-requested_at']

    def __str__(self):
        return f"Transfer request for {self.member} ({self.from_village} -> {self.to_village})"
