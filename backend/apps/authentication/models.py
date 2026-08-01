import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from apps.common.validators import validate_indian_phone_number
from apps.common.enums import UserType


class UserManager(BaseUserManager):
    """Custom user manager using phone_number as primary authentication identifier."""
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required for user registration.")
        
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_type', UserType.MEMBER)
        
        if extra_fields.get('email'):
            extra_fields['email'] = self.normalize_email(extra_fields['email'])

        user = self.model(phone_number=phone_number, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
            
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', UserType.SUPERADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model representing core identity (auth_users) for BVSMS.
    Supports phone number login, OTP authentication, and RBAC user types.
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        db_index=True,
        validators=[validate_indian_phone_number],
        help_text="Primary login 10-digit Indian phone number"
    )
    email = models.EmailField(
        max_length=254,
        null=True,
        blank=True,
        help_text="Optional user email address"
    )
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.MEMBER,
        db_index=True,
        help_text="User administrative category"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indicates if user account is active"
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Indicates if user can log into Django Admin interface"
    )
    date_joined = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'auth_users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.phone_number} ({self.user_type})"
