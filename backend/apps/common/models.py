import uuid
from django.db import models
from django.utils import timezone


class ActiveManager(models.Manager):
    """Queryset manager filtering out soft-deleted records."""
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    """
    Abstract base model providing UUID identity, audit timestamps, 
    and soft-delete capability across all BVSMS entities.
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
        help_text="Public-facing unique identifier"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Timestamp when record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when record was last updated"
    )
    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Soft-delete status flag"
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when record was soft-deleted"
    )

    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def soft_delete(self):
        """Perform soft delete by marking flag and timestamp."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])

    def restore(self):
        """Restore a soft-deleted record."""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=['is_deleted', 'deleted_at'])


class MediaAsset(models.Model):
    """
    Centralized media asset model (media_assets) for photos, documents, and uploads.
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )
    file = models.FileField(
        upload_to='uploads/%Y/%m/%d/',
        help_text="Uploaded file asset"
    )
    file_name = models.CharField(
        max_length=255,
        help_text="Original file name"
    )
    mime_type = models.CharField(
        max_length=100,
        blank=True,
        help_text="MIME type"
    )
    file_size = models.BigIntegerField(
        default=0,
        help_text="File size in bytes"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'media_assets'
        verbose_name = 'Media Asset'
        verbose_name_plural = 'Media Assets'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.file_name} ({self.file_size} bytes)"
