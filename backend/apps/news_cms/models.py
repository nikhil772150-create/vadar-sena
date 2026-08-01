from django.db import models
from django.utils import timezone
from apps.common.models import BaseModel, MediaAsset


class NewsStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    PUBLISHED = 'PUBLISHED', 'Published'
    ARCHIVED = 'ARCHIVED', 'Archived'


class NewsCategory(BaseModel):
    """Category taxonomy for News articles (cms_news_categories)."""
    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'cms_news_categories'
        verbose_name = 'News Category'
        verbose_name_plural = 'News Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class News(BaseModel):
    """News article and press release entity (cms_news)."""
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='news')
    content = models.TextField(help_text="Rich Text article content")
    cover_asset = models.ForeignKey(MediaAsset, on_delete=models.SET_NULL, null=True, blank=True, related_name='news_covers')
    status = models.CharField(max_length=20, choices=NewsStatus.choices, default=NewsStatus.DRAFT, db_index=True)
    is_pinned = models.BooleanField(default=False, help_text="Pin to top of news feed")
    is_featured = models.BooleanField(default=False, help_text="Feature on home page")
    published_at = models.DateTimeField(null=True, blank=True)
    meta_title = models.CharField(max_length=150, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'cms_news'
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = ['-is_pinned', '-published_at', '-created_at']

    def __str__(self):
        return self.title


class StaticPage(BaseModel):
    """Dynamic static website page content (cms_pages)."""
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    title = models.CharField(max_length=200)
    content = models.TextField(help_text="Rich HTML/Markdown content")
    meta_title = models.CharField(max_length=150, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'cms_pages'
        verbose_name = 'Static Page'
        verbose_name_plural = 'Static Pages'

    def __str__(self):
        return self.title


class FAQ(BaseModel):
    """Frequently Asked Questions catalog (cms_faqs)."""
    question = models.CharField(max_length=255)
    answer = models.TextField()
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'cms_faqs'
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.question


class HomepageBanner(BaseModel):
    """Homepage slider and notification banners (cms_banners)."""
    title = models.CharField(max_length=200)
    image_asset = models.ForeignKey(MediaAsset, on_delete=models.PROTECT, related_name='banners')
    link_url = models.URLField(blank=True, null=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'cms_banners'
        verbose_name = 'Homepage Banner'
        verbose_name_plural = 'Homepage Banners'
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.title
