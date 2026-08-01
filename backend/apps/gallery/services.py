import logging
from apps.gallery.models import GalleryAlbum, GalleryPhoto, GalleryVideo

logger = logging.getLogger(__name__)


class GalleryService:
    @staticmethod
    def add_photo_to_album(album: GalleryAlbum, media_asset, caption=""):
        photo = GalleryPhoto.objects.create(
            album=album,
            media_asset=media_asset,
            caption=caption
        )
        logger.info(f"[GALLERY PHOTO ADDED] Album: {album.title}")
        return photo

    @staticmethod
    def add_video(title, video_url, album=None, platform="YouTube"):
        video = GalleryVideo.objects.create(
            album=album,
            title=title,
            video_url=video_url,
            platform=platform
        )
        logger.info(f"[GALLERY VIDEO ADDED] Title: {title}")
        return video
