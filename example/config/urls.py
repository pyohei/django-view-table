from django.urls import path

from library.views import index

urlpatterns = [
    path("", index, name="index"),
]
