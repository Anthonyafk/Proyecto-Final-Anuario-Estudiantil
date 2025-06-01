from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import pgtrigger
from django.db.models import Count

# Necesario para manerjar la creación de usuarios con un modelo propio
class UsuarioManager(BaseUserManager):
    def _create_user(self, numCuenta, nombre, nombre_usuario, correoE, password, **extra_fields):
        if not numCuenta:
            raise ValueError('El número de cuenta es obligatorio.')
        if not correoE:
            raise ValueError('El correo es obligatorio')
        if not nombre_usuario:
            raise ValueError('El nombre de usuario es obligatorio')

        email = self.normalize_email(correoE)
        user = self.model(
            numCuenta=numCuenta,
            nombre=nombre,
            nombre_usuario=nombre_usuario,
            correoE = email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, numCuenta=None, nombre=None, nombre_usuario=None, correoE=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        #extra_fields.setdefault('esAdmin', False)
        return self._create_user(numCuenta, nombre, nombre_usuario, correoE, password, **extra_fields)

    def create_superuser(self, numCuenta=None, nombre=None, nombre_usuario=None, correoE=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        #extra_fields.setdefault('esAdmin', True)
        return self._create_user(numCuenta, nombre, nombre_usuario, correoE, password, **extra_fields)

# Modelo modificario para un usuario de la aplicación
# Utiliza la base de Django que provee la clase AbstractBaseUser
class Usuario(AbstractBaseUser, PermissionsMixin):
    numCuenta = models.IntegerField(
        primary_key=True,
        validators=[RegexValidator(r'^\d{1,9}$', 'Debe tener entre 1 y 9 dígitos')]
    )
    nombre = models.CharField(max_length=255, blank=True, default=' ')
    primer_apellido = models.CharField(max_length=50, blank=True, default='')
    segundo_apellido = models.CharField(max_length=50, blank=True, default='')
    correoE = models.EmailField(
        unique=True,
        max_length=100,
        validators=[RegexValidator(
            r'^[A-Za-z0-9._%+-]+@ciencias\.unam\.mx$',
            'Debe ser @ciencias.unam.mx'
        )]
    )
    nombre_usuario = models.CharField(unique=True, max_length=50)
    #contraseña = models.CharField(max_length=128, blank=True, default='')
    #esAdmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Necesario para el admin

    USERNAME_FIELD = 'numCuenta'
    REQUIRED_FIELDS = ['nombre', 'nombre_usuario', 'correoE']
    EMAIL_FIELD = 'correoE'
    objects = UsuarioManager()

    class Meta:
        constraints = [
            # rango válido para numCuenta
            models.CheckConstraint(
                check=models.Q(numCuenta__gte=1, numCuenta__lte=999999999),
                name='ck_usuario_numCuenta_range'
            ),
            # forzar dominio @ciencias.unam.mx a nivel de BD
            models.CheckConstraint(
                check=models.Q(correoE__regex=r'^[^@]+@ciencias\.unam\.mx$'),
                name='ck_usuario_correoE_domain'
            ),
        ]
        triggers = [
            pgtrigger.Trigger(
                name='anonymize_user_on_delete',
                operation=pgtrigger.Delete,
                when=pgtrigger.Before,
                func='''
                    UPDATE app_usuario
                       SET nombre = NULL,
                           primer_apellido = NULL,
                           segundo_apellido = NULL,
                           correoE = NULL,
                           nombre_usuario = NULL
                     WHERE numCuenta = OLD."numCuenta";
                    RETURN OLD;
                ''',
            )
        ]

    def save(self, *args, **kwargs):
        # ejecutar validadores antes de guardar
        self.full_clean()
        super().save(*args, **kwargs)


# Devuelve el nombre de usuario como cadena y sirve para mostrarlo en la interfaz de administración de Django
    def __str__(self):
        return str(self.numCuenta) + " - " + self.nombre_usuario + "\n"

class Perfil(models.Model):
    idPerfil = models.AutoField(primary_key=True)
    foto_perfil = models.ImageField(upload_to='perfil/', blank=True)
    foto_portada = models.ImageField(upload_to='portada/', blank=True)
    biografia = models.TextField(blank=True)

class Grupo(models.Model):
    codigo = models.AutoField(primary_key=True) # Es mas un id de grupo que un codigo
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    foto_portada = models.ImageField(upload_to='grupos/',blank=True)
    codigo_acceso = models.CharField(max_length=10, unique=True, blank=True, null=True) # Atributo para el código de acceso al grupo

# Devuelve el nombre del grupo como cadena y sirve para mostrarlo en la interfaz de administración de Django
    def __str__(self):
        return self.nombre
class Comentario(models.Model):
    idComentario = models.AutoField(primary_key=True)
    idPerfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    numCuenta = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateField()
    hora_creacion = models.TimeField()


class Publicacion(models.Model):
    idPublicacion = models.AutoField(primary_key=True)
    numCuenta = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    codigo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    fecha_creacion = models.DateField()
    hora_creacion = models.TimeField()
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='publicacion/',blank=True)
    video_url = models.URLField(blank=True, null=True) # Atributo/campo de prueba para almacenar la URL de un video


class Nominacion(models.Model):
    idNominacion = models.AutoField(primary_key=True)
    categoria = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    mostrar_resultados = models.BooleanField(default=True)

    #Muestra el ganador de la categoría cerrada
    def ganador(self):
        votos = Votar.objects.filter(idNominacion=self)
        if votos.exists():
            return votos.values('alumnoVotado').annotate(
                total=Count('alumnoVotado')
            ).order_by('-total').first()
        return None

    class Meta:
        triggers = [
            pgtrigger.Trigger(
                name='deactivate_ganar_on_nom_delete',
                operation=pgtrigger.Delete,
                when=pgtrigger.Before,
                func='''
                    UPDATE app_ganar
                       SET activa = FALSE
                     WHERE idNominacion_id = OLD."idNominacion";
                    RETURN OLD;
                ''',
            )
        ]

class Marco(models.Model):
    idMarco = models.AutoField(primary_key=True)
    marco = models.ImageField(upload_to='marco/', blank=True)
    #si gana mas de una categoría solo se asigna un marco 
    es_multiple = models.BooleanField(default=False)

    def __str__(self):
        return f"Marco {self.idMarco}"

class Ganar(models.Model):
    idNominacion = models.ForeignKey(Nominacion, on_delete=models.CASCADE)
    numCuenta = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    premio = models.ForeignKey(Marco, on_delete=models.CASCADE)
    activa = models.BooleanField(default=True)

    class Meta:
        unique_together = (('idNominacion', 'numCuenta'),)


class Votar(models.Model):
    numCuenta = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='votos_emitidos'
    )
    idNominacion = models.ForeignKey(Nominacion, on_delete=models.CASCADE)
    alumnoVotado = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='votos_recibidos'
    )

    class Meta:
        unique_together = (
            ('numCuenta', 'idNominacion', 'alumnoVotado'),
        )


class Poseer(models.Model):
    idComentario = models.ForeignKey(Comentario, on_delete=models.CASCADE)
    idPublicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('idComentario', 'idPublicacion'),)


class Existe(models.Model):
    idNominacion = models.ForeignKey(Nominacion, on_delete=models.CASCADE)
    codigo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()

    class Meta:
        unique_together = (('idNominacion', 'codigo'),)
        constraints = [
            models.CheckConstraint(
                check=models.Q(fecha_fin__gt=models.F('fecha_inicio')),
                name='check_fecha_fin_posterior'
            )
        ]


class Gestionar(models.Model):
    numCuenta = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    codigo = models.ForeignKey(Grupo, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('numCuenta', 'codigo'),)
        verbose_name = "Gestionar"          # Para mostrar correctamente el nombre de gestionar en la interfaz de administración de Django
        verbose_name_plural = "Gestionar"


class Pertenecer(models.Model):
    numCuenta = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    codigo = models.ForeignKey(Grupo, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('numCuenta', 'codigo'),)
        verbose_name = "Pertenecer"
        verbose_name_plural = "Pertenecer"  # Para mostrar correctamente el nombre en plural en la interfaz de administración de Django

# Para mostrar correctamente las relaciones de pertenencia en la interfaz de administración de Django
    def __str__(self):
        return f"{self.numCuenta} en {self.codigo}"

class Tener(models.Model):
    numCuenta = models.OneToOneField(Usuario, primary_key=True, on_delete=models.CASCADE)
    idPerfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)


class Postular(models.Model):
    numCuenta = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    idNominacion = models.ForeignKey(Nominacion, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('numCuenta', 'idNominacion'),)

class MarcoFoto(models.Model):
    idPerfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    marco_foto = models.ForeignKey(Marco, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('idPerfil', 'marco_foto'),)
        
