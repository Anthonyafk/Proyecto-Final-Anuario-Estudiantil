from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario, Grupo, Comentario, Publicacion, Nominacion, Perfil, Tener, Pertenecer, Postular # .... etc.
from .forms import UsuarioRegistroForm, UsuarioBusquedaNominacion
from django.db import IntegrityError

from django.shortcuts import HttpResponse #prueba
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

#Esta funcion esta disponible sii existe al menos un grupo en la vista home
def nominaciones(request):
    #deberiamos obtenemos el id del grupo al que le dio clic el usuario en el paso anterior
    codigo_grupo = 1
    nominaciones = Nominacion.objects.filter(activa=True,existe__codigo__codigo=codigo_grupo)
    return render(request, "nomination/all-nominations.html", {'nominaciones': nominaciones})

#Función para mostrar la descripción de la nominación, junto con los estudiantes a votar y el botón para postularse
def verNominacion(request, idNominacion):
    #No se debe habilitar la opción de postularse si el usuario ya esta inscrito 
    numCuenta = 1
    form = UsuarioBusquedaNominacion()
    desabilitar = ""
    dato = ""
    nominacion = Nominacion.objects.get(pk = idNominacion)
    inscritos = Postular.objects.filter(idNominacion = idNominacion)
    usuarioInscrito = inscritos.filter(numCuenta = numCuenta)
    
    if(usuarioInscrito.exists()):
        desabilitar = "disabled"
        inscritos = inscritos.exclude(numCuenta = numCuenta)
    
    if(request.method == "POST"):
        nombreCompleto = request.POST["nombre"]
        if(nombreCompleto):
            nombres = nombreCompleto.split()
            for nombre in nombres:
                inscritos = inscritos.filter(numCuenta__nombre__icontains = nombre) | inscritos.filter(numCuenta__primer_apellido__icontains = nombre) | inscritos.filter(numCuenta__segundo_apellido__icontains = nombre)
        
        if(not nombreCompleto):
            dato = 'Busqueda vacia.'
        
    
    return render(request, "nomination/nomination.html", {'nominacion':nominacion, 'inscritos':inscritos, 'desabilitar':desabilitar, 'form':form, 'dato':dato})
