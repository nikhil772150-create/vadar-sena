from rest_framework import serializers
from apps.common.validators import validate_indian_phone_number
from apps.donations.models import Donation


class DonationSerializer(serializers.ModelSerializer):
    receipt_url = serializers.SerializerMethodField()
    verified_by_phone = serializers.CharField(source='verified_by.phone_number', read_only=True)
    state_name = serializers.CharField(source='state.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)

    class Meta:
        model = Donation
        fields = (
            'id', 'uuid', 'donor_name', 'phone_number', 'email', 'amount',
            'purpose', 'transaction_id', 'payment_method', 'upi_ref',
            'receipt_asset', 'receipt_url', 'status', 'member', 'state',
            'state_name', 'district', 'district_name', 'verified_by',
            'verified_by_phone', 'verified_at', 'remarks', 'created_at'
        )
        read_only_fields = ('id', 'uuid', 'status', 'verified_by', 'verified_at', 'created_at')

    def get_receipt_url(self, obj):
        if obj.receipt_asset and obj.receipt_asset.file:
            return obj.receipt_asset.file.url
        return None


class DonationCreateSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(validators=[validate_indian_phone_number])

    class Meta:
        model = Donation
        fields = (
            'donor_name', 'phone_number', 'email', 'amount', 'purpose',
            'transaction_id', 'payment_method', 'upi_ref', 'receipt_asset',
            'member', 'state', 'district'
        )

    def validate_transaction_id(self, value):
        if Donation.objects.filter(transaction_id=value, is_deleted=False).exists():
            raise serializers.ValidationError("Donation with this transaction ID has already been submitted.")
        return value
