from django.shortcuts import render
from .models import Usuario, Grupo, Comentario, Publicacion, Nominacion  # .... etc.

def index(request):
    contextosinpretexto = {
    'usuarios': Usuario.objects.all(),
    'grupos': Grupo.objects.all(),
    'comentarios': Comentario.objects.all(),
    'publicaciones': Publicacion.objects.all(),
    'nominaciones': Nominacion.objects.all()
    }
    return render(request, "index.html", contextosinpretexto)

