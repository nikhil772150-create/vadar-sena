import logging
from django.core.exceptions import ValidationError
from apps.organization.models import State, District, Taluka, Village, Designation

logger = logging.getLogger(__name__)


class OrganizationService:
    """
    Business service encapsulating hierarchy operations and deletion constraints.
    """

    @staticmethod
    def validate_case_insensitive_unique(model_cls, name_field, value, parent_filter=None, current_id=None):
        """
        Validates case-insensitive and whitespace-trimmed uniqueness for entity names.
        """
        clean_val = value.strip()
        query = model_cls.objects.filter(**{f"{name_field}__iexact": clean_val})
        
        if parent_filter:
            query = query.filter(**parent_filter)
            
        if current_id:
            query = query.exclude(id=current_id)
            
        if query.exists():
            raise ValidationError(f"{model_cls._meta.verbose_name} with name '{clean_val}' already exists in this scope.")
        return clean_val

    @staticmethod
    def delete_state(state: State):
        """Soft-deletes a state after checking child district constraints."""
        if state.districts.filter(is_deleted=False).exists():
            raise ValidationError("Cannot delete State while active child Districts exist.")
        state.soft_delete()
        logger.info(f"[ORG DELETED] State: {state.name} (UUID: {state.uuid})")
        return state

    @staticmethod
    def delete_district(district: District):
        """Soft-deletes a district after checking child taluka constraints."""
        if district.talukas.filter(is_deleted=False).exists():
            raise ValidationError("Cannot delete District while active child Talukas exist.")
        district.soft_delete()
        logger.info(f"[ORG DELETED] District: {district.name} (UUID: {district.uuid})")
        return district

    @staticmethod
    def delete_taluka(taluka: Taluka):
        """Soft-deletes a taluka after checking child village constraints."""
        if taluka.villages.filter(is_deleted=False).exists():
            raise ValidationError("Cannot delete Taluka while active child Villages exist.")
        taluka.soft_delete()
        logger.info(f"[ORG DELETED] Taluka: {taluka.name} (UUID: {taluka.uuid})")
        return taluka

    @staticmethod
    def delete_village(village: Village):
        """Soft-deletes a village."""
        village.soft_delete()
        logger.info(f"[ORG DELETED] Village: {village.name} (UUID: {village.uuid})")
        return village

    @staticmethod
    def delete_designation(designation: Designation):
        """Soft-deletes a designation."""
        designation.soft_delete()
        logger.info(f"[ORG DELETED] Designation: {designation.title} (UUID: {designation.uuid})")
        return designation
