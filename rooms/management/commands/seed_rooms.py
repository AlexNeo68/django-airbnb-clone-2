from django.core.management import BaseCommand
from django_seed import Seed

from users.models import User
from rooms.models import Room, RoomType


class Command(BaseCommand):
    help = 'Seed rooms entities'

    def add_arguments(self, parser):
        parser.add_argument('--numbers', type=int, default=10, help='How many rooms do you want to create')

    def handle(self, *args, **options):

        numbers = options.get('numbers')

        seeder = Seed.seeder(locale='ru_RU')
        seeder.add_entity(Room, numbers)

        # print(seeder.faker.address())
        #
        # seeder.add_entity(User, numbers, {
        #     "is_staff": False,
        #     "is_superuser": False
        # })
        #
        seeder.execute()

        # self.stdout.write(self.style.SUCCESS(f"{numbers} rooms created!"))
