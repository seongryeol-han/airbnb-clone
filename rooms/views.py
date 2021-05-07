from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models, forms

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


class SearchView(View):

    """SearchView Definition"""

    def get(self, request):

        country = request.GET.get("country")

        if country:

            form = forms.SearchForm(request.GET)  # 이걸 쓰면 form이 기억을 하고 있다.

            if form.is_valid():  # form이 에러가 없다면.

                city = form.cleaned_data.get("city")  # cleand_data는 데이터를 정리해준다.
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by(
                    "-created"
                )  # pagination을 쓰려면 order이 되어 있어야한다.

                paginator = Paginator(qs, 10, orphans=5)  # qs를 받아서 10개씩 page 1개,

                page = request.GET.get(
                    "page", 1
                )  # url에서 읽어오는거고, 에러가 나오면 page= 1로 돌아간다는 뜻.

                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )

        else:
            form = forms.SearchForm()  # 첫번째 화면을 가져오려고, 아무것도 체크 되어있지 않는 것.

            return render(request, "rooms/search.html", {"form": form})