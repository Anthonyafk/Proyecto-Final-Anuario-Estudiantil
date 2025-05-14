from django.contrib import admin
from .models import Grupo, Pertenecer

# Funciones para el admin de Django

# Para Crear un grupo
@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre',)
