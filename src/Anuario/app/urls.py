from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("551123012/", views.index, name="index")
]
