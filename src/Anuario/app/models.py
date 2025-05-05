from django.db import models
from django.core.validators import RegexValidator

class Usuario(models.Model):
    numCuenta = models.IntegerField(
        primary_key=True,
        validators=[
            RegexValidator(
                regex=r'^\d{1,9}$',
                message='El número de cuenta debe tener entre 1 y 9 dígitos'
            )
        ]
    )
    nombre = models.CharField(max_length=50)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50)
    correoE = models.EmailField(unique=True, max_length=100)
    nombre_usuario = models.CharField(unique=True, max_length=50)
    contraseña = models.CharField(max_length=128)
    esAdmin = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(numCuenta__gte=1) & models.Q(numCuenta__lte=999999999),
                name='ck_usuario_numCuenta_range'
            ),
            models.CheckConstraint(
                check=models.Q(correoE__regex=r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
                name='ck_usuario_correoE_format'
            )
        ]

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

class Nominacion(models.Model):
    idNominacion = models.AutoField(primary_key=True)
    categoria = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)

class Ganar(models.Model):
    idNominacion = models.ForeignKey(Nominacion, on_delete=models.CASCADE)
    numCuenta = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    premio = models.TextField(blank=True)

    class Meta:
        unique_together = (('idNominacion', 'numCuenta'),)

class Votar(models.Model):
    numCuenta = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='votos_emitidos')
    idNominacion = models.ForeignKey(Nominacion, on_delete=models.CASCADE)
    alumnoVotado = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='votos_recibidos')

    class Meta:
        unique_together = (('numCuenta', 'idNominacion', 'alumnoVotado'),)

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
    numCuenta = models.OneToOneField(Usuario, primary_key=True, on_delete=models.CASCADE)
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
