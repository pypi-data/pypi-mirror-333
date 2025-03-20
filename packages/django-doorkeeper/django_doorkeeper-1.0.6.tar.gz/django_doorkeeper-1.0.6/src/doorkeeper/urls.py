from django.urls import path

from doorkeeper.views import DoorkeeperEntranceView, DoorkeeperExitView

app_name = "doorkeeper"

entrance_view = DoorkeeperEntranceView.as_view()
entrance_view.is_doorkeeper_entrance = True

urlpatterns = [
    path("entrance/", entrance_view, name="entrance"),
    path("exit/", DoorkeeperExitView.as_view(), name="exit"),
]
