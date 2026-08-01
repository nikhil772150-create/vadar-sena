import logging
from django.utils import timezone
from django.utils.text import slugify
from apps.news_cms.models import News, NewsStatus

logger = logging.getLogger(__name__)


class NewsCMSService:
    @staticmethod
    def publish_news(news: News):
        news.status = NewsStatus.PUBLISHED
        if not news.published_at:
            news.published_at = timezone.now()
        news.save(update_fields=['status', 'published_at', 'updated_at'])
        logger.info(f"[NEWS PUBLISHED] ID: {news.id} | Title: {news.title}")
        return news

    @staticmethod
    def archive_news(news: News):
        news.status = NewsStatus.ARCHIVED
        news.save(update_fields=['status', 'updated_at'])
        logger.info(f"[NEWS ARCHIVED] ID: {news.id} | Title: {news.title}")
        return news

    @staticmethod
    def generate_unique_slug(model_cls, title, instance_id=None):
        base_slug = slugify(title)
        slug = base_slug
        count = 1
        query = model_cls.objects.filter(slug=slug)
        if instance_id:
            query = query.exclude(id=instance_id)
        while query.exists():
            slug = f"{base_slug}-{count}"
            count += 1
            query = model_cls.objects.filter(slug=slug)
            if instance_id:
                query = query.exclude(id=instance_id)
        return slug
