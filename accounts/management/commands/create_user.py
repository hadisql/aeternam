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
        parser.add_argument('email', type=str, help='Email of user to create')
        parser.add_argument('--password', type=str, default='changez-moi', help='Password for the user')
        parser.add_argument('--change_existing', action='store_true', help='Change password for existing users if they already exist')
        parser.add_argument('--full_name', type=str, help='Sets the name of the user to save as first and last name')
        parser.add_argument('--inactive', action='store_true', help='Sets the user as inactive')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        full_name = options['full_name']
        is_inactive = options['inactive']

        users = []

        print(f"full_name : {full_name}")
        print(f"email : {email}")

        # Create users
        user, created = User.objects.get_or_create(email=email)
        users.append(user)

        if created or options['change_existing']:
            if created or password:
                # when changing: changes password only if --password passed explicitely / when creating : apply defzault password or passed argument
                user.password = make_password(password)

            if full_name:
                # Split the full name into first and last names
                first_name, last_name = full_name.split(' ', 1) if ' ' in full_name else (full_name, '')

                if first_name:
                    user.first_name = first_name
                if last_name:
                    user.last_name = last_name

            if is_inactive:
                user.is_active = False

            user.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f"User '{email}' created successfully. Full name : {user.get_full_name()}"))
            else:
                param_dict = {password:"Password updated", full_name: "Name updated", password: "Password is set", is_inactive:"User set to inactive"}
                updated = [descr for param,descr in param_dict.items() if param]

                # list the different updated parameters when using --change_existing
                self.stdout.write(self.style.SUCCESS(f"{', '.join(updated)} for existing user '{email}'."))
        else:
            self.stdout.write(self.style.WARNING(f"User '{email}' already exists. Use --change_existing to update the data."))
