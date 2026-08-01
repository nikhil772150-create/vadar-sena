from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.gallery.models import GalleryAlbum, GalleryVideo
from apps.gallery.services import GalleryService


class GalleryTest(TestCase):
    def setUp(self):
        self.album = GalleryAlbum.objects.create(title="State Convention 2026", description="Photos of convention")
        self.client = APIClient()

    def test_gallery_album_list_api(self):
        response = self.client.get('/api/v1/gallery/albums/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_gallery_video_service(self):
        video = GalleryService.add_video("Keynote Speech", "https://youtube.com/watch?v=example", album=self.album)
        self.assertEqual(GalleryVideo.objects.count(), 1)
        self.assertEqual(video.platform, "YouTube")
