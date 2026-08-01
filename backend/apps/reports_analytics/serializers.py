from rest_framework import serializers
from apps.reports_analytics.models import RegionalStats


class RegionalStatsSerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)

    class Meta:
        model = RegionalStats
        fields = (
            'id', 'state', 'state_name', 'district', 'district_name',
            'total_members', 'approved_members', 'pending_members',
            'suspended_members', 'total_donations_amount', 'last_updated_at'
        )


class ReportFilterSerializer(serializers.Serializer):
    state = serializers.IntegerField(required=False, allow_null=True)
    status = serializers.CharField(required=False, allow_blank=True)
