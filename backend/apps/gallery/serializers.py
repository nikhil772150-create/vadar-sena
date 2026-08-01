from rest_framework import serializers
from apps.gallery.models import GalleryAlbum, GalleryPhoto, GalleryVideo


class GalleryPhotoSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = GalleryPhoto
        fields = ('id', 'album', 'media_asset', 'photo_url', 'caption', 'display_order', 'created_at')

    def get_photo_url(self, obj):
        if obj.media_asset and obj.media_asset.file:
            return obj.media_asset.file.url
        return None


class GalleryVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryVideo
        fields = ('id', 'album', 'title', 'video_url', 'platform', 'created_at')


class GalleryAlbumSerializer(serializers.ModelSerializer):
    cover_url = serializers.SerializerMethodField()
    photos = GalleryPhotoSerializer(many=True, read_only=True)
    videos = GalleryVideoSerializer(many=True, read_only=True)

    class Meta:
        model = GalleryAlbum
        fields = ('id', 'uuid', 'title', 'description', 'cover_asset', 'cover_url', 'event', 'photos', 'videos', 'created_at')
        read_only_fields = ('id', 'uuid', 'created_at')

    def get_cover_url(self, obj):
        if obj.cover_asset and obj.cover_asset.file:
            return obj.cover_asset.file.url
        return None
