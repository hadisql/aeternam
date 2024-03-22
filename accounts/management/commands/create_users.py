from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Relation
from django.contrib.auth.hashers import make_password
from django.core.files import File
import os
import logging
logger = logging.getLogger(__name__)

User = get_user_model()

class Command(BaseCommand):
    help = 'Create users with default password: changez-moi, or custom password'

    def add_arguments(self, parser):
        parser.add_argument('emails', nargs='+', type=str, help='List of emails to create users')
        parser.add_argument('--password', type=str, default='changez-moi', help='Common password for all users')
        parser.add_argument('--relationbetween', action='store_true', help='Create Relation objects between all created users')
        parser.add_argument('--relationwith', type=str, help='Create Relation objects with a specified user (provide the user email)')
        parser.add_argument('--change_existing', action='store_true', help='Change password for existing users if they already exist')
        parser.add_argument('--full_name', type=str, help='Sets the name of the user to save as first and last name')
        parser.add_argument('--inactive', action='store_true', help='Sets the user as inactive')

    def handle(self, *args, **options):
        emails = options['emails']
        password = options['password']
        create_relation_between = options['relationbetween']
        relation_with_email = options['relationwith']
        full_name = options['full_name']
        is_inactive = options['inactive']

        users = []

        # Create users
        for email in emails:
            user, created = User.objects.get_or_create(email=email)
            users.append(user)

            profile_picture = None
            if full_name:
                # Split the full name into first and last names
                first_name, last_name = full_name.split(' ', 1) if ' ' in full_name else (full_name, '')

                if first_name:
                    user.first_name = first_name
                if last_name:
                    user.last_name = last_name

                # Try to find a profile picture based on the user's name
                supported_formats = ['.jpg', '.jpeg', '.png']

                for ext in supported_formats:
                    profile_picture_path = os.path.join('mediafiles', 'fake_profile_pictures', f'{first_name.lower()}_{last_name.lower()}{ext}')
                    if os.path.exists(profile_picture_path):
                        logger.info(f"profile picture path : {profile_picture_path}")
                        profile_picture  = profile_picture_path
                        break
                if profile_picture:
                    with open(profile_picture, 'rb') as f:
                        user.profile_picture.save(os.path.basename(profile_picture), File(f), save=True)

            else:
                # If full name not provided, use the first part as first name
                user.first_name = email.split('@')[0]

            if created or options['change_existing']:
                user.password = make_password(password)

                if is_inactive:
                    user.is_active = False

                user.save()
                if created:
                    self.stdout.write(self.style.SUCCESS(f"User '{email}' created successfully. Full name : {user.get_full_name()}"))
                else:
                    param_dict = {password:"Password updated", full_name: "Name updated", profile_picture: "Profile pic updated"}
                    updated = [descr for param,descr in param_dict.items() if param]

                    # list the different updated parameters when using --change_existing
                    self.stdout.write(self.style.SUCCESS(f"{', '.join(updated)} for existing user '{email}'."))
            else:
                self.stdout.write(self.style.WARNING(f"User '{email}' already exists. Use --change_existing to update the password."))

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
