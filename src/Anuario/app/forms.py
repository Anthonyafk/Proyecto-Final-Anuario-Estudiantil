from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Perfil, Grupo, Tener, Existe

# Formulario para el registro de un usuario.
# Cada campo es necesario para la base de datos
class UsuarioRegistroForm(UserCreationForm):
    numCuenta = forms.IntegerField(
        label="Número de cuenta",
        required=True,
        widget=forms.NumberInput(attrs={
            'class' : 'form-control ps-5 rounded-pill bg-light',
            'placeholder' : 'No. Cuenta'
        })
    )
    nombre = forms.CharField(
        label="Nombre",
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control ps-5 rounded-pill bg-light',
            'placeholder': 'Ingrese su nombre'
        })
    )
    primer_apellido= forms.CharField(
        label="Primer apellido",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control ps-5 rounded-pill bg-light',
            'placeholder': 'Ingrese su primer apellido'
        })
    )
    segundo_apellido= forms.CharField(
        label="Segundo apellido",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control ps-5 rounded-pill bg-light',
            'placeholder': 'Ingrese su segundo apellido'
        })
    )
    nombre_usuario = forms.CharField(
        label="Nombre de usuario",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control ps-5 rounded-pill bg-light',
            'placeholder': 'Nombre de Usuario'
        })
    )
    correoE = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control ps-5 rounded-pill bg-light',
            'placeholder': 'Email'
        })
    )
    password1 = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control ps-5 rounded-pill bg-light',
            'placeholder': 'Ingrese una contraseña'
        })
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control ps-5 rounded-pill bg-light',
            'placeholder': 'introduzca la misma contraseña anterior'
        })
    )
    class Meta:
        model = Usuario
        fields = ['numCuenta', 'nombre', 'primer_apellido', 'segundo_apellido', 'correoE', 'nombre_usuario', 'password1', 'password2']

class UsuarioBusquedaNominacion(forms.Form):
    #Input para texto tiene label, texto de ayuda, si es o no requerido y al final el parametro para insertar bootstrap
    nombre = forms.CharField(
        label="Nombre:", 
        help_text="Buscar Estudiante...", 
        required=False, widget=forms.TextInput(attrs={
            'class':'form-control', 
            'placeholder': 'Buscar Estudiante...'
        }))

# Formulario para editar perfil
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto_perfil', 'foto_portada', 'biografia']
        widgets = {
            'biografia': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
        labels = {
            'foto_perfil': 'Foto de perfil',
            'foto_portada': 'Foto de portada',
            'biografia': 'Biografía'
        }

# Formulario para unirse a un grupo
class GroupJoinForm(forms.Form):
    codigo = forms.CharField(
        label="Código de grupo",
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa el código de acceso'
        })
    )

# Formulario para grupo
class GrupoForm(forms.Form):
    nombre = forms.CharField(
        max_length=50,
        label="Nombre del grupo",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre del grupo'
        })
    )
    descripcion = forms.CharField(
        required=False,
        label="Descripción",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Descripción del grupo'
        })
    )
    foto_portada = forms.ImageField(
        required=False,
        label="Imagen de portada",
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )

class DejarComentario(forms.Form):
    #Input para texto tiene label, texto de ayuda, si es o no requerido y al final el parametro para insertar bootstrap
    comentario = forms.CharField(
        label="Comentario:",
        help_text="Escribe tu comentario...",
        required=False, widget=forms.TextInput(attrs={
            'class':'form-control rounded-pill bg-light',
            'placeholder': 'Dejar un comentario'
        }))

class PublicacionForm(forms.Form):
    descripcion = forms.CharField(
        label="descripcion",
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Escribe algo...'
        })
    )
    imagen = forms.ImageField(
        required=False,
        label="Imagen de publicacion",
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control rounded-pill bg-light'
        })
    )

# Formulario para editar tiempo de nominaciones
class EditarDuracionNominacionesForm(forms.ModelForm):
    class Meta:
        model = Existe
        fields = ['fecha_inicio', 'fecha_fin']
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_fin': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
