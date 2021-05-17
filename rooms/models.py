# 파이썬에서 가져오는거
from django.db import models  # 장고관한거
from django.urls import reverse  # absolure url 쓸 때 이거 import
from django_countries.fields import CountryField  # 외부 라이브러리
from core import models as core_models  # 내 파일에서 가져오는거

# Create your models here.
class AbstractItem(core_models.TimeStampedModel):
    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """ RoomType Object Definition"""

    class Meta:
        verbose_name = "Room Type"


class Amenity(AbstractItem):

    """ Amenity Object Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """ Facility Model Definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """ HouseRule Model Definition"""

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):
    """ Photo Model Definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField(
        upload_to="room_photos"
    )  # /uploads 폴더 안에 room_photos 폴더에다가 사진을 넣을것이다.
    room = models.ForeignKey(
        "Room", related_name="photos", on_delete=models.CASCADE
    )  # "Room"이라고 한 이유는 str로 읽어들일 수 있기 때문. 어차피.

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField(help_text="How many people will be staying?")
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User",
        related_name="rooms",  # (ForeignKey) related_name은 User가 room 정보를 가져올때 그냥 han.rooms.all() 이렇게. (rooms_set을 안써도됨.)
        on_delete=models.CASCADE,  # on_delete는 아이디가 삭제될때 관련된 room정보들도 다 같이 삭제
    )  # model과 model 연결, 일대다 관계임
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField(
        "Amenity", related_name="rooms", blank=True
    )  # Amenity에 shower가 있다면, shower.rooms하면 shower를 가진 room을 다 부르는거네.
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    # 이걸 해야지 rooms 이름이 나타난다.
    def __str__(self):
        return self.name

    # 이게 무슨 의미냐면, 이 class를 save해주는 method인데.
    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)
        # 이게 진짜 save이고, 이거 전에 다른걸 명령하면 save 전에 그걸 먼저 실행한다.

    def get_absolute_url(self):  # admin에서 해당 url로 갈 수 있는 버틑을 만들어 준다.
        return reverse(
            "rooms:detail", kwargs={"pk": self.pk}
        )  # 여기서 pk는 urls쓴 pk랑 같아야 한다.

    def total_rating(self):
        all_reviews = self.reviews.all()  # room의 모든 reviews 숫자 세주려고..
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            all_ratings_average = all_ratings / len(all_reviews)
            return round(all_ratings_average, 2)
        return 0

    def all_photo(self):
        photo = self.photos.all()  # ,를 찍으면 파이썬이 첫번째 array 요소를 원하는구나라는것을 알게됨
        print(photo[0].file.url)
        return photo
