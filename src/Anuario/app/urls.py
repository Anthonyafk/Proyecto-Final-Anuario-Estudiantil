from django.urls import path
from . import views

urlpatterns = [
    path("", views.registro, name="registro"),
    path("home/", views.home, name="home"),
    path("551123012/", views.index, name="index")
]
