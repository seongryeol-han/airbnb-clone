from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from rooms import models as room_models


class RoomInline(admin.TabularInline):
    model = room_models.Room


# Register your models here.
@admin.register(
    models.User
)  # models.py에서 User 을 가져오는거지. 그래서 CustomUserAdmin class에서 사용하는거여
class CustomUserAdmin(UserAdmin):  # UserAdmin이 있는 이유는 그냥 장고에서 만들어준 UserAdmin을 상속받은거임.

    """ Custom User Admin"""

    inlines = (RoomInline,)
    # UserAdmin.fieldsets 한 이유는 이게 없으면 Custom Profile 부분만 나오기 때문이다.
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                    "login_method",
                )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
        "login_method",
    )

    # list.display , list.filter 함수를 사용하면
