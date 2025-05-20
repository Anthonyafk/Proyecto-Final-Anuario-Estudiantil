from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario, Grupo, Comentario, Publicacion, Nominacion, Perfil, Tener, Pertenecer, Postular, Votar, MarcoFoto, Ganar, Comentario # .... etc.
from .forms import UsuarioRegistroForm, UsuarioBusquedaNominacion, PerfilForm, DejarComentario, GroupJoinForm
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from datetime import date
from datetime import datetime

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

# Registra un usuario en la aplicación
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
    grupos = []
    try:
        grupos_p = Pertenecer.objects.filter(numCuenta=request.user)
    except:
        grupos_p = []
    print(grupos_p)
    for g in grupos_p:
        print(f"g.codigo: {g.codigo}")
        grupos.append(g.codigo)
    print(grupos)
    return render(request, "home.html", { 'grupos' : grupos })

#Esta funcion esta disponible sii existe al menos un grupo en la vista home
def nominaciones(request,grupo_id):
    nominaciones = Nominacion.objects.filter(activa=True,existe__codigo__codigo=grupo_id)
    return render(request, "nomination/all-nominations.html", {'nominaciones': nominaciones,'grupo':grupo_id})

#Función para mostrar la descripción de la nominación, junto con los estudiantes a votar y el botón para postularse
def verNominacion(request, idNominacion):
    #No se debe habilitar la opción de postularse si el usuario ya esta inscrito 
    numCuenta = request.user
    formBusqueda = UsuarioBusquedaNominacion()
    
    desabilitarPostulacion = ""
    desabilitarVotacion = ""
    dato = ""
    
    marcos = MarcoFoto.objects.all()
    
    nominacion = Nominacion.objects.get(pk = idNominacion)
    inscritos = Postular.objects.filter(idNominacion = idNominacion)
    
    usuarioInscrito = inscritos.filter(numCuenta = numCuenta)
    
    if(usuarioInscrito.exists()):
        desabilitarPostulacion = "style= display:none;"
        inscritos = inscritos.exclude(numCuenta = numCuenta)
    
    votoAntes = Votar.objects.filter(idNominacion = idNominacion)
    votoAntes = votoAntes.filter(numCuenta = numCuenta.numCuenta)
    
    if(votoAntes.exists()):
        desabilitarVotacion = "style=display:none;"
    
    if(request.method == "POST"):
        if 'Postular' in request.POST:
            postular = Postular(numCuenta = numCuenta, idNominacion = nominacion)
            postular.save()
            return redirect('verNominacion', idNominacion = idNominacion)
        elif 'Votar' in request.POST:
            aVotar = request.POST.get('Votar')
            alumnoVotado = Usuario.objects.get(numCuenta = aVotar)
            votacion = Votar(numCuenta = numCuenta, idNominacion = nominacion, alumnoVotado = alumnoVotado) 
            votacion.save()
            return redirect('verNominacion', idNominacion = idNominacion)
        else:
            nombreCompleto = request.POST["nombre"]
            if(nombreCompleto):
                nombres = nombreCompleto.split()
                for nombre in nombres:
                    inscritos = inscritos.filter(numCuenta__nombre__icontains = nombre) | inscritos.filter(numCuenta__primer_apellido__icontains = nombre) | inscritos.filter(numCuenta__segundo_apellido__icontains = nombre)
            if(not nombreCompleto):
                dato = 'Busqueda vacia.'
        
    
    return render(request, "nomination/nomination.html", {'nominacion':nominacion, 'inscritos':inscritos, 'desabilitarPostulacion':desabilitarPostulacion, 'formBusqueda':formBusqueda, 'dato':dato, 'desabilitarVotacion':desabilitarVotacion, 'marcos':marcos})

#Funcion para acceder al perfil del usuario
def verPerfil(request, usuario_id):
    
    #Obtiene el Usuario  según el parámetro usuario_id
    usuario_obj = Usuario.objects.get(numCuenta=usuario_id)
    try:
        relacion_tener = Tener.objects.get(numCuenta=usuario_obj)
        perfil = relacion_tener.idPerfil
        marco = MarcoFoto.objects.filter(idPerfil=perfil)
        comentarios = Comentario.objects.filter(idPerfil=perfil)
    except Tener.DoesNotExist:
        # Si no existe el perfil, creamos uno vacío
        perfil = Perfil.objects.create(
            foto_perfil="",
            foto_portada="",
            biografia=""
        )
        Tener.objects.create(numCuenta=usuario_obj, idPerfil=perfil)
    datos = {
        'perfil': perfil,
        'usuario': usuario_obj,
        'marco': marco.first(),
        'comentarios': comentarios
    }
    return render(request, 'perfil/perfil.html', datos)

# Función para poder editar perfil
def editar_perfil(request):
    # Obtener el perfil del usuario actual
    perfil = request.user.tener.idPerfil
    
    # Obtiene todos los marcos que ha ganado el usuario
    marcos = Ganar.objects.filter(numCuenta = request.user)
    
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            marcoElegido = request.POST.get('marco_foto')
            if marcoElegido:
                marcoUnoAUno = MarcoFoto.objects.filter(idPerfil=perfil)
                if marcoUnoAUno.exists():
                    marcoUnoAUno.delete()
                marcofoto = MarcoFoto(idPerfil=perfil, marco_foto=marcoElegido) 
                marcofoto.save()
            form.save()
            return redirect('perfil', usuario_id=request.user.numCuenta)  # Redirige al perfil después de editar
    else:
        form = PerfilForm(instance=perfil)
    
    return render(request, 'perfil/editar_perfil.html', {'form': form, 'marcos': marcos})

#Función para añadir comentarios
def comentarioPerfil(request, idPerfil):
    formComentar = DejarComentario()
    usuario = Tener.objects.get(idPerfil=idPerfil)
    perfil = Perfil.objects.get(idPerfil=idPerfil)
    nota = ""
    if request.method == 'POST':
        comentario = request.POST["comentario"]
        if(comentario):
            fecha_creacion = date.today()
            now = datetime.now()
            subir = Comentario(idPerfil=perfil, numCuenta=request.user, contenido=comentario, fecha_creacion=fecha_creacion, hora_creacion=now.time())
            subir.save()
            return redirect('perfil', usuario_id = usuario.numCuenta.numCuenta)
        else:
            nota="No se puede publicar un comentario vacio."
    
    return render(request, 'common/dejarComentario.html', {'formComentar': formComentar, 'usuario':usuario, 'nota':nota})


#Funnción para ver la información de los grupos
# Al tener la otra pantalla (donde salen los grupos) podemos acceder al grupo mediante
# su id, como por ahora es la segunda vista, solo se muestra la base de la vista sin 
# datos.
# podemos cambiar por def detalle_grupo(request, grupo_id):
def detalle_grupo(request, grupo_id):
    grupo = Grupo.objects.get(codigo=grupo_id)
    return render(request, 'grupos/detalle_grupo.html', {'grupo': grupo} )  # Justo probe lo que comentabas :), funciona

# Función para ver los integrantes de un grupo
def integrantes(request, grupo_id):
    pertenencias = Pertenecer.objects.filter(codigo__codigo=grupo_id)
    grupo = Grupo.objects.get(codigo=grupo_id)
    
    marcos = MarcoFoto.objects.all()
    
    integrantes_qs = Usuario.objects.filter(
        numCuenta__in=pertenencias.values_list('numCuenta', flat=True)
    )

    # Filtro
    form = UsuarioBusquedaNominacion(request.GET or None)
    if form.is_valid() and form.cleaned_data.get('nombre'):
        termino = form.cleaned_data['nombre']
        integrantes_qs = (
            integrantes_qs.filter(nombre__icontains=termino) |
            integrantes_qs.filter(primer_apellido__icontains=termino) |
            integrantes_qs.filter(segundo_apellido__icontains=termino)
        )

    return render(request, 'integrantes/integrantes.html', {'grupo': grupo, 'form': form, 'integrantes': integrantes_qs, 'marcos':marcos})

def unirse_grupo(request):
    grupo = None
    redirigir = False  # para saber si redirigir tras isncripción o no
    if request.method == 'POST':
        form = GroupJoinForm(request.POST)
        if form.is_valid():
                grupo = Grupo.objects.get(codigo=form.cleaned_data['codigo'])
                if Pertenecer.objects.filter(numCuenta=request.user, codigo=grupo).exists():
                    messages.warning(request, f"Ya estás inscrito en «{grupo.nombre}».")
                else:
                    Pertenecer.objects.create(numCuenta=request.user, codigo=grupo)
                    messages.success(request, f"Te has unido al grupo «{grupo.nombre}». Serás redirigido a tus grupos en unos segundos.")
                    redirigir = True
    else:
        form = GroupJoinForm()
        codigo = request.GET.get('codigo')
        if codigo:
            try:
                grupo = Grupo.objects.get(codigo=codigo)
            except Grupo.DoesNotExist:
                grupo = None

    return render(request, 'grupos/unirseGrupo.html', { 'form': form, 'grupo': grupo, 'redirigir': redirigir })
