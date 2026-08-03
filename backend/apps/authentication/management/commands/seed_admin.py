from django.core.management.base import BaseCommand
from apps.authentication.models import User

class Command(BaseCommand):
    help = 'Seeds initial default SuperAdmin user for Bharatiya Vadar Sena (BVS)'

    def handle(self, *args, **options):
        phone_number = '9876543210'
        password = 'adminpassword123'

        user, created = User.objects.get_or_create(phone_number=phone_number)
        user.set_password(password)
        user.user_type = 'SUPERADMIN'
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created SuperAdmin user {phone_number}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Successfully updated password for SuperAdmin user {phone_number}'))
