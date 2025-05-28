import secrets
import string
import sweetify
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Usuario, Grupo, Comentario, Publicacion, Nominacion, Perfil, Tener, Pertenecer, Postular, Votar, MarcoFoto, Ganar, Comentario, Gestionar, Poseer, Marco, Existe, Count
from .forms import UsuarioRegistroForm, UsuarioBusquedaNominacion, PerfilForm, DejarComentario, GroupJoinForm, GrupoForm, PublicacionForm, BusquedaGenericaForm, EditarPublicacionForm, EditarDuracionNominacionesForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from datetime import date
from datetime import datetime
from django.utils import timezone

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
    try:
        if usuario.is_superuser:
            grupos_u = Gestionar.objects.filter(numCuenta=usuario)
        else:
            grupos_u = Pertenecer.objects.filter(numCuenta=usuario)
    except:
        grupos_u = []
    for g in grupos_u:
        grupos.append(g.codigo)
    return render(request, "home.html", { 'grupos' : grupos })

#Esta funcion esta disponible sii existe al menos un grupo en la vista home
def nominaciones(request,grupo_id):
    grupo = Grupo.objects.get(codigo=grupo_id)
    ahora = timezone.now() #Se agregó para tener la fecha y zona horario actual en las nominaciones

    # Solo se muestran nominaciones activas
    nominaciones = Nominacion.objects.filter(
        activa=True,
        existe__codigo__codigo=grupo_id,
        existe__fecha_inicio__lte=ahora,
        existe__fecha_fin__gte=ahora
    )

    # Verificar si el usuario es admin para mostrar el enlace de edición
    es_admin = request.user.is_superuser

    return render(request, "nomination/all-nominations.html", {
        'nominaciones': nominaciones,
        'grupo': grupo,
        'es_admin': es_admin
    })

#Función para mostrar la descripción de la nominación, junto con los estudiantes a votar y el botón para postularse
def verNominacion(request, idNominacion):
    #No se debe habilitar la opción de postularse si el usuario ya esta inscrito 
    numCuenta = request.user
    formBusqueda = UsuarioBusquedaNominacion()

    desabilitarPostulacion = ""
    desabilitarVotacion = ""
    dato = ""
    #inscrito = False

    marcos = MarcoFoto.objects.all()

    nominacion = Nominacion.objects.get(pk = idNominacion)
    inscritos = Postular.objects.filter(idNominacion = idNominacion)

    usuarioInscrito = inscritos.filter(numCuenta = numCuenta)

    # Verificar si la nominación está activa y dentro del período de activación
    ahora = timezone.now()
    existe = Existe.objects.filter(idNominacion=nominacion).first()

    if not existe or ahora < existe.fecha_inicio or ahora > existe.fecha_fin:
        messages.error(request, "Esta nominación no está disponible en este momento.")
        return redirect('nominaciones', grupo_id=existe.codigo.codigo)

    if(usuarioInscrito.exists()):
        desabilitarPostulacion = "style= display:none;"

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
    return render(request, "nomination/nomination.html", {
        'nominacion':nominacion,
        'inscritos':inscritos,
        'desabilitarPostulacion':desabilitarPostulacion,
        'formBusqueda':formBusqueda,
        'dato':dato,
        'desabilitarVotacion':desabilitarVotacion,
        'marcos':marcos,
    })

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
        marco = MarcoFoto.objects.filter(idPerfil=perfil)
        comentarios = Comentario.objects.filter(idPerfil=perfil)
    datos = {
        'perfil': perfil,
        'usuario': usuario_obj,
        'marco': marco.first(),
        'comentarios': comentarios
    }
    return render(request, 'perfil/perfil.html', datos)

# Función para poder editar perfil
def editar_perfil(request, usuario_id):
    usuario = Usuario.objects.get(numCuenta=usuario_id)
    # Obtener el perfil del usuario actual
    perfil = usuario.tener.idPerfil
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
            sweetify.success(
                request,
                'Usuario editado',
                text='Los datos se actualizaron correctamente.',
                persistent='OK'
            )
            return redirect('perfil', usuario_id=usuario_id)  # Redirige al perfil después de editar
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'perfil/editar_perfil.html', {
        'form': form,
        'marcos': marcos,
        'usuario' : usuario
    })

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
    return render(request, 'admin/admin_alumnos.html', {
        'grupo': grupo,
        'form': form,
        'integrantes': integrantes_qs,
        'marcos':marcos
    })

def comentarios(request, grupo_id, publicacion_id):
    grupo = Grupo.objects.get(codigo=grupo_id)
    publicacion = Publicacion.objects.get(idPublicacion=publicacion_id)
    poseer = Poseer.objects.filter(idPublicacion=publicacion)
    comentarios = Comentario.objects.filter(
        idComentario__in=poseer.values_list('idComentario', flat=True)
    ).order_by('-fecha_creacion', '-hora_creacion')

    return render(request, 'grupos/comentarios.html', {
        'grupo' : grupo,
        'publicacion': publicacion,
        'comentarios': comentarios,
        'grupo_id': grupo_id,
    })

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

def editar_comentario(request, grupo_id, comentario_id):
    grupo = Grupo.objects.get(codigo=grupo_id)
    comentario = Comentario.objects.get(idComentario=comentario_id)

    form = DejarComentario()
    if request.method=="POST":
        form = DejarComentario(request.POST)
        if form.is_valid():
            contenido = form.cleaned_data['comentario']
            fecha_creacion = date.today()
            now = datetime.now()

            if contenido:
                comentario.contenido = contenido
                comentario.fecha_creacion = fecha_creacion
                comentario.hora_creacion = now
            comentario.save()
            sweetify.success(
                request,
                'Comentario editado',
                text='Los datos se actualizaron correctamente.',
                persistent='OK'
            )
            return redirect('detalle_grupo', grupo_id=grupo_id)

    return render(request, "grupos/editar_comentario.html",{
        'grupo' : grupo,
        'comentario' : comentario,
        'form' : form
    })

def eliminar_comentario(request, grupo_id, comentario_id):
    comentario = get_object_or_404(Comentario, idComentario=comentario_id)
    comentario.delete()

    sweetify.success(request, 'Comentario eliminado', text='El comentario ha sido eliminado', persistent='OK')
    return redirect('ad_comentarios', grupo_id=grupo_id)

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
                codigo=grupo,
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

def editar_publicacion(request, grupo_id, publicacion_id):
    grupo = Grupo.objects.get(codigo=grupo_id)
    publicacion = Publicacion.objects.get(idPublicacion=publicacion_id)

    form = EditarPublicacionForm()
    if request.method=="POST":
        form = EditarPublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            descripcion = form.cleaned_data['descripcion']
            fecha_creacion = date.today()
            now = datetime.now()
            imagen = form.cleaned_data['imagen']

            if descripcion:
                publicacion.descripcion = descripcion
                publicacion.fecha_creacion = fecha_creacion
                publicacion.hora_creacion = now
            if imagen:
                publicacion.image = imagen
            publicacion.save()
            sweetify.success(
                request,
                'Publicacion editada',
                text='Los datos se actualizaron correctamente.',
                persistent='OK'
            )
            return redirect('detalle_grupo', grupo_id=grupo_id)

    return render(request, "grupos/editar_publicacion.html",{
        'grupo' : grupo,
        'publicacion' : publicacion,
        'form' : form
    })

def eliminar_publicacion(request, grupo_id, publicacion_id):
    publicacion = get_object_or_404(Publicacion, idPublicacion=publicacion_id)
    publicacion.delete()

    sweetify.success(request, 'Publicacion eliminada', text='La publicacion ha sido eliminada', persistent='OK')
    return redirect('ad_publicaciones', grupo_id=grupo_id)

def expulsar_alumno(request, grupo_id, numCuenta):
    pertenencia = get_object_or_404(Pertenecer, codigo__codigo=grupo_id, numCuenta__numCuenta=numCuenta)
    pertenencia.delete()

    sweetify.success(request, 'Alumno expulsado', text='El alumno ha sido eliminado del grupo.', persistent='OK')
    return redirect('ad_alumnos', grupo_id=grupo_id)

@staff_member_required
def ad_alumnos(request,grupo_id):
    grupo, form, integrantes_qs, marcos = revisar_integrantes(request, grupo_id)
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

@staff_member_required
def ad_publicaciones(request, grupo_id):
    grupo = Grupo.objects.get(codigo=grupo_id)
    publicaciones = get_publicaciones(request, grupo_id) # Publicaciones del grupo
    form = BusquedaGenericaForm(request.GET or None)
    if form.is_valid():
        usuario = form.cleaned_data.get('nombre_usuario')
        numCuenta = form.cleaned_data.get('numCuenta')
        fecha = form.cleaned_data.get('fecha')

        if usuario:
            publicaciones = publicaciones.filter(numCuenta__nombre_usuario__icontains=usuario)
        if numCuenta:
            publicaciones = publicaciones.filter(numCuenta__numCuenta__icontains=numCuenta)
        if fecha:
            publicaciones = publicaciones.filter(fecha_creacion=fecha)

    return render(request, 'admin/admin_publicaciones.html', {
        'publicaciones': publicaciones,
        'grupo' : grupo,
        'is_generic' : True,
        'form' : form
    })

@staff_member_required
def ad_comentarios(request, grupo_id):
    # Obtener publicaciones del grupo
    publicaciones = get_publicaciones(request,grupo_id)
    if publicaciones:
        publicaciones_ids = publicaciones.values_list('idPublicacion', flat=True)
        # Obtener comentarios en publicaciones
        comentarios = Comentario.objects.filter(
            idComentario__in=Poseer.objects.filter(
                idPublicacion__in=publicaciones_ids
            ).values_list('idComentario', flat=True)
        ).order_by('-fecha_creacion', '-hora_creacion')
    else:
        comentarios = []

    grupo = Grupo.objects.get(codigo=grupo_id)
    # Busqueda en comentarios
    form = BusquedaGenericaForm(request.GET or None)
    if form.is_valid():
        usuario = form.cleaned_data.get('nombre_usuario')
        numCuenta = form.cleaned_data.get('numCuenta')
        fecha = form.cleaned_data.get('fecha')

        if usuario:
            comentarios = comentarios.filter(numCuenta__nombre_usuario__icontains=usuario)
        if numCuenta:
            comentarios = comentarios.filter(numCuenta__numCuenta__icontains=numCuenta)
        if fecha:
            comentarios = comentarios.filter(fecha_creacion=fecha)
    return render(request, 'admin/admin_comentarios.html', {
        'grupo' : grupo,
        'comentarios' : comentarios,
        'is_generic' : True,
        'form' : form
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
                codigo_acceso=codigo_generado
            )
            Gestionar.objects.create(numCuenta=request.user, codigo=grupo)
            messages.success(request, f"Grupo creado correctamente. El código de acceso es: {codigo_generado}")
            return redirect('detalle_grupo', grupo_id=grupo.codigo)  # Solo aquí redirige

    # Si no es POST o el form no es válido, solo renderiza el formulario
    return render(request, 'grupos/gestionar_grupo.html', {'form': form, 'grupo': grupo})

# Función para generar un código de grupo aleatorio
def generar_codigo_grupo(length=7):
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

# Función para buscar un grupo por su código
def buscar_grupo_por_codigo(codigo):
    return Grupo.objects.filter(codigo_acceso=codigo).first()

#Función para cambiar la duración de las nominaciones
def editar_duracion_nominaciones(request, grupo_id):
    grupo = get_object_or_404(Grupo, codigo=grupo_id)
    nominaciones_grupo = Existe.objects.filter(codigo=grupo)

    if not nominaciones_grupo.exists():
        messages.warning(request, "No hay nominaciones para este grupo.")
        return redirect('nominaciones', grupo_id=grupo.codigo)

    # damos la misma duración a todas las categorías de un mismo grupo
    nominacion_referencia = nominaciones_grupo.first()

    if request.method == 'POST':
        form = EditarDuracionNominacionesForm(request.POST, instance=nominacion_referencia)
        if form.is_valid():
            # Actualiza todas las nominaciones del grupo con la misma duración
            nominaciones_grupo.update(
                fecha_inicio=form.cleaned_data['fecha_inicio'],
                fecha_fin=form.cleaned_data['fecha_fin']
            )
            messages.success(request, "La duración de las nominaciones ha sido actualizada.")
            return redirect('nominaciones', grupo_id=grupo.codigo)
    else:
        form = EditarDuracionNominacionesForm(instance=nominacion_referencia)

    return render(request, 'admin/editar_duracion.html', {
        'form': form,
        'grupo': grupo,
    })

#Función para ver los resultados de las nominaciones
def resultados_votacion(request, idNominacion=None, codigo_grupo=None):
    ahora = timezone.now()

    # Muestra todos los ganadores por categoría (vista general)
    if codigo_grupo:
        nominaciones = Nominacion.objects.all()
        categorias_con_ganadores = []

        for nominacion in nominaciones:
            existe = nominacion.existe_set.first()

            # Solo procesa nominaciones que ya terminaron
            if existe and existe.fecha_fin < ahora:
                resultados = Votar.objects.filter(idNominacion=nominacion).values(
                    'alumnoVotado__numCuenta',
                    'alumnoVotado__nombre',
                    'alumnoVotado__primer_apellido'
                ).annotate(
                    total_votos=Count('alumnoVotado')
                ).order_by('-total_votos')

                if resultados:
                    max_votos = resultados[0]['total_votos']
                    ganadores = [r for r in resultados if r['total_votos'] == max_votos]

                    categorias_con_ganadores.append({
                        'categoria': nominacion.categoria,
                        'ganadores': ganadores,
                        'es_empate': len(ganadores) > 1,
                        'existe': existe,
                        'max_votos': max_votos
                    })

        return render(request, 'nomination/ganadores.html', {
            'vista_ganadores': True,
            'categorias_con_ganadores': categorias_con_ganadores,
            'mostrar_ganadores': len(categorias_con_ganadores) > 0
        })

    # Vista individual de una nominación específica
    nominacion = get_object_or_404(Nominacion, pk=idNominacion)
    existe = nominacion.existe_set.first()

    # Verifica estado de la votación
    votacion_activa = existe and existe.fecha_inicio <= ahora <= existe.fecha_fin
    votacion_cerrada = existe and existe.fecha_fin < ahora

    # Obtiene resultados
    resultados = Votar.objects.filter(idNominacion=nominacion).values(
        'alumnoVotado__numCuenta',
        'alumnoVotado__nombre',
        'alumnoVotado__primer_apellido'
    ).annotate(
        total_votos=Count('alumnoVotado')
    ).order_by('-total_votos')

    # Determina ganador(es)
    ganadores = []
    max_votos = 0

    if resultados:
        max_votos = resultados[0]['total_votos']
        ganadores = [r for r in resultados if r['total_votos'] == max_votos]

    return render(request, 'nomination/resultados_individuales.html', {
        'nominacion': nominacion,
        'resultados': resultados,
        'votacion_activa': votacion_activa,
        'votacion_cerrada': votacion_cerrada,
        'mostrar_resultados': nominacion.mostrar_resultados,
        'ganadores': ganadores,
        'es_empate': len(ganadores) > 1,
        'max_votos': max_votos,
        'no_hay_nominaciones_activas': not votacion_activa and not votacion_cerrada,
        'vista_ganadores': False  # Importante para el template
    })
