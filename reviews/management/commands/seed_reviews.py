import random

from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand
from django.utils.timezone import now
from django_seed import Seed

from reviews.models import Review
from rooms.models import Room
from users.models import User


class Command(BaseCommand):
    help = 'Seed reviews entities'

    def add_arguments(self, parser):
        parser.add_argument('--numbers', type=int, default=10, help='How many reviews do you want to create')

    def handle(self, *args, **options):
        numbers = options.get('numbers')

        seeder = Seed.seeder()

        users = User.objects.all()
        rooms = Room.objects.all()

        for i in range(numbers):
            Review.objects.create(
                review=seeder.faker.paragraph(),
                cleanliness=random.randint(1, 5),
                accuracy=random.randint(1, 5),
                check_in=random.randint(1, 5),
                communication=random.randint(1, 5),
                location=random.randint(1, 5),
                value=random.randint(1, 5),
                user=random.choice(users),
                room=random.choice(rooms),
            )

        self.stdout.write(self.style.SUCCESS(f"{numbers} reviews created!"))
