from django.db import models


class UserType(models.TextChoices):
    MEMBER = 'MEMBER', 'Member'
    ADMIN = 'ADMIN', 'Admin'
    SUPERADMIN = 'SUPERADMIN', 'Super Admin'


class MemberStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending Approval'
    APPROVED = 'APPROVED', 'Approved'
    REJECTED = 'REJECTED', 'Rejected'
    SUSPENDED = 'SUSPENDED', 'Suspended'


class HierarchyLevel(models.TextChoices):
    STATE = 'STATE', 'State Level'
    DISTRICT = 'DISTRICT', 'District Level'
    TALUKA = 'TALUKA', 'Taluka Level'
    VILLAGE = 'VILLAGE', 'Village Level'


class VerificationStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    VERIFIED = 'VERIFIED', 'Verified'
    REJECTED = 'REJECTED', 'Rejected'
