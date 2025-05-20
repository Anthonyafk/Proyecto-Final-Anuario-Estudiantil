from django.contrib import admin
from .models import Grupo, Pertenecer

# Funciones para el admin de Django

# Para Crear un grupo
@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre',)

# Pertenencia de un usuario a un grupo
@admin.register(Pertenecer)
class PertenecerAdmin(admin.ModelAdmin):
    list_display = ('numCuenta', 'codigo',)