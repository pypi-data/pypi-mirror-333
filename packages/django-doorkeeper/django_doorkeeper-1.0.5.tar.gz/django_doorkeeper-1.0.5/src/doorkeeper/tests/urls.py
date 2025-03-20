from django.urls import include, path

urlpatterns = [
    path("doorkeeper/", include("doorkeeper.urls")),
    path("", include("doorkeeper.tests.test_app.urls")),
]
