from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
# AbstractUser은 기존에 장고가 가지고 있던거임.
class User(AbstractUser):

    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "male"),
        (GENDER_FEMALE, "female"),
        (GENDER_OTHER, "other"),
    )

    LANGUAGE_ENGRLISH = "en"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICES = ((LANGUAGE_ENGRLISH, "English"), (LANGUAGE_KOREAN, "Korean"))

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURENCY_CHOICES = ((CURRENCY_USD, "USD"), (CURRENCY_KRW, "KRW"))

    avatar = models.ImageField(
        upload_to="avatars",  # /uploads 폴더 안데 avatars 폴더에다가 사진을 넣을것임.
        blank=True,
    )
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    bio = models.TextField(
        default="", blank=True
    )  # default를 넣는 이유는 데이터베이스 column에 빈칸이 없도록..

    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2, blank=True)
    currency = models.CharField(choices=CURENCY_CHOICES, max_length=3, blank=True)
    superhost = models.BooleanField(default=False)
