from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Perfil, Tener

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
    nombre = forms.CharField(label="Nombre:", help_text="Buscar Estudiante...", required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
