import random

from django.core.management import BaseCommand
from django_seed import Seed

from users.models import User
from rooms.models import Room, RoomType, Amenity, Facility, HouseRule, Photo


class Command(BaseCommand):
    help = 'Seed rooms entities'

    def add_arguments(self, parser):
        parser.add_argument('--numbers', type=int, default=10, help='How many rooms do you want to create')

    def handle(self, *args, **options):

        numbers = options.get('numbers')

        seeder = Seed.seeder(locale='ru_RU')

        users = User.objects.all()
        room_types = RoomType.objects.all()
        amenities = Amenity.objects.all()
        facilities = Facility.objects.all()
        house_rules = HouseRule.objects.all()

        for i in range(numbers):

            user = random.choice(users)

            room = Room.objects.create(
                name=seeder.faker.address(),
                description=seeder.faker.address(),
                country=seeder.faker.country(),
                city=seeder.faker.city(),
                price=random.randint(1000, 10000),
                address=seeder.faker.address(),
                guests=random.randint(1, 20),
                beds=random.randint(1, 5,),
                bedrooms=random.randint(1, 5),
                baths=random.randint(1, 5),
                check_in=seeder.faker.time(),
                check_out=seeder.faker.time(),
                instant_book=random.choice([0, 1]),
                host=user,
                room_type=random.choice(room_types),
            )

            for p in range(random.randint(10, 17)):
                Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1, 31)}.webp"
                )

            for a in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2:
                    room.amenities.add(a)

            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2:
                    room.facilities.add(f)

            for r in house_rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2:
                    room.house_rules.add(r)

        self.stdout.write(self.style.SUCCESS(f"{numbers} rooms created!"))
