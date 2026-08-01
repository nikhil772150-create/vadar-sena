from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ValidationError

from apps.common.responses import success_response, error_response
from apps.common.permissions import IsAdminUserOrSuperAdmin
from apps.donations.models import Donation, VerificationStatus
from apps.donations.serializers import DonationSerializer, DonationCreateSerializer
from apps.donations.services import DonationService


class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.filter(is_deleted=False).select_related('receipt_asset', 'state', 'district', 'verified_by')
    serializer_class = DonationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'payment_method', 'state', 'district']
    search_fields = ['donor_name', 'phone_number', 'transaction_id', 'upi_ref', 'purpose']
    ordering_fields = ['amount', 'created_at', 'verified_at']

    def get_permissions(self):
        if self.action in ['create', 'submit']:
            return [permissions.AllowAny()]
        if self.action in ['list', 'retrieve', 'my_donations']:
            return [permissions.IsAuthenticated()]
        return [IsAdminUserOrSuperAdmin()]

    def create(self, request, *args, **kwargs):
        serializer = DonationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            donation = DonationService.create_donation(serializer.validated_data)
            return success_response(
                DonationSerializer(donation).data,
                "Donation submitted successfully. Pending verification.",
                status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return error_response(None, e.message, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUserOrSuperAdmin])
    def verify(self, request, pk=None):
        donation = self.get_object()
        remarks = request.data.get('remarks', 'Verified by Admin')
        donation = DonationService.verify_donation(donation, admin_user=request.user, remarks=remarks)
        return success_response(DonationSerializer(donation).data, "Donation verified successfully.")

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUserOrSuperAdmin])
    def reject(self, request, pk=None):
        donation = self.get_object()
        remarks = request.data.get('remarks', 'Payment rejected')
        donation = DonationService.reject_donation(donation, admin_user=request.user, remarks=remarks)
        return success_response(DonationSerializer(donation).data, "Donation rejected.")

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_donations(self, request):
        if hasattr(request.user, 'member_profile'):
            qs = self.queryset.filter(member=request.user.member_profile)
        else:
            qs = self.queryset.filter(phone_number=request.user.phone_number)
        serializer = self.get_serializer(qs, many=True)
        return success_response(serializer.data, "My donations history")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return success_response(None, "Donation soft-deleted successfully")
