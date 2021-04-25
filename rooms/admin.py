# 여기에 넣어줘야 admin 패널에서 보인다.


from django.contrib import admin
from django.utils.html import mark_safe
from . import models


# Register your models here.


@admin.register(models.RoomType, models.Facility, models.HouseRule, models.Amenity)
class ItemAdmin(admin.ModelAdmin):

    """ Item Adim Definition"""

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()  # obj를 쓰고 있는 room들을 불러 오는거다.


class PhotoInline(admin.TabularInline):
    model = models.Photo  # Photo 모델을 넣고.. room에다가 사진 올리는거 연동


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Defintion"""

    inlines = (PhotoInline,)  # Photo 모델을 넣고.. room에다가 사진 올리는거 연동

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "city", "address", "price")},
        ),
        (
            "Times",
            {"fields": ("check_in", "check_out", "instant_book")},
        ),
        (
            "More About the Space",
            {
                "classes": ("collapse",),  # 접었다 폈다 할 수 있음.
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        (
            "Space",
            {"fields": ("guests", "beds", "bedrooms", "baths")},
        ),
        (
            "Space",
            {"fields": ("host",)},
        ),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    ordering = ("name", "price", "bedrooms")

    list_filter = (
        "instant_book",
        "host__superhost",
        "host__gender",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    raw_id_fields = ("host",)  # username 저장할때 search 기능이 있다..

    # admin에서 검색기능 추가
    search_fields = (
        "city",
        "^host__username",  # host : users.user 에서 username을 가져온다.
    )

    # manytomany에서만 사용 가능.
    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    def count_amenities(
        self, obj
    ):  # admin 안에 func에서 첫번째는 class를 받고, 두번째 obj는 그 admin에서 보이는 raw를 받는다.
        return obj.amenities.count()
        # admin에서 count_amenities 항목이 추가됨.

    def count_photos(self, obj):
        return (
            obj.photos.count()
        )  # 한 room에 등록된 사진 개수를 카운트, photos는 어디서 가지고 왔냐면, model에서 Photo의 FK로 가져온것임.

    count_photos.short_description = "Photo Count"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ """

    list_display = (
        "__str__",
        "get_thumbnail",
    )

    def get_thumbnail(self, obj):
        return mark_safe(
            f'<img width="50px" src="{obj.file.url}"/>'
        )  # mark_safe는 안전한 string이야!, 맨 위에서 import 해줘야한다.

    get_thumbnail.short_description = "Thumbnail"
