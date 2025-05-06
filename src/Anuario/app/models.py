from django.db import models
from django.core.validators import RegexValidator
import pgtrigger

class Usuario(models.Model):
    numCuenta = models.IntegerField(
        primary_key=True,
        validators=[RegexValidator(r'^\d{1,9}$', 'Debe tener entre 1 y 9 dígitos')]
    )
    nombre = models.CharField(max_length=50)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50)
    correoE = models.EmailField(
        unique=True,
        max_length=100,
        validators=[RegexValidator(
            r'^[A-Za-z0-9._%+-]+@ciencias\.unam\.mx$',
            'Debe ser @ciencias.unam.mx'
        )]
    )
    nombre_usuario = models.CharField(unique=True, max_length=50)
    contraseña = models.CharField(max_length=128)
    esAdmin = models.BooleanField(default=False)

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


class Perfil(models.Model):
    idPerfil = models.AutoField(primary_key=True)
    foto_perfil = models.TextField(blank=True)
    foto_portada = models.TextField(blank=True)
    biografia = models.TextField(blank=True)


class Grupo(models.Model):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    foto_portada = models.TextField(blank=True)


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
    fecha_creacion = models.DateField()
    hora_creacion = models.TimeField()
    descripcion = models.TextField(blank=True)
    imagen = models.TextField(blank=True)
    video_url = models.URLField(blank=True, null=True) # Atributo/campo de prueba para almacenar la URL de un video


class Nominacion(models.Model):
    idNominacion = models.AutoField(primary_key=True)
    categoria = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)

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


class Ganar(models.Model):
    idNominacion = models.ForeignKey(Nominacion, on_delete=models.CASCADE)
    numCuenta = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    premio = models.TextField(blank=True)
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


class Pertenecer(models.Model):
    numCuenta = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    codigo = models.ForeignKey(Grupo, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('numCuenta', 'codigo'),)


class Tener(models.Model):
    numCuenta = models.OneToOneField(
        Usuario, primary_key=True, on_delete=models.CASCADE
    )
    idPerfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)


class Postular(models.Model):
    numCuenta = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    idNominacion = models.ForeignKey(Nominacion, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('numCuenta', 'idNominacion'),)


class MarcoFoto(models.Model):
    idPerfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    marco_foto = models.TextField()

    class Meta:
        unique_together = (('idPerfil', 'marco_foto'),)
