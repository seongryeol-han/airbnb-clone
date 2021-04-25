import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_models
from users import models as user_models
from rooms import models as room_models


class Command(BaseCommand):  # 이거를 통해서 seed 데이터를 미리 만들어 놓을 수 있음. 가짜 데이터 생성.

    help = "This command creates many lists"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many lists do you want to create?",
        )

    # User에 가짜 데이터 넣는법
    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()  # seeder 사용하려면 pipenv install django_seed 쳐서 설치해야함.
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        seeder.add_entity(
            list_models.List,
            number,
            {
                "user": lambda x: random.choice(users),
            },
        )
        created_photos = seeder.execute()
        cleaned = flatten(list(created_photos.values()))
        for pk in cleaned:
            list_model = list_models.List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]
            list_model.rooms.add(*to_add)

        self.stdout.write(self.style.SUCCESS(f"{number} lists created!"))
