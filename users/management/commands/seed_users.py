from django.core.management import BaseCommand
from django_seed import Seed

from users.models import User


class Command(BaseCommand):
    help = 'Seed users entities'

    def add_arguments(self, parser):
        parser.add_argument('--numbers', type=int, default=10, help='How many users do you want to create')

    def handle(self, *args, **options):

        numbers = options.get('numbers')

        seeder = Seed.seeder()

        seeder.add_entity(User, numbers, {
            "is_staff": False,
            "is_superuser": False
        })

        seeder.execute()

        self.stdout.write(self.style.SUCCESS("Successfully added Users"))
