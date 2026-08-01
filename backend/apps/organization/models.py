from django.db import models
from django.core.exceptions import ValidationError
from apps.common.models import BaseModel
from apps.common.enums import HierarchyLevel


class State(BaseModel):
    """Indian State administrative unit entity (org_states)."""
    name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Unique state name"
    )
    code = models.CharField(
        max_length=10,
        unique=True,
        help_text="State ISO/Abbreviation code (e.g., MH, KA)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Status flag"
    )

    class Meta:
        db_table = 'org_states'
        verbose_name = 'State'
        verbose_name_plural = 'States'
        ordering = ['name']

    def clean(self):
        super().clean()
        if self.name:
            self.name = self.name.strip()
        if self.code:
            self.code = self.code.strip().upper()

    def __str__(self):
        return f"{self.name} ({self.code})"


class District(BaseModel):
    """District administrative unit linked to parent State (org_districts)."""
    state = models.ForeignKey(
        State,
        on_delete=models.PROTECT,
        related_name='districts',
        help_text="Parent State"
    )
    name = models.CharField(
        max_length=100,
        db_index=True,
        help_text="District name"
    )
    code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Optional District code"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Status flag"
    )

    class Meta:
        db_table = 'org_districts'
        verbose_name = 'District'
        verbose_name_plural = 'Districts'
        ordering = ['name']
        unique_together = [['state', 'name']]

    def clean(self):
        super().clean()
        if self.name:
            self.name = self.name.strip()

    def __str__(self):
        return f"{self.name}, {self.state.code}"


class Taluka(BaseModel):
    """Taluka / Block unit linked to parent District (org_talukas)."""
    district = models.ForeignKey(
        District,
        on_delete=models.PROTECT,
        related_name='talukas',
        help_text="Parent District"
    )
    name = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Taluka name"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Status flag"
    )

    class Meta:
        db_table = 'org_talukas'
        verbose_name = 'Taluka'
        verbose_name_plural = 'Talukas'
        ordering = ['name']
        unique_together = [['district', 'name']]

    def clean(self):
        super().clean()
        if self.name:
            self.name = self.name.strip()

    def __str__(self):
        return f"{self.name}, {self.district.name}"


class Village(BaseModel):
    """Village / Ward unit linked to parent Taluka (org_villages)."""
    taluka = models.ForeignKey(
        Taluka,
        on_delete=models.PROTECT,
        related_name='villages',
        help_text="Parent Taluka"
    )
    name = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Village name"
    )
    pin_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Pincode"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Status flag"
    )

    class Meta:
        db_table = 'org_villages'
        verbose_name = 'Village'
        verbose_name_plural = 'Villages'
        ordering = ['name']
        unique_together = [['taluka', 'name']]

    def clean(self):
        super().clean()
        if self.name:
            self.name = self.name.strip()

    def __str__(self):
        return f"{self.name}, {self.taluka.name}"


class Designation(BaseModel):
    """Office bearer designation master catalog (master_designations)."""
    title = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Designation title (e.g., President, Vice President)"
    )
    level_scope = models.CharField(
        max_length=20,
        choices=HierarchyLevel.choices,
        default=HierarchyLevel.STATE,
        help_text="Administrative scope tier"
    )
    display_order = models.IntegerField(
        default=0,
        help_text="Sort order priority"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Status flag"
    )

    class Meta:
        db_table = 'org_designations'
        verbose_name = 'Designation'
        verbose_name_plural = 'Designations'
        ordering = ['display_order', 'title']

    def clean(self):
        super().clean()
        if self.title:
            self.title = self.title.strip()

    def __str__(self):
        return f"{self.title} ({self.level_scope})"
