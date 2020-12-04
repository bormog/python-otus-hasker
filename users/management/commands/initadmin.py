from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from users.models import UserProfile


class Command(BaseCommand):
    help = 'Create admin user by env variables if not exists'

    def handle(self, *args, **options):
        try:
            email = settings.ADMIN_DEFAULT_EMAIL
            password = settings.ADMIN_DEFAULT_PASSWORD
        except AttributeError:
            raise CommandError('email and password not exists in settings')

        if not email or not password:
            raise CommandError('email and password cant be empty')

        username, _, _ = email.partition('@')

        exists = UserProfile.objects.filter(email=email, username=username).exists()
        if exists:
            self.stdout.write('User already exists')
            return

        try:
            UserProfile.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
        except Exception as e:
            raise CommandError(str(e))
