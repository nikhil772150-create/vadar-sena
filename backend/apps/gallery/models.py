from django.db import models
from apps.common.models import BaseModel, MediaAsset
from apps.events_meetings.models import Event


class GalleryAlbum(BaseModel):
    """Photo albums and media groupings (gallery_albums)."""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cover_asset = models.ForeignKey(MediaAsset, on_delete=models.SET_NULL, null=True, blank=True, related_name='album_covers')
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True, related_name='albums')

    class Meta:
        db_table = 'gallery_albums'
        verbose_name = 'Gallery Album'
        verbose_name_plural = 'Gallery Albums'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class GalleryPhoto(models.Model):
    """Photo items within an Album (gallery_photos)."""
    album = models.ForeignKey(GalleryAlbum, on_delete=models.CASCADE, related_name='photos')
    media_asset = models.ForeignKey(MediaAsset, on_delete=models.CASCADE, related_name='gallery_photos')
    caption = models.CharField(max_length=255, blank=True, null=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gallery_photos'
        ordering = ['display_order', '-created_at']


class GalleryVideo(models.Model):
    """Video embed links (gallery_videos)."""
    album = models.ForeignKey(GalleryAlbum, on_delete=models.CASCADE, related_name='videos', null=True, blank=True)
    title = models.CharField(max_length=255)
    video_url = models.URLField(help_text="YouTube or Vimeo video link")
    platform = models.CharField(max_length=50, default='YouTube')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gallery_videos'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
