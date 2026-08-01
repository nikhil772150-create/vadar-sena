from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from apps.common.responses import success_response, error_response
from apps.common.permissions import IsAdminUserOrSuperAdmin
from apps.gallery.models import GalleryAlbum, GalleryPhoto, GalleryVideo
from apps.gallery.serializers import GalleryAlbumSerializer, GalleryPhotoSerializer, GalleryVideoSerializer
from apps.gallery.services import GalleryService


class GalleryAlbumViewSet(viewsets.ModelViewSet):
    queryset = GalleryAlbum.objects.filter(is_deleted=False).prefetch_related('photos', 'videos')
    serializer_class = GalleryAlbumSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdminUserOrSuperAdmin()]

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUserOrSuperAdmin])
    def add_photo(self, request, pk=None):
        album = self.get_object()
        media_asset_id = request.data.get('media_asset')
        caption = request.data.get('caption', '')
        
        if not media_asset_id:
            return error_response(None, "media_asset is required.", status.HTTP_400_BAD_REQUEST)

        photo = GalleryService.add_photo_to_album(album, media_asset_id, caption)
        return success_response(GalleryPhotoSerializer(photo).data, "Photo added to album successfully.", status.HTTP_201_CREATED)


class GalleryVideoViewSet(viewsets.ModelViewSet):
    queryset = GalleryVideo.objects.all()
    serializer_class = GalleryVideoSerializer
    search_fields = ['title']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdminUserOrSuperAdmin()]
