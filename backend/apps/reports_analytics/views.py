from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from apps.common.responses import success_response, error_response
from apps.common.permissions import IsAdminUserOrSuperAdmin, IsSuperAdmin
from apps.reports_analytics.models import RegionalStats
from apps.reports_analytics.serializers import RegionalStatsSerializer
from apps.reports_analytics.services import AnalyticsReportService


class DashboardView(APIView):
    """
    GET /api/v1/analytics/dashboard/
    Unified Executive Dashboard metrics API.
    """
    permission_classes = [IsAdminUserOrSuperAdmin]

    def get(self, request):
        summary_data = AnalyticsReportService.get_dashboard_summary()
        return success_response(summary_data, "Dashboard metrics compiled successfully")


class MemberReportView(APIView):
    """
    GET /api/v1/reports/members/
    Structured JSON Member Growth & Status Report.
    """
    permission_classes = [IsAdminUserOrSuperAdmin]

    def get(self, request):
        state_id = request.query_params.get('state')
        status_filter = request.query_params.get('status')
        report_data = AnalyticsReportService.get_member_report(state_id=state_id, status_filter=status_filter)
        return success_response(report_data, "Member report generated")


class DonationReportView(APIView):
    """
    GET /api/v1/reports/donations/
    Structured JSON Financial Donations Report.
    """
    permission_classes = [IsAdminUserOrSuperAdmin]

    def get(self, request):
        status_filter = request.query_params.get('status')
        report_data = AnalyticsReportService.get_donation_report(status_filter=status_filter)
        return success_response(report_data, "Donation report generated")


class RegionalStatsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/v1/analytics/regional-stats/
    Pre-aggregated regional statistics catalog.
    """
    queryset = RegionalStats.objects.all().select_related('state', 'district')
    serializer_class = RegionalStatsSerializer
    permission_classes = [IsAdminUserOrSuperAdmin]
