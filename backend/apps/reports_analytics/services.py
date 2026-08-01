import logging
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta

from apps.members.models import Member
from apps.donations.models import Donation, VerificationStatus
from apps.news_cms.models import News, NewsStatus
from apps.events_meetings.models import Event, EventStatus
from apps.organization.models import State, District

logger = logging.getLogger(__name__)


class AnalyticsReportService:
    """
    Service generating structured JSON dashboard aggregations and exportable analytics reports.
    """

    @classmethod
    def get_dashboard_summary(cls):
        now = timezone.now()
        start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Member Status Counters
        member_counts = Member.objects.filter(is_deleted=False).aggregate(
            total=Count('id'),
            pending=Count('id', filter=Q(status='PENDING')),
            approved=Count('id', filter=Q(status='APPROVED')),
            suspended=Count('id', filter=Q(status='SUSPENDED')),
            transferred=Count('id', filter=Q(status='TRANSFERRED')),
            today=Count('id', filter=Q(created_at__gte=start_of_today)),
            monthly=Count('id', filter=Q(created_at__gte=start_of_month))
        )

        # Regional Breakdown
        state_breakdown = list(
            State.objects.filter(is_deleted=False).annotate(
                member_count=Count('members', filter=Q(members__is_deleted=False))
            ).values('id', 'name', 'code', 'member_count')
        )

        district_breakdown = list(
            District.objects.filter(is_deleted=False).annotate(
                member_count=Count('members', filter=Q(members__is_deleted=False))
            ).values('id', 'name', 'state__name', 'member_count')[:10]
        )

        # Financial Aggregations
        donation_stats = Donation.objects.filter(is_deleted=False, status=VerificationStatus.VERIFIED).aggregate(
            total_amount=Sum('amount'),
            total_count=Count('id')
        )

        # Recent Feeds
        recent_members = list(
            Member.objects.filter(is_deleted=False)
            .select_related('district')
            .order_by('-created_at')
            .values('id', 'first_name', 'last_name', 'membership_number', 'status', 'district__name', 'created_at')[:5]
        )

        recent_donations = list(
            Donation.objects.filter(is_deleted=False, status=VerificationStatus.VERIFIED)
            .order_by('-created_at')
            .values('id', 'donor_name', 'amount', 'purpose', 'transaction_id', 'created_at')[:5]
        )

        upcoming_events = list(
            Event.objects.filter(is_deleted=False, status=EventStatus.UPCOMING)
            .order_by('start_time')
            .values('id', 'title', 'start_time', 'venue_address')[:5]
        )

        latest_news = list(
            News.objects.filter(is_deleted=False, status=NewsStatus.PUBLISHED)
            .order_by('-published_at')
            .values('id', 'title', 'slug', 'published_at')[:5]
        )

        logger.info("[DASHBOARD ACCESSED] Summary metrics compiled successfully.")

        return {
            "counters": {
                "total_members": member_counts['total'],
                "pending_members": member_counts['pending'],
                "approved_members": member_counts['approved'],
                "suspended_members": member_counts['suspended'],
                "transferred_members": member_counts['transferred'],
                "today_registrations": member_counts['today'],
                "monthly_registrations": member_counts['monthly']
            },
            "financials": {
                "total_verified_donations": float(donation_stats['total_amount'] or 0.00),
                "total_donation_count": donation_stats['total_count']
            },
            "breakdowns": {
                "members_by_state": state_breakdown,
                "top_districts": district_breakdown
            },
            "feeds": {
                "recent_members": recent_members,
                "recent_donations": recent_donations,
                "upcoming_events": upcoming_events,
                "latest_news": latest_news
            }
        }

    @classmethod
    def get_member_report(cls, state_id=None, status_filter=None):
        qs = Member.objects.filter(is_deleted=False).select_related('state', 'district', 'taluka', 'village')
        if state_id:
            qs = qs.filter(state_id=state_id)
        if status_filter:
            qs = qs.filter(status=status_filter)

        summary = qs.aggregate(
            total=Count('id'),
            approved=Count('id', filter=Q(status='APPROVED')),
            pending=Count('id', filter=Q(status='PENDING'))
        )
        return {
            "summary": summary,
            "total_records": qs.count(),
            "data": list(qs.values('id', 'membership_number', 'first_name', 'last_name', 'phone_number', 'status', 'state__name', 'district__name', 'created_at')[:100])
        }

    @classmethod
    def get_donation_report(cls, status_filter=None):
        qs = Donation.objects.filter(is_deleted=False)
        if status_filter:
            qs = qs.filter(status=status_filter)

        summary = qs.aggregate(
            total_count=Count('id'),
            total_sum=Sum('amount')
        )
        return {
            "summary": {
                "total_count": summary['total_count'],
                "total_amount": float(summary['total_sum'] or 0.00)
            },
            "data": list(qs.values('id', 'donor_name', 'phone_number', 'amount', 'purpose', 'transaction_id', 'status', 'created_at')[:100])
        }
