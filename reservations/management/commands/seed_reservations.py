import random
from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand
from django.utils.timezone import now
from django_seed import Seed

from reservations.models import Reservation
from rooms.models import Room
from users.models import User


class Command(BaseCommand):
    help = 'Seed reservations entities'

    def add_arguments(self, parser):
        parser.add_argument('--numbers', type=int, default=10, help='How many reservations do you want to create')

    def handle(self, *args, **options):
        numbers = options.get('numbers')

        seeder = Seed.seeder()

        users = User.objects.all()
        rooms = Room.objects.all()

        for i in range(numbers):
            Reservation.objects.create(
                status=random.choice(
                    [Reservation.STATUS_PENDING, Reservation.STATUS_CONFIRMED, Reservation.STATUS_CANCELED]),
                check_in=datetime.now(),
                check_out=datetime.now() + timedelta(days=random.randint(4, 21)),
                guest=random.choice(users),
                room=random.choice(rooms),
            )

        self.stdout.write(self.style.SUCCESS(f"{numbers} reservations created!"))
