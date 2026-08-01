from django.db import models
from django.conf import settings
from apps.common.models import BaseModel, MediaAsset
from apps.common.validators import validate_indian_phone_number
from apps.organization.models import State, District
from apps.members.models import Member


class PaymentMethod(models.TextChoices):
    UPI = 'UPI', 'UPI Payment'
    BANK_TRANSFER = 'BANK_TRANSFER', 'Bank Transfer (NEFT/RTGS)'
    CASH = 'CASH', 'Cash'
    CHEQUE = 'CHEQUE', 'Cheque'
    OTHER = 'OTHER', 'Other'


class VerificationStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending Verification'
    VERIFIED = 'VERIFIED', 'Verified'
    REJECTED = 'REJECTED', 'Rejected'


class Donation(BaseModel):
    """Donation record entity (donations_donation)."""
    donor_name = models.CharField(max_length=150, help_text="Name of donor")
    phone_number = models.CharField(max_length=15, validators=[validate_indian_phone_number], help_text="Contact phone number")
    email = models.EmailField(blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Donation amount in INR")
    purpose = models.CharField(max_length=200, default="General Organization Fund", help_text="Donation intent/cause")
    transaction_id = models.CharField(max_length=100, unique=True, db_index=True, help_text="Unique transaction or reference ID")
    payment_method = models.CharField(max_length=30, choices=PaymentMethod.choices, default=PaymentMethod.UPI)
    upi_ref = models.CharField(max_length=100, blank=True, null=True, help_text="UPI Reference No")
    receipt_asset = models.ForeignKey(MediaAsset, on_delete=models.SET_NULL, null=True, blank=True, related_name='donation_receipts')
    status = models.CharField(max_length=20, choices=VerificationStatus.choices, default=VerificationStatus.PENDING, db_index=True)
    
    # Optional linkage
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='donations')
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True, related_name='donations')
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, related_name='donations')
    
    # Audit tracking
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_donations')
    verified_at = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'donations_donation'
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.donor_name} - ₹{self.amount} ({self.status})"
