from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):  # 이거를 통해서 seed 데이터를 미리 만들어 놓을 수 있음.

    help = "This command creates facilities"

    #    def add_arguments(self, parser):
    #   parser.add_argument(
    #       "--times",
    #       help="How many times do you want me to tell you that I love you?",
    #   )

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        for f in facilities:
            Facility.objects.create(name=f)
        self.stdout.write(self.style.SUCCESS(f"{len(facilities)} facilities created!"))
