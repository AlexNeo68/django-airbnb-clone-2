import random

from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand
from django.utils.timezone import now
from django_seed import Seed

from lists.models import List
from rooms.models import Room
from users.models import User


class Command(BaseCommand):
    help = 'Seed lists entities'

    def add_arguments(self, parser):
        parser.add_argument('--numbers', type=int, default=10, help='How many lists do you want to create')

    def handle(self, *args, **options):
        numbers = options.get('numbers')

        seeder = Seed.seeder()

        users = User.objects.all()
        rooms = Room.objects.all()

        for i in range(numbers):
            list_created = List.objects.create(
                name=seeder.faker.paragraph(),
                user=random.choice(users),
            )

            list_created.rooms.add(*rooms[random.randint(2, 3):random.randint(8, 20)])

        self.stdout.write(self.style.SUCCESS(f"{numbers} lists created!"))
