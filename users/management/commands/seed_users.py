from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User


class Command(BaseCommand):  # 이거를 통해서 seed 데이터를 미리 만들어 놓을 수 있음. 가짜 데이터 생성.

    help = "This command creates many users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many users do you want to create?",
        )

    # User에 가짜 데이터 넣는법
    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()  # seeder 사용하려면 pipenv install django_seed 쳐서 설치해야함.
        seeder.add_entity(User, number, {"is_staff": False, "is_superuser": False})
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} users created!"))
