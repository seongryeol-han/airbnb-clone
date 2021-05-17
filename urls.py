from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>", views.RoomDetail.as_view(), name="detail"),
    path("search/", views.SearchView.as_view(), name="search"),
]  # <int:pk> 이게 주소에서 room/ 다음에 오는 부분. url.py -> views.py 로 pk를 넘겨주는거네. 그리고 views.room_detail를 불러온다.
# room_detail은 argument를 기다린다. 그래서 room_list.html에서 "room:detail" 다음에 argument가 필요하다.

# 기본적으로. pk를 argument를 받아서 views.RoomDetail에다가 넘긴다.
