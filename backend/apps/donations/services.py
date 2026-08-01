import logging
from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.donations.models import Donation, VerificationStatus

logger = logging.getLogger(__name__)


class DonationService:
    @staticmethod
    def create_donation(data):
        tx_id = data.get('transaction_id')
        if Donation.objects.filter(transaction_id=tx_id, is_deleted=False).exists():
            raise ValidationError(f"A donation with Transaction ID '{tx_id}' already exists.")

        donation = Donation.objects.create(**data)
        logger.info(f"[DONATION SUBMITTED] ID: {donation.id} | Amount: ₹{donation.amount} | Tx: {tx_id}")
        return donation

    @staticmethod
    def verify_donation(donation: Donation, admin_user, remarks="Payment verified by Finance Admin"):
        if donation.status == VerificationStatus.VERIFIED:
            return donation

        donation.status = VerificationStatus.VERIFIED
        donation.verified_by = admin_user
        donation.verified_at = timezone.now()
        donation.remarks = remarks
        donation.save(update_fields=['status', 'verified_by', 'verified_at', 'remarks', 'updated_at'])
        logger.info(f"[DONATION VERIFIED] ID: {donation.id} | Amount: ₹{donation.amount} | Verified by: {admin_user}")
        return donation

    @staticmethod
    def reject_donation(donation: Donation, admin_user, remarks="Invalid payment receipt/tx ID"):
        donation.status = VerificationStatus.REJECTED
        donation.verified_by = admin_user
        donation.verified_at = timezone.now()
        donation.remarks = remarks
        donation.save(update_fields=['status', 'verified_by', 'verified_at', 'remarks', 'updated_at'])
        logger.info(f"[DONATION REJECTED] ID: {donation.id} | Admin: {admin_user}")
        return donation
