from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class Proyecto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    prioridad = models.PositiveSmallIntegerField(
        choices=[
            (1, "1 estrella"),
            (2, "2 estrellas"),
            (3, "3 estrellas"),
            (4, "4 estrellas"),
            (5, "5 estrellas"),
        ],
        default=3,
    )
    eliminado = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nombre
    
    def clean(self):
        super().clean()
    
        if self.fecha_inicio and self.fecha_termino:
            if self.fecha_inicio > self.fecha_termino:
                raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de término.")
    
    
class Tarea(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("en_progreso", "En progreso"),
        ("completada", "Completada"),
    ]
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="tareas",)
    responsable = models.ForeignKey("Participacion", on_delete=models.PROTECT, related_name="tareas_responsables",)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    importancia = models.PositiveSmallIntegerField(
        choices=[(i, f"{i}") for i in range(1,11)],
        default=1,
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="pendiente",
    )
    eliminado = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nombre
    
    def clean(self):
        super().clean()

        if self.fecha_inicio and self.fecha_termino:
            if self.fecha_inicio > self.fecha_termino:
                raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de término.")
            
        if self.proyecto_id and self.proyecto:
            if self.fecha_inicio and self.fecha_inicio < self.proyecto.fecha_inicio:
                raise ValidationError("La fecha de inicio de la tarea no puede ser anterior a la fecha de inicio del proyecto.")
            
            if self.fecha_termino and self.fecha_termino > self.proyecto.fecha_termino:
                raise ValidationError("La fecha de término de la tarea no puede ser posterior a la fecha de término del proyecto.")
        

class Participacion(models.Model):
    ROLES = [
        ("encargado_principal", "Encargado principal"),
        ("ayudante", "Ayudante"),
        ("colaborador", "Colaborador"),
    ]
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name="participaciones",)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT, related_name="participaciones")
    rol = models.CharField(max_length=25, choices=ROLES,)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Participación"
        verbose_name_plural = "Participaciones"
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "proyecto"],
                condition=models.Q(activo=True),
                name="una_participacion_activa_por_usuario_proyecto",
            ),
        ]
        
    def __str__(self):
        return f"{self.usuario.username} - {self.proyecto.nombre}"