from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from arithmetica.models import UserInfo


class Command(BaseCommand):
    help = 'Populate UserInfo based on User model data'

    def handle(self, *args, **options):
        for user in User.objects.all():
            if not UserInfo.objects.filter(user=user).exists():
                UserInfo.objects.create(user=user, credits=3000)

        self.stdout.write(self.style.SUCCESS('Successfully populated UserInfo'))
