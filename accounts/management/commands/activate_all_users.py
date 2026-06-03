from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Activates all user accounts in the database'

    def handle(self, *args, **options):
        count = User.objects.filter(is_active=False).update(is_active=True)
        self.stdout.write(
            self.style.SUCCESS(f'Successfully activated {count} user(s)')
        )
        
        # Also show all users
        all_users = User.objects.all()
        self.stdout.write('\nAll users in database:')
        for user in all_users:
            self.stdout.write(f'  - {user.email} (active: {user.is_active}, role: {user.role})')
            