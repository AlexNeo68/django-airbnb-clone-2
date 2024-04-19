from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Tell you that program love you'

    def add_arguments(self, parser):
        parser.add_argument('--times', type=int, default=10, help='How many times do you want to print - I love you')

    def handle(self, *args, **options):
        times = options.get('times')
        for i in range(0, times):
            self.stdout.write(self.style.SUCCESS('I Love You!'))
