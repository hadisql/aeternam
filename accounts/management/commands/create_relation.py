from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from accounts.models import Relation, CustomUser
import logging
logger = logging.getLogger(__name__)

User = get_user_model()

class Command(BaseCommand):
    help = 'Create relation between two given users'

    def add_arguments(self, parser):
        parser.add_argument('email_1', type=str, help='first user to give relation to')
        parser.add_argument('email_2', type=str, help='second user to give relation to')

    def handle(self, *args, **options):
        email_1 = options['email_1']
        email_2 = options['email_2']

        user_1 = CustomUser.objects.filter(email=email_1).first()
        user_2 = CustomUser.objects.filter(email=email_2).first()

        if user_1 and user_2:
            relation_1 = Relation.objects.filter(user_receiving=user_1, user_sending=user_2).first()
            relation_2 = Relation.objects.filter(user_receiving=user_2, user_sending=user_1).first()

            if relation_1 or relation_2:
                self.stdout.write(self.style.WARNING(f"Relation already exist."))

            # relation, created = Relation.objects.get_or_create(user_receiving=user_1, user_sending=user_2)
            else:
                Relation.objects.create(user_receiving=user_1, user_sending=user_2)
                self.stdout.write(self.style.SUCCESS(f"Relation created between '{email_1}' and '{email_2}'."))



        elif user_1 is None:
            self.stdout.write(self.style.ERROR(f"user {email_1} does not exist."))
        elif user_2 is None:
            self.stdout.write(self.style.ERROR(f"user {email_2} does not exist."))
