import secrets
import string
import sweetify
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Usuario, Grupo, Comentario, Publicacion, Nominacion, Perfil, Tener, Pertenecer, Postular, Votar, MarcoFoto, Ganar, Comentario, Gestionar, Poseer, Marco # .... etc.
from .forms import UsuarioRegistroForm, UsuarioBusquedaNominacion, PerfilForm, DejarComentario, GroupJoinForm, GrupoForm, PublicacionForm
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
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
                marco = Marco.objects.get(idMarco = marcoElegido)
                marcoUnoAUno = MarcoFoto.objects.filter(idPerfil=perfil)
                if marcoUnoAUno.exists():
                    marcoUnoAUno.delete()
                marcofoto = MarcoFoto(idPerfil=perfil, marco_foto=marco) 
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

def alerta_grupo(request):
    sweetify.warning(
        request,
        'Acceso denegado',
        text='No perteneces a este grupo.',
        persistent='OK'
    )
    return redirect('home')
#Funnción para ver la información de los grupos
# Al tener la otra pantalla (donde salen los grupos) podemos acceder al grupo mediante
# su id, como por ahora es la segunda vista, solo se muestra la base de la vista sin 
# datos.
# podemos cambiar por def detalle_grupo(request, grupo_id):
@login_required
def detalle_grupo(request, grupo_id):
    grupo = Grupo.objects.get(codigo=grupo_id)
    pertenece = Pertenecer.objects.filter(
        codigo=grupo,
        numCuenta = request.user
    )
    gestiona = Gestionar.objects.filter(
        codigo=grupo,
        numCuenta=request.user
    )
    publicaciones = get_publicaciones(request, grupo_id)

    if request.user.is_superuser:
        if not gestiona:
            return alerta_grupo(request)
    else:
        if not pertenece:
            return alerta_grupo(request)

    forms = {
        pub.idPublicacion : DejarComentario() for pub in publicaciones
    }

    return render(request, 'grupos/detalle_grupo.html', {
        'grupo': grupo,
        'publicaciones' : publicaciones,
        'forms' : forms
    })

def revisar_integrantes(request, grupo_id):
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
    return (grupo, form, integrantes_qs, marcos)

# Función para ver los integrantes de un grupo
def integrantes(request, grupo_id):
    grupo, form, integrantes_qs, marcos = revisar_integrantes(request, grupo_id)
    print(integrantes_qs)
    return render(request, 'admin/admin_alumnos.html', {
        'grupo': grupo,
        'form': form,
        'integrantes': integrantes_qs,
        'marcos':marcos
    })

def comentarios(request, grupo_id, publicacion_id):
    return redirect('detalle_grupo', grupo_id=grupo_id)

def comentar(request, grupo_id, publicacion_id):
    publicacion = Publicacion.objects.get(idPublicacion=publicacion_id)
    perfil_tener = Tener.objects.get(numCuenta=request.user)
    if request.method=="POST":
        form = DejarComentario(request.POST)
        if form.is_valid():
            contenido = form.cleaned_data['comentario']
            fecha_creacion = date.today()
            now = datetime.now()

            if contenido:
                comentario = Comentario.objects.create(
                    idPerfil=perfil_tener.idPerfil,
                    numCuenta=request.user,
                    contenido=contenido,
                    fecha_creacion=fecha_creacion,
                    hora_creacion=now
                )
                Poseer.objects.create(
                    idComentario=comentario,
                    idPublicacion=publicacion
                )

    return redirect('detalle_grupo', grupo_id=grupo_id)

def publicar(request, grupo_id):
    grupo = Grupo.objects.get(codigo=grupo_id)

    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            fecha_creacion = date.today()
            now = datetime.now()

            publicacion = Publicacion.objects.create(
                numCuenta=request.user,
                fecha_creacion=fecha_creacion,
                hora_creacion=now.time(),
                descripcion=data['descripcion'],
                imagen=data.get('imagen'),
                video_url=None
            )

            sweetify.success(
                request,
                '¡Publicación realizada!',
                text='Tu publicación se ha guardado exitosamente.',
                persistent='Aceptar'
            )

            return redirect('detalle_grupo', grupo_id=grupo.codigo)
    else:
        form = PublicacionForm()

    return render(request, 'grupos/publicar.html', {
        'grupo': grupo,
        'form': form
    })

def expulsar_alumno(request, grupo_id, numCuenta):
    pertenencia = get_object_or_404(Pertenecer, codigo__codigo=grupo_id, numCuenta__numCuenta=numCuenta)
    pertenencia.delete()

    sweetify.success(request, 'Alumno expulsado', text='El alumno ha sido eliminado del grupo.', persistent='OK')
    return redirect('ad_alumnos', grupo_id=grupo_id)

@staff_member_required
def ad_alumnos(request,grupo_id):
    grupo, form, integrantes_qs, marcos = revisar_integrantes(request, grupo_id)
    print(integrantes_qs)
    return render(request, 'admin/admin_alumnos.html', {
        'grupo': grupo,
        'form': form,
        'integrantes': integrantes_qs,
        'marcos':marcos
    })

def get_publicaciones(request, grupo_id):
    publicaciones = Publicacion.objects.filter(
        codigo__codigo=grupo_id
    ).order_by('-fecha_creacion', '-hora_creacion')
    return publicaciones

def ad_publicaciones(request, grupo_id):
    # Subconsulta: obtener publicaciones de alumnos que pertenecen al grupo
    grupo = Grupo.objects.get(codigo=grupo_id)
    publicaciones = get_publicaciones(request, grupo_id)

    return render(request, 'admin/admin_publicaciones.html', {
        'publicaciones': publicaciones,
        'grupo' : grupo
    })

def ad_comentarios(request, grupo_id):
    # Obtener publicaciones del grupo
    publicaciones = get_publicaciones(request,grupo_id)
    if publicaciones:
        publicaciones_ids = publicaciones.values_list('idPublicacion', flat=True)
        # Obtener comentarios relacionados usando la tabla intermedia Poseer
        comentarios = Comentario.objects.filter(
            idComentario__in=Poseer.objects.filter(
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

def unirse_grupo(request):
    grupo = None
    redirigir = False   # para saber si redirigir tras isncripción o no
    if request.method == 'POST':
        form = GroupJoinForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['codigo']
            grupo = buscar_grupo_por_codigo(codigo)
            if grupo:
                if Pertenecer.objects.filter(numCuenta=request.user, codigo=grupo).exists():
                    messages.warning(request, f"Ya estás inscrito en «{grupo.nombre}».")
                else:
                    Pertenecer.objects.create(numCuenta=request.user, codigo=grupo)
                    messages.success(request, f"Te has unido al grupo «{grupo.nombre}». Serás redirigido a tus grupos en unos segundos.")
                    redirigir = True
            else:
                messages.error(request, "El código de grupo no es válido.")
    else:
        form = GroupJoinForm()
        codigo = request.GET.get('codigo')
        if codigo:
            grupo = buscar_grupo_por_codigo(codigo)

    return render(request, 'grupos/unirseGrupo.html', { 'form': form, 'grupo': grupo, 'redirigir': redirigir })

# Función para crear o editar un grupo
@staff_member_required
def crear_o_editar_grupo(request, grupo_id=None):
    if grupo_id:
        # editar
        grupo = Grupo.objects.get(codigo=grupo_id)
        initial = {
            'nombre': grupo.nombre,
            'descripcion': grupo.descripcion,
        }
        form = GrupoForm(request.POST or None, request.FILES or None, initial=initial)
    else:
        # crear
        grupo = None
        form = GrupoForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        if grupo:
            # actualización
            grupo.nombre = data['nombre']
            grupo.descripcion = data['descripcion']
            if data['foto_portada']:
                grupo.foto_portada = data['foto_portada']
            grupo.save()
            messages.success(request, "Grupo actualizado correctamente.")
            return redirect('detalle_grupo', grupo_id=grupo.codigo)
        else:
            # creación
            codigo_generado = generar_codigo_grupo()
            grupo = Grupo.objects.create(
                nombre=data['nombre'],
                descripcion=data['descripcion'],
                foto_portada=data['foto_portada'] or None,
                codigo_acceso=codigo_generado  # <--- Aquí se guarda el código de acceso
            )
            Gestionar.objects.create(numCuenta=request.user, codigo=grupo)
            messages.success(request, f"Grupo creado correctamente. El código de acceso es: {codigo_generado}")

        return redirect('detalle_grupo', grupo_id=grupo.codigo)

    return render(request, 'grupos/gestionar_grupo.html', {'form': form, 'grupo': grupo,})

# Función para generar un código de grupo aleatorio
def generar_codigo_grupo(length=7):
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

# Función para buscar un grupo por su código
def buscar_grupo_por_codigo(codigo):
    return Grupo.objects.filter(codigo_acceso=codigo).first()
