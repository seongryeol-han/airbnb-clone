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

    rooms = models.Room.objects.filter(**filter_args)

    return render(request, "rooms/search.html", {**form, **choices, "rooms": rooms})
