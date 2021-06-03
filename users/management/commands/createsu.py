from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):  # 이거를 통해서 seed 데이터를 미리 만들어 놓을 수 있음. 가짜 데이터 생성.

    help = "This command creates superuser"

    # User에 가짜 데이터 넣는법
    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username="ebadmin")
        if not admin:
            User.objects.create_superuser("ebadmin", "gkstjdfuf17@posely.com", "123123")
            self.stdout.write(self.style.SUCCESS(f"Superuser created!"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser Exists"))