from rest_framework import serializers
from apps.common.validators import validate_indian_phone_number
from apps.members.models import (
    Member,
    MemberProfile,
    MemberDocument,
    MemberStatusHistory,
    MembershipCard,
    MemberTransferRequest
)
from apps.organization.serializers import (
    StateSerializer,
    DistrictSerializer,
    TalukaSerializer,
    VillageSerializer
)


class MemberProfileSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = MemberProfile
        fields = (
            'father_husband_name', 'blood_group', 'education', 'occupation',
            'address_line', 'pincode', 'emergency_contact_name',
            'emergency_contact_phone', 'photo_asset', 'photo_url'
        )

    def get_photo_url(self, obj):
        if obj.photo_asset and obj.photo_asset.file:
            return obj.photo_asset.file.url
        return None


class MembershipCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipCard
        fields = ('card_number', 'qr_token', 'issued_at', 'expires_at', 'is_active')


class MemberDocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = MemberDocument
        fields = ('id', 'document_type', 'document_number', 'file_asset', 'file_url', 'verification_status', 'created_at')
        read_only_fields = ('id', 'created_at')

    def get_file_url(self, obj):
        if obj.file_asset and obj.file_asset.file:
            return obj.file_asset.file.url
        return None


class MemberStatusHistorySerializer(serializers.ModelSerializer):
    changed_by_phone = serializers.CharField(source='changed_by.phone_number', read_only=True)

    class Meta:
        model = MemberStatusHistory
        fields = ('id', 'previous_status', 'new_status', 'changed_by_phone', 'remarks', 'created_at')


class MemberTransferRequestSerializer(serializers.ModelSerializer):
    from_village_name = serializers.CharField(source='from_village.name', read_only=True)
    to_village_name = serializers.CharField(source='to_village.name', read_only=True)

    class Meta:
        model = MemberTransferRequest
        fields = ('id', 'member', 'from_village', 'from_village_name', 'to_village', 'to_village_name', 'reason', 'status', 'requested_at', 'approved_at')
        read_only_fields = ('id', 'from_village', 'status', 'requested_at', 'approved_at')


class MemberRegistrationSerializer(serializers.Serializer):
    """Member public registration payload serializer."""
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    gender = serializers.ChoiceField(choices=['MALE', 'FEMALE', 'OTHER'], default='MALE')
    date_of_birth = serializers.DateField()
    phone_number = serializers.CharField(validators=[validate_indian_phone_number])
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    state = serializers.IntegerField()
    district = serializers.IntegerField()
    taluka = serializers.IntegerField()
    village = serializers.IntegerField()

    # Optional Profile fields
    father_husband_name = serializers.CharField(required=False, allow_blank=True)
    blood_group = serializers.CharField(required=False, allow_blank=True)
    education = serializers.CharField(required=False, allow_blank=True)
    occupation = serializers.CharField(required=False, allow_blank=True)
    address_line = serializers.CharField(required=False, allow_blank=True)
    pincode = serializers.CharField(required=False, allow_blank=True)
    emergency_contact_name = serializers.CharField(required=False, allow_blank=True)
    emergency_contact_phone = serializers.CharField(required=False, allow_blank=True)


class MemberListSerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    taluka_name = serializers.CharField(source='taluka.name', read_only=True)
    village_name = serializers.CharField(source='village.name', read_only=True)

    class Meta:
        model = Member
        fields = (
            'id', 'uuid', 'membership_number', 'first_name', 'last_name',
            'gender', 'phone_number', 'email', 'status', 'state', 'state_name',
            'district', 'district_name', 'taluka', 'taluka_name', 'village',
            'village_name', 'created_at', 'approved_at'
        )


class MemberDetailSerializer(serializers.ModelSerializer):
    state_detail = StateSerializer(source='state', read_only=True)
    district_detail = DistrictSerializer(source='district', read_only=True)
    taluka_detail = TalukaSerializer(source='taluka', read_only=True)
    village_detail = VillageSerializer(source='village', read_only=True)
    profile = MemberProfileSerializer(read_only=True)
    membership_card = MembershipCardSerializer(read_only=True)
    documents = MemberDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Member
        fields = (
            'id', 'uuid', 'membership_number', 'first_name', 'last_name',
            'gender', 'date_of_birth', 'phone_number', 'email', 'status',
            'state', 'state_detail', 'district', 'district_detail',
            'taluka', 'taluka_detail', 'village', 'village_detail',
            'profile', 'membership_card', 'documents', 'created_at', 'approved_at'
        )


class MemberCardVerificationSerializer(serializers.Serializer):
    """Public QR code card verification payload."""
    is_valid = serializers.BooleanField()
    member_name = serializers.CharField()
    membership_number = serializers.CharField()
    status = serializers.CharField()
    photo_url = serializers.CharField(allow_null=True)
    district_name = serializers.CharField()
    taluka_name = serializers.CharField()
    village_name = serializers.CharField()
    issued_at = serializers.DateTimeField(allow_null=True)
