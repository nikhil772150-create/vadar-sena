from rest_framework import viewsets, permissions, status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ValidationError

from apps.common.responses import success_response, error_response
from apps.common.permissions import IsAdminUserOrSuperAdmin
from apps.organization.models import State, District, Taluka, Village, Designation
from apps.organization.serializers import (
    StateSerializer,
    DistrictSerializer,
    TalukaSerializer,
    VillageSerializer,
    DesignationSerializer
)
from apps.organization.services import OrganizationService


class BaseOrganizationViewSet(viewsets.ModelViewSet):
    """Base ViewSet enforcing RBAC write permissions and standard response envelopes."""
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdminUserOrSuperAdmin()]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data, "Records retrieved successfully")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(serializer.data, "Record retrieved successfully")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            return success_response(serializer.data, "Record created successfully", status.HTTP_201_CREATED)
        except Exception as e:
            return error_response(None, f"Record with matching unique fields (name/code) already exists or is archived: {str(e)}", status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)
            return success_response(serializer.data, "Record updated successfully")
        except Exception as e:
            return error_response(None, f"Update failed due to unique constraint conflict: {str(e)}", status.HTTP_400_BAD_REQUEST)


class StateViewSet(BaseOrganizationViewSet):
    queryset = State.objects.filter(is_deleted=False)
    serializer_class = StateSerializer
    search_fields = ['name', 'code', 'uuid']
    ordering_fields = ['name', 'code', 'created_at']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            OrganizationService.delete_state(instance)
            return success_response(None, "State deleted successfully", status.HTTP_200_OK)
        except ValidationError as e:
            return error_response(None, e.message, status.HTTP_400_BAD_REQUEST)


class DistrictViewSet(BaseOrganizationViewSet):
    queryset = District.objects.filter(is_deleted=False).select_related('state')
    serializer_class = DistrictSerializer
    filterset_fields = ['state', 'is_active']
    search_fields = ['name', 'code', 'state__name', 'uuid']
    ordering_fields = ['name', 'created_at']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            OrganizationService.delete_district(instance)
            return success_response(None, "District deleted successfully", status.HTTP_200_OK)
        except ValidationError as e:
            return error_response(None, e.message, status.HTTP_400_BAD_REQUEST)


class TalukaViewSet(BaseOrganizationViewSet):
    queryset = Taluka.objects.filter(is_deleted=False).select_related('district', 'district__state')
    serializer_class = TalukaSerializer
    filterset_fields = ['district', 'district__state', 'is_active']
    search_fields = ['name', 'district__name', 'uuid']
    ordering_fields = ['name', 'created_at']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            OrganizationService.delete_taluka(instance)
            return success_response(None, "Taluka deleted successfully", status.HTTP_200_OK)
        except ValidationError as e:
            return error_response(None, e.message, status.HTTP_400_BAD_REQUEST)


class VillageViewSet(BaseOrganizationViewSet):
    queryset = Village.objects.filter(is_deleted=False).select_related('taluka', 'taluka__district')
    serializer_class = VillageSerializer
    filterset_fields = ['taluka', 'taluka__district', 'is_active']
    search_fields = ['name', 'pin_code', 'taluka__name', 'uuid']
    ordering_fields = ['name', 'created_at']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        OrganizationService.delete_village(instance)
        return success_response(None, "Village deleted successfully", status.HTTP_200_OK)


class DesignationViewSet(BaseOrganizationViewSet):
    queryset = Designation.objects.filter(is_deleted=False)
    serializer_class = DesignationSerializer
    filterset_fields = ['level_scope', 'is_active']
    search_fields = ['title', 'uuid']
    ordering_fields = ['display_order', 'title', 'created_at']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        OrganizationService.delete_designation(instance)
        return success_response(None, "Designation deleted successfully", status.HTTP_200_OK)
