from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.gallery.views import GalleryAlbumViewSet, GalleryVideoViewSet

router = DefaultRouter()
router.register('albums', GalleryAlbumViewSet, basename='album')
router.register('videos', GalleryVideoViewSet, basename='video')

urlpatterns = [
    path('', include(router.urls)),
]
