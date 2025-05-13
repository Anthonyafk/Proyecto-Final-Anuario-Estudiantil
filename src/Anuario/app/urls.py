from django.urls import path, include
from django.views.generic.base import TemplateView  # new
from . import views

urlpatterns = [
    path("nominaciones/", views.nominaciones, name="nominaciones"),
    path("verNominacion/<str:idNominacion>", views.verNominacion, name="verNominacion"),
    #path("551123012/", views.index, name="index"),
    path("perfil/", views.verPerfil, name="perfil"),
    path("perfil/editar/", views.editar_perfil, name="editar_perfil"),
    path("grupo/info/", views.detalle_grupo, name="grupo_info"),
    path("accounts/signup/", views.signup, name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),  # new
    path("", TemplateView.as_view(template_name="home.html"), name="home")  # new
]
