from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from apps.common.responses import success_response, error_response
from apps.common.permissions import IsAdminUserOrSuperAdmin
from apps.communications.models import ContactInquiry, Notification
from apps.communications.serializers import ContactInquirySerializer, NotificationSerializer
from apps.communications.services import CommunicationsService


class ContactInquiryViewSet(viewsets.ModelViewSet):
    queryset = ContactInquiry.objects.filter(is_deleted=False)
    serializer_class = ContactInquirySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'phone', 'email', 'subject', 'message']
    ordering_fields = ['created_at', 'status']

    def get_permissions(self):
        if self.action in ['create', 'submit']:
            return [permissions.AllowAny()]
        return [IsAdminUserOrSuperAdmin()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        inquiry = CommunicationsService.create_inquiry(**serializer.validated_data)
        return success_response(ContactInquirySerializer(inquiry).data, "Contact message submitted successfully.", status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUserOrSuperAdmin])
    def resolve(self, request, pk=None):
        inquiry = self.get_object()
        inquiry = CommunicationsService.resolve_inquiry(inquiry, request.user)
        return success_response(ContactInquirySerializer(inquiry).data, "Inquiry marked as resolved.")


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient_user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save(update_fields=['is_read'])
        return success_response(NotificationSerializer(notification).data, "Notification marked as read.")
