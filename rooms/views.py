from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from . import models

# Create your views here.


class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 10  # 저절로 한페이지에 10개씩 보여준다.
    ordering = "created"
    context_object_name = "rooms"  # Room 모델에서 object를 rooms라고 표현


class RoomDetail(DetailView):

    """RoomDetail Definition"""

    model = (
        models.Room
    )  # html은 room_detail.html (room은 모델명이고, detail은 import detailview)


def search(request):
    city = request.GET.get("city", "Anywhere")  # city에 뭐가 없을 때 Anywhere을 가져온다.
    city = str.capitalize(city)  # database 첫번째 알파벳은 대문자이기 때문에.
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    room_types = models.RoomType.objects.all()

    form = {
        "city": city,
        "s_room_type": room_type,
        "s_country": country,
    }

    choices = {
        "countries": countries,
        "room_types": room_types,
    }

    return render(request, "rooms/search.html", {**form, **choices})
