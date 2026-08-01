from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ValidationError

from apps.common.responses import success_response, error_response
from apps.common.permissions import IsAdminUserOrSuperAdmin, IsOwnerOrAdmin
from apps.organization.models import State, District, Taluka, Village
from apps.members.models import Member, MemberDocument, MembershipCard, MemberTransferRequest
from apps.members.serializers import (
    MemberListSerializer,
    MemberDetailSerializer,
    MemberRegistrationSerializer,
    MemberDocumentSerializer,
    MemberStatusHistorySerializer,
    MemberTransferRequestSerializer,
    MembershipCardSerializer,
    MemberCardVerificationSerializer
)
from apps.members.services import MemberService


class MemberViewSet(viewsets.ModelViewSet):
    """
    Complete Member Management ViewSet supporting CRUD, Registration, Approval workflows,
    Document management, Membership Card issuance, and Transfer requests.
    """
    queryset = Member.objects.filter(is_deleted=False).select_related(
        'state', 'district', 'taluka', 'village', 'profile', 'membership_card'
    )
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['state', 'district', 'taluka', 'village', 'status', 'gender']
    search_fields = ['first_name', 'last_name', 'membership_number', 'phone_number', 'email', 'uuid']
    ordering_fields = ['first_name', 'created_at', 'approved_at', 'membership_number', 'status']

    def get_serializer_class(self):
        if self.action == 'list':
            return MemberListSerializer
        return MemberDetailSerializer

    def get_permissions(self):
        if self.action in ['register', 'verify_card']:
            return [permissions.AllowAny()]
        if self.action in ['approve', 'reject', 'suspend', 'restore', 'destroy']:
            return [IsAdminUserOrSuperAdmin()]
        if self.action in ['retrieve', 'card', 'documents', 'history', 'transfer']:
            return [permissions.IsAuthenticated()]
        return [IsAdminUserOrSuperAdmin()]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data, "Members retrieved successfully")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(serializer.data, "Member retrieved successfully")

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """Public Member Registration endpoint."""
        serializer = MemberRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            validated_data = serializer.validated_data
            validated_data['state'] = State.objects.get(id=validated_data['state'])
            validated_data['district'] = District.objects.get(id=validated_data['district'])
            validated_data['taluka'] = Taluka.objects.get(id=validated_data['taluka'])
            validated_data['village'] = Village.objects.get(id=validated_data['village'])

            member = MemberService.register_member(validated_data)
            return success_response(
                MemberDetailSerializer(member).data,
                "Member registration submitted successfully. Status: PENDING APPROVAL.",
                status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return error_response(None, str(e.message if hasattr(e, 'message') else e), status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return error_response(None, f"Registration failed: {str(e)}", status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUserOrSuperAdmin])
    def approve(self, request, pk=None):
        """Approves a pending member and activates their digital membership card."""
        member = self.get_object()
        remarks = request.data.get('remarks', 'Approved by Admin')
        member = MemberService.approve_member(member, admin_user=request.user, remarks=remarks)
        return success_response(MemberDetailSerializer(member).data, "Member approved and ID Card issued successfully.")

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUserOrSuperAdmin])
    def reject(self, request, pk=None):
        """Rejects a member registration."""
        member = self.get_object()
        remarks = request.data.get('remarks', 'Registration rejected')
        member = MemberService.reject_member(member, admin_user=request.user, remarks=remarks)
        return success_response(MemberDetailSerializer(member).data, "Member registration rejected.")

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUserOrSuperAdmin])
    def suspend(self, request, pk=None):
        """Suspends a member."""
        member = self.get_object()
        remarks = request.data.get('remarks', 'Membership suspended')
        member = MemberService.suspend_member(member, admin_user=request.user, remarks=remarks)
        return success_response(MemberDetailSerializer(member).data, "Member suspended.")

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUserOrSuperAdmin])
    def restore(self, request, pk=None):
        """Restores a soft-deleted or suspended member."""
        member = self.get_object()
        remarks = request.data.get('remarks', 'Member restored')
        member = MemberService.restore_member(member, admin_user=request.user, remarks=remarks)
        return success_response(MemberDetailSerializer(member).data, "Member restored.")

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticated])
    def documents(self, request, pk=None):
        """Manage documents for a member."""
        member = self.get_object()
        if request.method == 'GET':
            docs = member.documents.all()
            return success_response(MemberDocumentSerializer(docs, many=True).data, "Documents retrieved")
        
        serializer = MemberDocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(member=member)
        return success_response(serializer.data, "Document uploaded successfully", status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def card(self, request, pk=None):
        """Retrieves membership card details."""
        member = self.get_object()
        if not hasattr(member, 'membership_card'):
            return error_response(None, "No membership card generated for this member.", status.HTTP_404_NOT_FOUND)
        return success_response(MembershipCardSerializer(member.membership_card).data, "Membership card details")

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def history(self, request, pk=None):
        """Retrieves status transition history log."""
        member = self.get_object()
        history = member.status_history.all()
        return success_response(MemberStatusHistorySerializer(history, many=True).data, "Status history log")

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticated])
    def transfer(self, request, pk=None):
        """Request or view member transfer requests."""
        member = self.get_object()
        if request.method == 'GET':
            requests_qs = member.transfer_requests.all()
            return success_response(MemberTransferRequestSerializer(requests_qs, many=True).data, "Transfer requests list")

        to_village_id = request.data.get('to_village')
        reason = request.data.get('reason', 'Relocation')
        try:
            to_village = Village.objects.get(id=to_village_id)
            transfer_req = MemberService.request_transfer(member, to_village, reason)
            return success_response(MemberTransferRequestSerializer(transfer_req).data, "Transfer request submitted", status.HTTP_201_CREATED)
        except Village.DoesNotExist:
            return error_response(None, "Destination village not found", status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return error_response(None, e.message, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return success_response(None, "Member soft-deleted successfully", status.HTTP_200_OK)


class VerifyCardView(APIView):
    """
    GET /api/v1/members/verify-card/{qr_token}/
    Public endpoint scanned from Digital Membership Card QR Codes.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, qr_token):
        try:
            card = MembershipCard.objects.select_related('member', 'member__district', 'member__taluka', 'member__village', 'member__profile').get(qr_token=qr_token)
            member = card.member
            
            photo_url = None
            if hasattr(member, 'profile') and member.profile.photo_asset and member.profile.photo_asset.file:
                photo_url = member.profile.photo_asset.file.url

            from django.utils import timezone
            is_valid = (
                card.is_active and 
                member.status == 'APPROVED' and 
                not member.is_deleted and 
                (card.expires_at is None or card.expires_at >= timezone.now())
            )

            data = {
                "is_valid": is_valid,
                "member_name": f"{member.first_name} {member.last_name}",
                "membership_number": member.membership_number or "N/A",
                "status": member.status,
                "photo_url": photo_url,
                "district_name": member.district.name if member.district else "",
                "taluka_name": member.taluka.name if member.taluka else "",
                "village_name": member.village.name if member.village else "",
                "issued_at": card.issued_at
            }
            serializer = MemberCardVerificationSerializer(data=data)
            serializer.is_valid()
            return success_response(serializer.data, "Membership Card verification result")
        except MembershipCard.DoesNotExist:
            return error_response(None, "Invalid QR Code token. Membership Card not found.", status.HTTP_404_NOT_FOUND)
