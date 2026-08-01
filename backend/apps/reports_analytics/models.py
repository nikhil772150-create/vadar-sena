from django.db import models
from apps.organization.models import State, District


class RegionalStats(models.Model):
    """
    Pre-aggregated regional analytics table (analytics_regional_stats)
    for fast dashboard rendering without expensive live DB joins.
    """
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True, related_name='analytics')
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True, related_name='analytics')
    total_members = models.IntegerField(default=0)
    approved_members = models.IntegerField(default=0)
    pending_members = models.IntegerField(default=0)
    suspended_members = models.IntegerField(default=0)
    total_donations_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'analytics_regional_stats'
        verbose_name = 'Regional Stats'
        verbose_name_plural = 'Regional Stats'

    def __str__(self):
        region = self.district.name if self.district else (self.state.name if self.state else "National")
        return f"Stats for {region} ({self.total_members} members)"
