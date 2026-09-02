from django.contrib import admin
from .models import Proyecto, Tarea, Participacion

# Register your models here.
@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "fecha_inicio",
        "fecha_termino",
        "prioridad",
        "eliminado",
    )
    
    list_filter = (
        "prioridad",
        "eliminado",
    )
    
    search_fields = (
        "nombre",
        "descripcion",
    )


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "descripcion",  
        "responsable",
        "fecha_inicio",
        "fecha_termino",
        "eliminado",
        "estado",        
    )
    
    list_filter = (
        "estado",
        "importancia",
        "eliminado",
    )
    
    search_fields = (
        "nombre",
        "descripcion",
    )


@admin.register(Participacion)
class ParticipacionAdmin(admin.ModelAdmin):
    list_display = (
        "usuario",
        "proyecto",
        "rol",
        "activo",
    )
    
    list_filter = (
        "rol",
        "activo",
    )
    
    search_fields = (
        "usuario__username",
        "proyecto__nombre",
    )
