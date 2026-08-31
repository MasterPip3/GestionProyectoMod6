from django.contrib import admin
from .models import Proyecto, Tarea, Participacion

# Register your models here.
admin.site.register(Proyecto)
admin.site.register(Tarea)
admin.site.register(Participacion)