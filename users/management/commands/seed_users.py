import random

from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand
from django.utils.timezone import now
from django_seed import Seed

from users.models import User


class Command(BaseCommand):
    help = 'Seed users entities'

    def add_arguments(self, parser):
        parser.add_argument('--numbers', type=int, default=10, help='How many users do you want to create')

    def handle(self, *args, **options):

        numbers = options.get('numbers')

        seeder = Seed.seeder()

        # seeder.add_entity(User, numbers, {
        #     "is_staff": False,
        #     "is_superuser": False
        # })

        for i in range(numbers):
            User.objects.create(
                username=seeder.faker.user_name(),
                first_name=seeder.faker.first_name(),
                last_name=seeder.faker.last_name(),
                email=seeder.faker.email(),
                is_staff=False,
                is_superuser=False,
                is_active=True,
                date_joined=now(),
                bio=seeder.faker.paragraph(),
                gender=random.choices([User.MALE, User.FEMALE])[0],
                birthday=seeder.faker.date_of_birth(),
                currency=random.choices([User.RUB, User.USD])[0],
                language=random.choices([User.EN, User.RU])[0],
                superhost=False,
                password=make_password('12345')
            )

        self.stdout.write(self.style.SUCCESS(f"{numbers} users created!"))
