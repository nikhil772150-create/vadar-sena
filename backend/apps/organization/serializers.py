from rest_framework import serializers
from django.core.exceptions import ValidationError
from apps.organization.models import State, District, Taluka, Village, Designation
from apps.organization.services import OrganizationService


class StateSerializer(serializers.ModelSerializer):
    districts_count = serializers.SerializerMethodField()

    class Meta:
        model = State
        fields = ('id', 'uuid', 'name', 'code', 'is_active', 'districts_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'uuid', 'created_at', 'updated_at')

    def get_districts_count(self, obj):
        return obj.districts.filter(is_deleted=False).count()

    def validate_name(self, value):
        current_id = self.instance.id if self.instance else None
        try:
            return OrganizationService.validate_case_insensitive_unique(State, 'name', value, current_id=current_id)
        except ValidationError as e:
            raise serializers.ValidationError(e.message)


class DistrictSerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', read_only=True)
    state_code = serializers.CharField(source='state.code', read_only=True)
    talukas_count = serializers.SerializerMethodField()

    class Meta:
        model = District
        fields = ('id', 'uuid', 'state', 'state_name', 'state_code', 'name', 'code', 'is_active', 'talukas_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'uuid', 'created_at', 'updated_at')

    def get_talukas_count(self, obj):
        return obj.talukas.filter(is_deleted=False).count()

    def validate(self, attrs):
        state = attrs.get('state', getattr(self.instance, 'state', None))
        name = attrs.get('name', getattr(self.instance, 'name', None))
        current_id = self.instance.id if self.instance else None

        if state and name:
            try:
                attrs['name'] = OrganizationService.validate_case_insensitive_unique(
                    District, 'name', name, parent_filter={'state': state}, current_id=current_id
                )
            except ValidationError as e:
                raise serializers.ValidationError({'name': e.message})
        return attrs


class TalukaSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source='district.name', read_only=True)
    state_name = serializers.CharField(source='district.state.name', read_only=True)
    villages_count = serializers.SerializerMethodField()

    class Meta:
        model = Taluka
        fields = ('id', 'uuid', 'district', 'district_name', 'state_name', 'name', 'is_active', 'villages_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'uuid', 'created_at', 'updated_at')

    def get_villages_count(self, obj):
        return obj.villages.filter(is_deleted=False).count()

    def validate(self, attrs):
        district = attrs.get('district', getattr(self.instance, 'district', None))
        name = attrs.get('name', getattr(self.instance, 'name', None))
        current_id = self.instance.id if self.instance else None

        if district and name:
            try:
                attrs['name'] = OrganizationService.validate_case_insensitive_unique(
                    Taluka, 'name', name, parent_filter={'district': district}, current_id=current_id
                )
            except ValidationError as e:
                raise serializers.ValidationError({'name': e.message})
        return attrs


class VillageSerializer(serializers.ModelSerializer):
    taluka_name = serializers.CharField(source='taluka.name', read_only=True)
    district_name = serializers.CharField(source='taluka.district.name', read_only=True)

    class Meta:
        model = Village
        fields = ('id', 'uuid', 'taluka', 'taluka_name', 'district_name', 'name', 'pin_code', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'uuid', 'created_at', 'updated_at')

    def validate(self, attrs):
        taluka = attrs.get('taluka', getattr(self.instance, 'taluka', None))
        name = attrs.get('name', getattr(self.instance, 'name', None))
        current_id = self.instance.id if self.instance else None

        if taluka and name:
            try:
                attrs['name'] = OrganizationService.validate_case_insensitive_unique(
                    Village, 'name', name, parent_filter={'taluka': taluka}, current_id=current_id
                )
            except ValidationError as e:
                raise serializers.ValidationError({'name': e.message})
        return attrs


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ('id', 'uuid', 'title', 'level_scope', 'display_order', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'uuid', 'created_at', 'updated_at')

    def validate_title(self, value):
        current_id = self.instance.id if self.instance else None
        try:
            return OrganizationService.validate_case_insensitive_unique(Designation, 'title', value, current_id=current_id)
        except ValidationError as e:
            raise serializers.ValidationError(e.message)
