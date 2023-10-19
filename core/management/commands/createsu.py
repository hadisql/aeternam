
from accounts.models import CustomUser
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        if not CustomUser.objects.filter(username='admin').exists():
            CustomUser.objects.create_superuser(
                email='hadisu@example.com',
                password='sansebastian'
            )
        print('Superuser has been created.')
