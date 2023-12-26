from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Relation


User = get_user_model()

class Command(BaseCommand):
    help = 'Create users with default password: changez-moi, or custom password'

    def add_arguments(self, parser):
        parser.add_argument('emails', nargs='+', type=str, help='List of emails to create users')
        parser.add_argument('--password', type=str, default='changez-moi', help='Common password for all users')
        parser.add_argument('--relationbetween', action='store_true', help='Create Relation objects between all created users')
        parser.add_argument('--relationwith', type=str, help='Create Relation objects with a specified user (provide the user email)')

    def handle(self, *args, **options):
        emails = options['emails']
        password = options['password']
        create_relation_between = options['relationbetween']
        relation_with_email = options['relationwith']

        users = []

        # Create users
        for email in emails:
            user, created = User.objects.get_or_create(email=email)
            users.append(user)

            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"User '{email}' created successfully."))
            else:
                self.stdout.write(self.style.WARNING(f"User '{email}' already exists."))

        # Create Relation objects between all created users
        if create_relation_between:
            for user1 in users:
                for user2 in users:
                    if user1 != user2:
                        Relation.objects.get_or_create(user_receiving=user1, user_sending=user2)
                        self.stdout.write(self.style.SUCCESS(f"Relation created between '{user1.email}' and '{user2.email}'."))

        # Create Relation objects with a specified user
        if relation_with_email:
            try:
                target_user = User.objects.get(email=relation_with_email)
                for user in users:
                    if user != target_user:
                        Relation.objects.get_or_create(user_receiving=user, user_sending=target_user)
                        self.stdout.write(self.style.SUCCESS(f"Relation created between '{user.email}' and '{target_user.email}'."))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"User with email '{relation_with_email}' does not exist."))
