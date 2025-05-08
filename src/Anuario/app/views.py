from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario, Grupo, Comentario, Publicacion, Nominacion, Perfil, Tener # .... etc.
from .forms import UsuarioRegistroForm
from django.db import IntegrityError

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

def registro(request):
    form = UsuarioRegistroForm()
    usuario = None
    if request.method == "POST":
        form = UsuarioRegistroForm(request.POST)
        if form.is_valid():
            num_cuenta = form.cleaned_data['numCuenta']

            try:
                usuario = Usuario.objects.get(numCuenta=num_cuenta)
            except Usuario.DoesNotExist:
                messages.error(request, f"El usuario con número de cuenta {num_cuenta} no existe.")
                return render(request, 'registration/registration.html', {'form' : form})

            if Tener.objects.filter(numCuenta=num_cuenta).exists():
                messages.error(request, "Este usuario ya tiene un perfil registrado.")
                return render(request, 'registration/registration.html', {'form' : form})

            usuario.correoE = form.cleaned_data['correoE']
            usuario.nombre_usuario = form.cleaned_data['nombre_usuario']
            usuario.contraseña = form.cleaned_data['contraseña']
            usuario.save()

            perfil = Perfil.objects.create(
                foto_perfil = "",
                foto_portada = "",
                biografia = ""
            )

            Tener.objects.create(numCuenta=num_cuenta, idPerfil=perfil.idPerfil)
            messages.success(request, "Registro exitoso")
            return redirect('home')
    #else:
    #    form = UsuarioRegistroForm()
    return render(request, 'registration/registration.html', { 'form' : form })


def home(request):
    #usuario = Usuario.objects.get(pk=id)
    #print(usuario)
    return render(request, "home.html")
