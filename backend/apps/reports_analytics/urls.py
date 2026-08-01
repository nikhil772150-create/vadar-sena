from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.reports_analytics.views import (
    DashboardView,
    MemberReportView,
    DonationReportView,
    RegionalStatsViewSet
)

router = DefaultRouter()
router.register('regional-stats', RegionalStatsViewSet, basename='regional-stats')

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard-summary'),
    path('reports/members/', MemberReportView.as_view(), name='report-members'),
    path('reports/donations/', DonationReportView.as_view(), name='report-donations'),
    path('', include(router.urls)),
]
