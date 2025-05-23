from django.contrib import admin
from .models import Grupo, Pertenecer, Gestionar, Nominacion

# Funciones para el admin de Django

# Para Crear un grupo
@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre',)

# Para guardar el grupo y crear la relación con el usuario en la tabla Gestionar dentro de la vista de admin de Django por defecto
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Solo crea la relación si es un grupo nuevo
        if not Gestionar.objects.filter(numCuenta=request.user, codigo=obj).exists():
            Gestionar.objects.create(numCuenta=request.user, codigo=obj)

# Tabla para gestionar la relación entre un usuario y un grupo
@admin.register(Gestionar)
class GestionarAdmin(admin.ModelAdmin):
    list_display = ('numCuenta', 'codigo',)

# Pertenencia de un usuario a un grupo
@admin.register(Pertenecer)
class PertenecerAdmin(admin.ModelAdmin):
    list_display = ('numCuenta', 'codigo',)

#Para cambiar la duración de laa nominaciones
@admin.register(Nominacion)
class NominacionAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'activa', 'mostrar_resultados')
    list_editable = ('mostrar_resultados',)