from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario, Grupo, Comentario, Publicacion, Nominacion, Perfil, Tener, Pertenecer, Postular, Votar, Gestionar# .... etc.
from .forms import UsuarioRegistroForm, UsuarioBusquedaNominacion, PerfilForm
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
    usuario = request.user
    print(usuario)
    try:
        if usuario.is_superuser:
            grupos_u = Gestionar.objects.filter(numCuenta=usuario)
        else:
            grupos_u = Pertenecer.objects.filter(numCuenta=usuario)
    except:
        grupos_u = []
    for g in grupos_u:
        print(f"g.codigo: {g.codigo}")
        grupos.append(g.codigo)
    print(grupos)
    return render(request, "home.html", { 'grupos' : grupos })

#Esta funcion esta disponible sii existe al menos un grupo en la vista home
def nominaciones(request,grupo_id):
    grupo = Grupo.objects.get(codigo=grupo_id)
    nominaciones = Nominacion.objects.filter(activa=True,existe__codigo__codigo=grupo_id)
    return render(request, "nomination/all-nominations.html", {'nominaciones': nominaciones,'grupo':grupo})

#Función para mostrar la descripción de la nominación, junto con los estudiantes a votar y el botón para postularse
def verNominacion(request, idNominacion):
    #No se debe habilitar la opción de postularse si el usuario ya esta inscrito 
    numCuenta = request.user
    formBusqueda = UsuarioBusquedaNominacion()
    
    desabilitarPostulacion = ""
    desabilitarVotacion = ""
    dato = ""
    
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
        
    
    return render(request, "nomination/nomination.html", {'nominacion':nominacion, 'inscritos':inscritos, 'desabilitarPostulacion':desabilitarPostulacion, 'formBusqueda':formBusqueda, 'dato':dato, 'desabilitarVotacion':desabilitarVotacion})

#Funcion para acceder al perfil del usuario
def verPerfil(request, usuario_id):
    
    #Obtiene el Usuario  según el parámetro usuario_id
    usuario_obj = Usuario.objects.get(numCuenta=usuario_id)
    try:
        relacion_tener = Tener.objects.get(numCuenta=usuario_obj)
        perfil = relacion_tener.idPerfil
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
        'usuario': usuario_obj
    }
    return render(request, 'perfil/perfil.html', datos)

# Función para poder editar perfil
def editar_perfil(request):
    # Obtener el perfil del usuario actual
    perfil = request.user.tener.idPerfil
    
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil', usuario_id=request.user.numCuenta)  # Redirige al perfil después de editar
    else:
        form = PerfilForm(instance=perfil)
    
    return render(request, 'perfil/editar_perfil.html', {'form': form})

#Funnción para ver la información de los grupos
# Al tener la otra pantalla (donde salen los grupos) podemos acceder al grupo mediante
# su id, como por ahora es la segunda vista, solo se muestra la base de la vista sin 
# datos.
# podemos cambiar por def detalle_grupo(request, grupo_id):
def detalle_grupo(request, grupo_id):
    grupo = Grupo.objects.get(codigo=grupo_id)
    publicaciones = Publicacion.objects.filter(
        numCuenta__in=Pertenecer.objects.filter(
            codigo__codigo=grupo_id
        ).values_list('numCuenta', flat=True)
    ).order_by('-fecha_creacion', '-hora_creacion')
    return render(request, 'grupos/detalle_grupo.html', {
        'grupo': grupo,
        'publicaciones' : publicaciones
    })



# Función para ver los integrantes de un grupo
def integrantes(request, grupo_id):
    pertenencias = Pertenecer.objects.filter(codigo__codigo=grupo_id)
    grupo = Grupo.objects.get(codigo=grupo_id)
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

    return render(request, 'integrantes/integrantes.html', {'grupo': grupo, 'form': form, 'integrantes': integrantes_qs,})

def ad_alumnos(request,grupo_id):
    grupo = Grupo.objects.get(codigo=grupo_id)
    pertenencias = Pertenecer.objects.filter(codigo__codigo=grupo_id)
    alumnos = Usuario.objects.filter(
        numCuenta__in=pertenencias.values_list('numCuenta', flat=True)
    )

    # Filtro
    form = UsuarioBusquedaNominacion(request.GET or None)
    if form.is_valid() and form.cleaned_data.get('nombre'):
        termino = form.cleaned_data['nombre']
        alumnos = (
            alumnos.filter(nombre__icontains=termino) |
            alumnos.filter(primer_apellido__icontains=termino) |
            alumnos.filter(segundo_apellido__icontains=termino)
        )
    return render(request, 'admin/admin_alumnos.html', {
        'alumnos': alumnos,
        'form' : form,
        'grupo' : grupo
    })

def get_publicaciones(grupo_id):
    publicaciones = Publicacion.objects.filter(
        numCuenta__in=Pertenecer.objects.filter(
            codigo__codigo=grupo_id
        ).values_list('numCuenta', flat=True)
    ).order_by('-fecha_creacion', '-hora_creacion')  # Opcional: más recientes primero

def ad_publicaciones(request, grupo_id):
    # Subconsulta: obtener publicaciones de alumnos que pertenecen al grupo
    grupo = Grupo.objects.get(codigo=grupo_id)
    publicaciones = get_publicaciones(grupo_id)

    return render(request, 'admin/admin_publicaciones.html', {
        'publicaciones': publicaciones,
        'grupo' : grupo
    })

def ad_comentarios(request, grupo_id):
    # Obtener publicaciones del grupo
    publicaciones = get_publicaciones(grupo_id)
    if publicaciones:
        publicaciones_ids = publicaciones.values_list('idPublicacion', flat=True)
        # Obtener comentarios relacionados usando la tabla intermedia Poseer
        comentarios = Comentario.objects.filter(
            idcomentario__in=Poseer.objects.filter(
                idPublicacion__in=publicaciones_ids
            ).values_list('idComentario', flat=True)
        ).order_by('-fecha_creacion', '-hora_creacion')  # Si tu modelo Comentario tiene estos campos
    else:
        comentarios = []

    grupo = Grupo.objects.get(codigo=grupo_id)
    return render(request, 'admin/admin_comentarios.html', {
        'grupo' : grupo,
        'comentarios' : comentarios
    })
