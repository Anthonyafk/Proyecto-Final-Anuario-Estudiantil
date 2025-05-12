from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario, Grupo, Comentario, Publicacion, Nominacion, Perfil, Tener, Pertenecer, Postular # .... etc.
from .forms import UsuarioRegistroForm, UsuarioBusquedaNominacion
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

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
