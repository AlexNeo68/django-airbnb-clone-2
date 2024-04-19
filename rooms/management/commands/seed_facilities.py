from django.core.management import BaseCommand

from rooms.models import Facility


class Command(BaseCommand):
    help = 'Seed facilities entities'

    # def add_arguments(self, parser):
    #     parser.add_argument('--times', type=int, default=10, help='How many times do you want to print - I love you')

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]

        for facility in facilities:
            Facility.objects.create(name=facility)

        self.stdout.write(self.style.SUCCESS("Successfully added Facilities")
)