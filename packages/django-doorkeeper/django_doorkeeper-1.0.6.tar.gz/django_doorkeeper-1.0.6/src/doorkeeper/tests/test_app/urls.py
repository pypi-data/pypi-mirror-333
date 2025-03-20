from django.urls import path

from doorkeeper.decorators import doorkeeper_exempt
from doorkeeper.tests.test_app import views

urlpatterns = [
    path("", views.public_view, name="home"),
    path("protected/", views.protected_view, name="protected"),
    path("public/", views.public_view, name="public"),
    path("exempt/", doorkeeper_exempt(views.exempt_view), name="exempt"),
]
