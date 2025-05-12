from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Usuario, Grupo, Comentario, Publicacion, Nominacion, Perfil, Tener # .... etc.
from .forms import UsuarioRegistroForm
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

def index(request):
    contextosinpretexto = {
    'usuarios': Usuario.objects.all(),
    'grupos': Grupo.objects.all(),
    'comentarios': Comentario.objects.all(),
    'publicaciones': Publicacion.objects.all(),
    'nominaciones': Nominacion.objects.all(),
    'perfiles': Perfil.objects.all()
    }
    return render(request, "index.html", contextosinpretexto)

def signup(request):
    form = UsuarioRegistroForm()
    if request.method == 'POST':
        form = UsuarioRegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            usuario.save()
            user = authenticate(username=form.cleaned_data['numCuenta'], password=form.cleaned_data['password1'])
            perfil = Perfil.objects.create(
                foto_perfil = "",
                foto_portada = "",
                biografia = ""
            )
            try:
                Tener.objects.create(numCuenta=usuario, idPerfil=perfil)
            except:
                Perfil.objects.filter(idPerfil=perfil.idPerfil).delete()
            login(request, user)
            messages.success(request, "Registro exitoso")
            return redirect('home')
    else:
        form = UsuarioRegistroForm()
    return render(request, 'registration/registration.html', { 'form' : form })

@login_required
def home(request):
    #numCuenta= request.GET.get('numCuenta')
    #usuario = Usuario.objects.get(numCuenta=numCuenta)
    #grupos =
    return render(request, "home.html")
