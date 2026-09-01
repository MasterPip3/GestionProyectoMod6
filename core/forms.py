from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Proyecto, Tarea, Participacion
from django.utils import timezone


class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email',)
        

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ("nombre", "descripcion", "fecha_inicio", "fecha_termino", "prioridad",)
        widgets = {
            "fecha_inicio": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"},),
            "fecha_termino": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"},),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["descripcion"].label = "Descripción"
        self.fields["fecha_inicio"].label = "Fecha de inicio"
        self.fields["fecha_termino"].label = "Fecha de término"
        
        
        if not self.is_bound:
            self.fields["fecha_inicio"].initial = timezone.localdate()
            

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = (
            "nombre",
            "descripcion",
            "fecha_inicio",
            "fecha_termino",
            "importancia",
            "estado",
            "responsable",
        )
        widgets = {
            "fecha_inicio": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"},),
            "fecha_termino": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"},),
        }
        
    def __init__(self, *args, **kwargs):
        proyecto = kwargs.pop("proyecto", None)
        usuario = kwargs.pop("usuario", None)
        super().__init__(*args, **kwargs)
        
        self.fields["descripcion"].label = "Descripción"
        self.fields["fecha_inicio"].label = "Fecha de inicio"
        self.fields["fecha_termino"].label = "Fecha de término"
        
        modo_creacion = self.instance.pk is None
        
        if proyecto is not None:
            participaciones = proyecto.participaciones.filter(activo=True,).select_related("usuario")
            
            if usuario is not None:
                participacion_usuario = participaciones.filter(usuario=usuario,).first()
                
                if (participacion_usuario is not None and participacion_usuario.rol == "colaborador"):
                    
                    self.fields.pop("responsable")
                    
                else:
                    self.fields["responsable"].queryset = participaciones
                    
                    if (modo_creacion and participacion_usuario is not None):
                        self.fields["responsable"].initial = participacion_usuario
            
            else:
                self.fields["responsable"].queryset = participaciones
                
            self.fields["fecha_inicio"].initial = proyecto.fecha_inicio
            
            
class ParticipacionForm(forms.ModelForm):
    class Meta:
        model = Participacion
        fields = ("usuario", "rol")
        
    def __init__(self, *args, **kwargs):
        proyecto = kwargs.pop("proyecto", None)
        super().__init__(*args, **kwargs)
        
        self.fields["rol"].choices = [
            ("colaborador", "Colaborador"),
            ("ayudante", "Ayudante"),                
        ]
        
        self.fields["rol"].initial = "colaborador"
        
        if proyecto is not None:
            usuarios_participantes = Participacion.objects.filter(proyecto=proyecto, activo=True,).values_list("usuario_id", flat=True)
            
            self.fields["usuario"].queryset = User.objects.exclude(id__in=usuarios_participantes,)
            
            
class CambiarRolForm(forms.Form):
    rol = forms.ChoiceField(
        choices=[
            ("ayudante", "Ayudante"),
            ("colaborador", "Colaborador"),
        ]
    )
