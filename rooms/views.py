from django.http import Http404
from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import (
    login_required,
)  # @delete_photo에서 @login_required를 쓰려면 import
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from users import mixins as user_mixins
from . import models, forms

# Create your views here.


class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 12  # 저절로 한페이지에 10개씩 보여준다.
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"  # Room 모델에서 object를 rooms라고 표현

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):  # 룸 호스트랑 요청하는 사람이랑 같은지
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):
    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):  # 룸 호스트랑 요청하는 사람이랑 같은지
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required  # 만약 로그인이 안되어 있으면, setting에서 LOGIN_URL 로 이동한다 (이거 설정해둬야함.)
def delete_photo(request, room_pk, photo_pk):  # url.py에 등록되어있는거.
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Can't delete that photo")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo Deleted")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:  # room이 없음
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"  # pk를 찾아야하니까.
    success_message = "Photo Updated"
    fields = ("caption",)

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):

    model = models.Photo
    template_name = "rooms/photo_create.html"
    fields = ("caption", "file")
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")  # form으로 pk를 갖다줘야해서 pk를 설정 (room의 pk).
        form.save(pk)  # pk를 줌 form에다가
        messages.success(self.request, "Photo Uploaded")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))


class CreateRoomView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreateRoomForm
    template_name = "rooms/room_create.html"

    def form_valid(self, form):
        room = form.save()
        room.host = self.request.user
        room.save()
        form.save_m2m()  # many to many를 저장하는 것임. 이거는 DB에 object를 저장한 후에 할 수 있음.
        messages.success(self.request, "Room Uploaded")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
