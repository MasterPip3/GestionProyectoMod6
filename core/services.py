from django.core.exceptions import ValidationError
from core.models import Participacion, Tarea, Proyecto
from django.db import transaction
from django.utils import timezone



def crear_tarea(usuario, proyecto, datos):
    if proyecto.eliminado:
        raise ValidationError("No se pueden crear tareas en un proyecto eliminado.")
    
    participacion_creador = Participacion.objects.filter(
        usuario = usuario,
        proyecto = proyecto,
        activo=True,
    ).first()
    
    if participacion_creador is None:
        raise ValidationError("El usuario no participa activamente en este proyecto.")
    
    participaciones_activas = Participacion.objects.filter(proyecto=proyecto, activo=True,)
    
    if participacion_creador.rol == "colaborador":
        responsable_enviado = datos.get("responsable")
        
        if (responsable_enviado is not None and responsable_enviado != participacion_creador):
            raise ValidationError("Un colaborador no puede asignar una tarea a otro participante.")
        
        responsable = participacion_creador
        
    else:
        responsable = datos.get("responsable")
        
        if responsable is not None:
            if responsable not in participaciones_activas:
                raise ValidationError("El responsable seleccionado no participa activamente en este proyecto.")
            
        else:
            cantidad_participaciones = participaciones_activas.count()
            
            if cantidad_participaciones == 1:
                responsable = participaciones_activas.first()
            
            else:
                raise ValidationError("Debe seleccionar un responsable para la tarea.")
        
    tarea = Tarea(
        proyecto = proyecto,
        responsable = responsable,
        nombre = datos["nombre"],
        descripcion = datos["descripcion"],
        fecha_inicio = datos["fecha_inicio"],
        fecha_termino = datos["fecha_termino"],
        importancia = datos.get("importancia", 1),
        estado = datos.get("estado", "pendiente"),
    )
    
    tarea.full_clean()
    tarea.save()
    
    return tarea


def editar_tarea(usuario, tarea, datos):
    proyecto = tarea.proyecto
    
    if proyecto.eliminado:
        raise ValidationError("No se pueden editar tareas de un proyecto eliminado.")
    
    if tarea.eliminado:
        raise ValidationError("No se puede editar una tarea eliminada.")
    
    participacion_editor = Participacion.objects.filter(
        usuario=usuario,
        proyecto=proyecto,
        activo=True,
    ).first()
    
    if participacion_editor is None:
        raise ValidationError("El usuario no participa activamente en este proyecto.")
    
    participaciones_activas = Participacion.objects.filter(proyecto=proyecto, activo=True,)
    responsable_nuevo = tarea.responsable
    
    if participacion_editor.rol == "colaborador":
        if "responsable" in datos:
            if datos["responsable"] != tarea.responsable:
                raise ValidationError("Un colaborador no puede cambiar el responsable de la tarea.")
            
    else:        
        if "responsable" in datos:
            responsable_nuevo = datos["responsable"]
            
            if responsable_nuevo not in participaciones_activas:
                raise ValidationError("El responsable seleccionado no participa activamente en este proyecto.")
            
            
    campos_editables = ["nombre", "descripcion", "fecha_inicio", "fecha_termino", "importancia", "estado",]
    
    tarea_editada = Tarea.objects.get(pk=tarea.pk)
    tarea_editada.responsable = responsable_nuevo
    
    for campo in campos_editables:
        if campo in datos:
            setattr(tarea_editada, campo, datos[campo])
            
    tarea_editada.full_clean()
    tarea_editada.save()
    
    return tarea_editada


def eliminar_tarea(usuario, tarea):
    proyecto = tarea.proyecto
    
    if proyecto.eliminado:
        raise ValidationError("No se pueden eliminar tareas de un proyecto eliminado.")
    
    if tarea.eliminado:
        raise ValidationError("La tarea ya está eliminada.")
    
    participacion_usuario = Participacion.objects.filter(usuario=usuario, proyecto=proyecto, activo=True,).first()
    
    if participacion_usuario is None:
        raise ValidationError("El usuario no participa activamente en este proyecto.")
    
    if participacion_usuario.rol != "encargado_principal":
        raise ValidationError("Sólo el encargado principal puede eliminar tareas.")
    
    tarea.eliminado = True
    tarea.save(update_fields=["eliminado"])
    
    return tarea


@transaction.atomic
def cambiar_rol_participacion(usuario, participacion, nuevo_rol):
    proyecto = participacion.proyecto
    
    if proyecto.eliminado:
        raise ValidationError("No se pueden modificar roles en un proyecto eliminado.")
    
    if not participacion.activo:
        raise ValidationError("No se puede modificar una participación inactiva.")
    
    participacion_editor = Participacion.objects.filter(usuario=usuario, proyecto=proyecto, activo=True,).first()
    
    if participacion_editor is None:
        raise ValidationError("El usuario no participa activamente en este proyecto.")
    
    if participacion_editor.rol != "encargado_principal":
        raise ValidationError("Sólo el encargado principal puede cambiar roles.")
    
    if participacion_editor == participacion:
        raise ValidationError("El encargado principal no puede cambiar su propio rol. Para más información revise FAQs.")
    
    roles_validos = ["encargado_principal", "ayudante", "colaborador",]
    
    if nuevo_rol not in roles_validos:
        raise ValidationError("El rol seleccionado no es válido.")
    
    if nuevo_rol == "encargado_principal":
        raise ValidationError("No se puede asignar otro encargado principal mediante esta función. Para más información revise FAQs.")
    
    if nuevo_rol == "ayudante":
        ayudante_actual = Participacion.objects.filter(proyecto=proyecto, rol="ayudante", activo=True,).first()
        
        if ayudante_actual is not None:
            ayudante_actual.rol = "colaborador"
            ayudante_actual.save(update_fields=["rol"])
    
    participacion.rol = nuevo_rol
    participacion.save(update_fields=["rol"])
    
    return participacion


@transaction.atomic
def salir_proyecto(usuario, proyecto):
    if proyecto.eliminado:
        raise ValidationError("No se puede salir de un proyecto eliminado.")
    
    participacion = Participacion.objects.filter(usuario=usuario, proyecto=proyecto, activo=True,).first()
    
    if participacion is None:
        raise ValidationError("El usuario no participa activamente en este proyecto.")
    
    tareas_pendientes = Tarea.objects.filter(proyecto=proyecto, responsable=participacion, eliminado=False,).exists()
    
    if tareas_pendientes:
        raise ValidationError("No puede salir del proyecto mientras tenga tareas activas a su cargo. Debe reasignar todas sus tareas antes de salir.")
    
    if participacion.rol == "encargado_principal":
        ayudante = Participacion.objects.filter(proyecto=proyecto, rol="ayudante", activo=True,).first()
        
        if ayudante is None:
            raise ValidationError("El encargado principal no puede salir si no existe un ayudante. Para más información revisar FAQs.")
        
        ayudante.rol = "encargado_principal"
        ayudante.save(update_fields=["rol"])
        
    participacion.activo = False
    participacion.save(update_fields=["activo"])
    
    return participacion


@transaction.atomic
def calcular_progreso_proyecto(proyecto):
    tareas_activas = Tarea.objects.filter(proyecto=proyecto, eliminado=False,)
    
    if not tareas_activas.exists():
        return 0.0
    
    peso_total = sum(tarea.importancia for tarea in tareas_activas)
    
    if peso_total == 0:
        return 0.0
    
    avance_ponderado = 0
    
    for tarea in tareas_activas:
        if tarea.estado == "pendiente":
            avance = 0
        elif tarea.estado == "en_progreso":
            avance = 0.5
        elif tarea.estado == "completada":
            avance = 1
        else:
            raise ValidationError(f"Estado de tarea no válido: {tarea.estado}")
        
        avance_ponderado += tarea.importancia * avance
        
    return (avance_ponderado / peso_total) * 100


@transaction.atomic
def crear_proyecto(usuario, datos):
    fecha_inicio = datos.get("fecha_inicio", timezone.localdate())
    
    proyecto = Proyecto(
        nombre=datos["nombre"],
        descripcion=datos["descripcion"],
        fecha_inicio=fecha_inicio,
        fecha_termino=datos["fecha_termino"],
        prioridad=datos.get("prioridad", 3),
        eliminado=False,
    )
    
    proyecto.full_clean()
    proyecto.save()
    
    Participacion.objects.create(
        usuario=usuario,
        proyecto=proyecto,
        rol="encargado_principal",
        activo=True,
    )
    
    return proyecto


def obtener_proyectos_dashboard(usuario):
    participaciones_activas = Participacion.objects.filter(usuario=usuario, activo=True, proyecto__eliminado=False,).select_related("proyecto")
    
    proyectos_encargado = []
    proyectos_ayudante = []
    proyectos_colaborador = []
    
    for participacion in participaciones_activas:
        proyecto = participacion.proyecto
        progreso = calcular_progreso_proyecto(proyecto)
        proyecto.progreso = progreso
        
        if participacion.rol == "encargado_principal":
            proyectos_encargado.append(proyecto)
        elif participacion.rol == "ayudante":
            proyectos_ayudante.append(proyecto)
        elif participacion.rol == "colaborador":
            proyectos_colaborador.append(proyecto)
            
    proyectos_encargado.sort(key=lambda proyecto: proyecto.prioridad, reverse=True)
    proyectos_ayudante.sort(key=lambda proyecto: proyecto.prioridad, reverse=True)
    proyectos_colaborador.sort(key=lambda proyecto: proyecto.prioridad, reverse=True)
    
    return {
        "proyectos_encargado": proyectos_encargado[:5],
        "proyectos_ayudante": proyectos_ayudante[:5],
        "proyectos_colaborador": proyectos_colaborador[:5],
    }
    
    
def obtener_proyecto_para_usuario(usuario, proyecto_id):
    participacion = Participacion.objects.filter(
        usuario=usuario,
        proyecto_id=proyecto_id,
        activo=True,
        proyecto__eliminado=False,
    ).select_related("proyecto").first()
    
    if participacion is None:
        raise ValidationError("El usuario no participa activamente en este proyecto.")
    
    proyecto = participacion.proyecto
    proyecto.progreso = calcular_progreso_proyecto(proyecto)
    
    return proyecto, participacion


@transaction.atomic
def agregar_participante(usuario, proyecto, nuevo_usuario, nuevo_rol):
    if proyecto.eliminado:
        raise ValidationError("No se pueden agregar participantes a un proyecto eliminado.")
    
    participacion_editor = Participacion.objects.filter(
        usuario=usuario,
        proyecto=proyecto,
        activo=True,
    ).first()
    
    if participacion_editor is None:
        raise ValidationError("El usuario no participa activamente en este proyecto.")
    
    if participacion_editor.rol != "encargado_principal":
        raise ValidationError("Sólo el encargado principal puede agregar participantes.")
    
    if nuevo_rol not in ["ayudante", "colaborador"]:
        raise ValidationError("El rol seleccionado no es válido.")
    
    participacion_existente = Participacion.objects.filter(
        usuario=nuevo_usuario,
        proyecto=proyecto,
        activo=True,
    ).first()
    
    if participacion_existente is not None:
        raise ValidationError("El usuario ya participa activamente en este proyecto.")
    
    if nuevo_rol == "ayudante":
        ayudante_actual = Participacion.objects.filter(
            proyecto=proyecto,
            rol="ayudante",
            activo=True,
        ).first()
        
        if ayudante_actual is not None:
            raise ValidationError("El proyecto ya tiene un ayudante.")
        
    return Participacion.objects.create(
        usuario=nuevo_usuario,
        proyecto=proyecto,
        rol=nuevo_rol,
        activo=True,
    )
    
    
@transaction.atomic
def retirar_participante(usuario, participacion):
    proyecto = participacion.proyecto
    
    if proyecto.eliminado:
        raise ValidationError("No se puede retirar participantes de un proyecto eliminado.")
    
    if not participacion.activo:
        raise ValidationError("No se puede retirar una participación inactiva.")
    
    participacion_editor = Participacion.objects.filter(usuario=usuario, proyecto=proyecto, activo=True,).first()
    
    if participacion_editor is None:
        raise ValidationError("El usuario no participa activamente en este proyecto.")
    
    if participacion_editor.rol != "encargado_principal":
        raise ValidationError("Sólo el encargado principal puede retirar participantes.")
    
    if participacion_editor == participacion:
        raise ValidationError("El encargado principal no puede retirarse mediante esta funcion.")
    
    if participacion.rol == "encargado_principal":
        raise ValidationError("No se puede retirar al encargado principal.")
    
    tareas_activas = Tarea.objects.filter(proyecto=proyecto, responsable=participacion, eliminado=False,).exists()
    
    if tareas_activas:
        raise ValidationError(
            "No se puede retirar al participante mientras tenga tareas activas a su cargo. "
            "Debe reasignar todas sus tareas antes de retirarlo."                
        )
        
    participacion.activo = False
    participacion.save(update_fields=["activo"])
    
    return participacion


def obtener_navegacion_proyectos(usuario, proyecto_actual):
    participaciones = Participacion.objects.filter(usuario=usuario, activo=True, proyecto__eliminado=False,).select_related("proyecto")
    
    proyectos = sorted(
        {participacion.proyecto for participacion in participaciones},
        key=lambda proyecto: (-proyecto.prioridad, proyecto.id),
    )
    
    cantidad = len(proyectos)
    
    if cantidad <= 1:
        return {
            "proyecto_anterior": None,
            "proyecto_siguiente": None,
            "proyecto_primero": None,
        }
        
    indice_actual = next(
        (
            indice
            for indice, proyecto in enumerate(proyectos)
            if proyecto.id == proyecto_actual.id
        ),
        None,
    )
    
    if indice_actual is None:
        return {
            "proyecto_actual": None,
            "proyecto_siguiente": None,
            "proyecto_primero": None,
        }
        
    proyecto_anterior = (
        proyectos[indice_actual - 1]
        if indice_actual > 0
        else None
    )
    
    proyecto_siguiente = (
        proyectos[indice_actual + 1]
        if indice_actual < cantidad - 1
        else None
    )
    
    return{
        "proyecto_anterior": proyecto_anterior,
        "proyecto_siguiente": proyecto_siguiente,
        "proyecto_primero": proyectos[0],
    }
    
    
@transaction.atomic
def eliminar_proyecto(usuario, proyecto):
    if proyecto.eliminado:
        raise ValidationError("El proyecto se encuentra eliminado.")
    
    participacion = Participacion.objects.filter(usuario=usuario, proyecto=proyecto, activo=True).first()
    
    if participacion is None:
        raise ValidationError("El usuario no participa activamente en este proyecto.")
    
    if participacion.rol != "encargado_principal":
        raise ValidationError("Sólo el encargado principal puede eliminar el proyecto.")
    
    proyecto.eliminado = True
    proyecto.save(update_fields=["eliminado"])
    
    return proyecto