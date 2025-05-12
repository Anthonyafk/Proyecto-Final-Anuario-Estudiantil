from django import forms

class UsuarioRegistroForm(forms.Form):
    numCuenta = forms.IntegerField(label="No. Cuenta", required=True)
    nombre_usuario = forms.CharField(label="Nombre de usuario", max_length=150,required=True)
    correoE = forms.EmailField(label="Email", required=True)
    contraseña = forms.CharField(label="Contraseña", required=True, widget=forms.PasswordInput)

class UsuarioBusquedaNominacion(forms.Form):
    #Input para texto tiene label, texto de ayuda, si es o no requerido y al final el parametro para insertar bootstrap
    nombre = forms.CharField(label="Nombre:", help_text="Buscar Estudiante...", required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
