from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create users with password: changez-moi'

    def add_arguments(self, parser):
        parser.add_argument('emails', nargs='+', type=str, help='List of emails to create users')
        parser.add_argument('--password', type=str, default='changez-moi', help='Common password for all users')


    def handle(self, *args, **options):
        emails = options['emails']
        password = options['password']

        for email in emails:
            user, created = User.objects.get_or_create(email=email)

            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"User '{email}' created successfully."))
            else:
                self.stdout.write(self.style.WARNING(f"User '{email}' already exists."))
