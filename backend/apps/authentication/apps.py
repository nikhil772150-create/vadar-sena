from django.apps import AppConfig
from django.db.models.signals import post_migrate

def auto_seed_admin(sender, **kwargs):
    from apps.authentication.models import User
    try:
        user, created = User.objects.get_or_create(phone_number='9876543210')
        user.set_password('adminpassword123')
        user.user_type = 'SUPERADMIN'
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
    except Exception:
        pass

class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.authentication'

    def ready(self):
        post_migrate.connect(auto_seed_admin, sender=self)
