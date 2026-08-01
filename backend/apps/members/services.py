import logging
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from apps.common.enums import MemberStatus, VerificationStatus
from apps.members.models import (
    Member,
    MemberProfile,
    MemberStatusHistory,
    MembershipCard,
    MemberTransferRequest,
    MemberDocument
)

User = get_user_model()
logger = logging.getLogger(__name__)


class MemberService:
    """
    Business service encapsulating member onboarding, status transitions,
    card issuance, and transfer requests.
    """

    @classmethod
    @transaction.atomic
    def register_member(cls, data):
        """
        Onboards a new member: creates/links User, Member, MemberProfile,
        PENDING StatusHistory, and Card placeholder.
        """
        phone_number = data.get('phone_number')
        email = data.get('email')

        if Member.objects.filter(phone_number=phone_number, is_deleted=False).exists():
            raise ValidationError("A member with this phone number is already registered.")

        # Get or create user account
        user, _ = User.objects.get_or_create(
            phone_number=phone_number,
            defaults={'email': email, 'is_active': True}
        )

        member = Member.objects.create(
            user=user,
            first_name=data['first_name'],
            last_name=data['last_name'],
            gender=data.get('gender', 'MALE'),
            date_of_birth=data['date_of_birth'],
            phone_number=phone_number,
            email=email,
            state=data['state'],
            district=data['district'],
            taluka=data['taluka'],
            village=data['village'],
            status=MemberStatus.PENDING
        )

        # Create Profile
        MemberProfile.objects.create(
            member=member,
            father_husband_name=data.get('father_husband_name'),
            blood_group=data.get('blood_group'),
            education=data.get('education'),
            occupation=data.get('occupation'),
            address_line=data.get('address_line'),
            pincode=data.get('pincode'),
            emergency_contact_name=data.get('emergency_contact_name'),
            emergency_contact_phone=data.get('emergency_contact_phone')
        )

        # Log Status History
        MemberStatusHistory.objects.create(
            member=member,
            previous_status='',
            new_status=MemberStatus.PENDING,
            remarks="Initial Member Registration"
        )

        # Create Card Placeholder
        MembershipCard.objects.create(
            member=member,
            card_number=f"PENDING-{member.id}",
            qr_token=MembershipCard.generate_unique_qr_token(),
            is_active=False
        )

        logger.info(f"[MEMBER REGISTERED] Member ID: {member.id} | Phone: {phone_number}")
        return member

    @classmethod
    @transaction.atomic
    def approve_member(cls, member: Member, admin_user=None, remarks="Approved by Admin"):
        """
        Approves member, generates unique Membership Number, and activates digital card.
        """
        if member.status == MemberStatus.APPROVED:
            return member

        old_status = member.status
        member.status = MemberStatus.APPROVED
        member.approved_at = timezone.now()
        member.approved_by = admin_user

        # Generate unique membership number: BVS-{STATE_CODE}-{DISTRICT_CODE}-{ID:06d}
        state_code = member.state.code if member.state and member.state.code else "MH"
        dist_code = member.district.code if member.district and member.district.code else "DIST"
        member.membership_number = f"BVS-{state_code}-{dist_code}-{member.id:06d}"
        member.save(update_fields=['status', 'approved_at', 'approved_by', 'membership_number', 'updated_at'])

        # Update and activate MembershipCard
        card, _ = MembershipCard.objects.get_or_create(member=member)
        card.card_number = member.membership_number
        card.qr_token = MembershipCard.generate_unique_qr_token()
        card.issued_at = timezone.now()
        card.is_active = True
        card.save()
        member.membership_card = card

        # Log Status History
        MemberStatusHistory.objects.create(
            member=member,
            previous_status=old_status,
            new_status=MemberStatus.APPROVED,
            changed_by=admin_user,
            remarks=remarks
        )

        logger.info(f"[MEMBER APPROVED] Membership No: {member.membership_number} | Member ID: {member.id}")
        return member

    @classmethod
    @transaction.atomic
    def reject_member(cls, member: Member, admin_user=None, remarks="Registration rejected"):
        """Rejects member registration."""
        old_status = member.status
        member.status = MemberStatus.REJECTED
        member.save(update_fields=['status', 'updated_at'])

        # Deactivate card
        if hasattr(member, 'membership_card'):
            member.membership_card.is_active = False
            member.membership_card.save(update_fields=['is_active'])

        MemberStatusHistory.objects.create(
            member=member,
            previous_status=old_status,
            new_status=MemberStatus.REJECTED,
            changed_by=admin_user,
            remarks=remarks
        )
        return member

    @classmethod
    @transaction.atomic
    def suspend_member(cls, member: Member, admin_user=None, remarks="Membership suspended"):
        """Suspends an active member."""
        old_status = member.status
        member.status = MemberStatus.SUSPENDED
        member.save(update_fields=['status', 'updated_at'])

        if hasattr(member, 'membership_card'):
            member.membership_card.is_active = False
            member.membership_card.save(update_fields=['is_active'])

        MemberStatusHistory.objects.create(
            member=member,
            previous_status=old_status,
            new_status=MemberStatus.SUSPENDED,
            changed_by=admin_user,
            remarks=remarks
        )
        return member

    @classmethod
    @transaction.atomic
    def restore_member(cls, member: Member, admin_user=None, remarks="Member restored"):
        """Restores a soft-deleted or suspended member."""
        old_status = member.status
        member.restore()
        member.status = MemberStatus.APPROVED if member.membership_number else MemberStatus.PENDING
        member.save(update_fields=['status', 'is_deleted', 'deleted_at', 'updated_at'])

        if hasattr(member, 'membership_card') and member.status == MemberStatus.APPROVED:
            member.membership_card.is_active = True
            member.membership_card.save(update_fields=['is_active'])

        MemberStatusHistory.objects.create(
            member=member,
            previous_status=old_status,
            new_status=member.status,
            changed_by=admin_user,
            remarks=remarks
        )
        return member

    @classmethod
    def request_transfer(cls, member: Member, to_village, reason="Member Relocation"):
        """Creates a regional transfer request."""
        if member.village == to_village:
            raise ValidationError("Destination village must be different from current village.")

        transfer_req = MemberTransferRequest.objects.create(
            member=member,
            from_village=member.village,
            to_village=to_village,
            reason=reason,
            status=VerificationStatus.PENDING
        )
        return transfer_req
