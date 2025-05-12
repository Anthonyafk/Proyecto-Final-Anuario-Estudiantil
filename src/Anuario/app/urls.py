from django.urls import path, include
from django.views.generic.base import TemplateView  # new
from . import views

urlpatterns = [
    #path("551123012/", views.index, name="index"),
    path("accounts/signup/", views.signup, name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),  # new
    path("", TemplateView.as_view(template_name="home.html"), name="home")  # new
]
