from django.urls import path, include
from django.views.generic.base import TemplateView  # new
from . import views

urlpatterns = [
    path("verNominacion/<str:idNominacion>", views.verNominacion, name="verNominacion"),
    #path("551123012/", views.index, name="index"),
    path("perfil/<int:usuario_id>", views.verPerfil, name="perfil"),
    path("perfil/comentario/<int:idPerfil>", views.comentarioPerfil, name="add_comentario"),
    path("perfil/editar/<int:usuario_id>", views.editar_perfil, name="editar_perfil"),
    # path("grupo/info/", views.detalle_grupo, name="grupo_info"),
    path('grupos/<int:grupo_id>/',views.detalle_grupo,name='detalle_grupo'), #ruta anterior pero dinamica
    path("grupos/<int:grupo_id>/nominaciones/", views.nominaciones, name="nominaciones"),
    path('grupos/<int:grupo_id>/integrantes/', views.integrantes, name='integrantes'),
    path('grupos/unirse/', views.unirse_grupo, name='unirseGrupo'),
    path('grupos/nuevo/', views.crear_o_editar_grupo, name='crear_grupo'),
    path('grupos/<int:grupo_id>/editar/', views.crear_o_editar_grupo, name='editar_grupo'),
    path('grupos/<int:grupo_id>/publicar/', views.publicar, name='publicar'),
    path('grupos/<int:grupo_id>/comentar/<int:publicacion_id>', views.comentar, name='comentar'),
    path('grupos/<int:grupo_id>/comentarios/<int:publicacion_id>', views.comentarios, name='comentarios'),
    path('grupos/<int:grupo_id>/admin/alumnos/', views.ad_alumnos, name='ad_alumnos'),
    path('grupos/<int:grupo_id>/admin/publicaciones/', views.ad_publicaciones, name='ad_publicaciones'),
    path('grupos/<int:grupo_id>/admin/comentarios/', views.ad_comentarios, name='ad_comentarios'),
    path('grupos/<int:grupo_id>/admin/expulsar/<int:numCuenta>/', views.expulsar_alumno, name='expulsar_alumno'),
    path("accounts/signup/", views.signup, name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),  # new
    #path("", TemplateView.as_view(template_name="home.html"), name="home")  # new
    path("",views.home, name="home")
]

'''
accounts/login/ [name='login']
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']
'''
