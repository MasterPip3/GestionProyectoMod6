from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Case, When, Value, IntegerField
from django.db.models.functions import Lower
from .forms import RegistroForm, ProyectoForm, TareaForm, ParticipacionForm, CambiarRolForm
from .services import crear_proyecto, obtener_proyectos_dashboard, obtener_proyecto_para_usuario, crear_tarea, editar_tarea, eliminar_tarea, agregar_participante, cambiar_rol_participacion, salir_proyecto, retirar_participante, obtener_navegacion_proyectos, eliminar_proyecto

# Create your views here.
def inicio(request):
    return render(request, "inicio.html")


@login_required
def dashboard(request):
    proyectos = obtener_proyectos_dashboard(request.user)
    
    contexto = {
        'usuario': request.user,
        **proyectos,
    }
    
    return render(request, 'dashboard.html', contexto)


def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect("login")
        
    else:
        form = RegistroForm()
    
    return render(request, 'registration/registro.html', {'form': form,})


@login_required
def crear_proyecto_view(request):
    if request.method == "POST":
        form = ProyectoForm(request.POST)
        
        if form.is_valid():
            try:
                crear_proyecto(request.user, form.cleaned_data)
            except ValidationError as error:
                form.add_error(None, error)
            else:
                return redirect("dashboard")
            
    else:
        form = ProyectoForm()
        
    return render(request, 'proyectos/crear_proyecto.html', {"form": form},)


@login_required
def detalle_proyecto(request, proyecto_id):
    try:
        proyecto, participacion = obtener_proyecto_para_usuario(request.user, proyecto_id,)
    except ValidationError:
        messages.warning(
            request,
            "El proyecto ya no está disponible porque fue eliminado."
        )
        return redirect("dashboard")
    
    tareas = proyecto.tareas.filter(eliminado=False,).select_related("responsable__usuario")
    
    navegacion = obtener_navegacion_proyectos(request.user, proyecto)
    
    contexto = {
        "usuario": request.user,
        "proyecto": proyecto,
        "participacion": participacion,
        "tareas": tareas,
        **navegacion,
    }
    
    return render(request, "proyectos/detalle_proyecto.html", contexto,)


@login_required
def crear_tarea_view(request, proyecto_id):
    proyecto, participacion = obtener_proyecto_para_usuario(request.user, proyecto_id,)
    
    if request.method == "POST":
        form = TareaForm(request.POST, proyecto=proyecto, usuario=request.user,)
        
        if form.is_valid():
            try:
                crear_tarea(request.user, proyecto, form.cleaned_data,)
            except ValidationError as error:
                form.add_error(None, error)
            else:
                return redirect("detalle_proyecto", proyecto_id=proyecto.id)

    else:
        form = TareaForm(proyecto=proyecto, usuario=request.user,)
        
    contexto = {
        "usuario": request.user,
        "proyecto": proyecto,
        "participacion": participacion,
        "form": form,
    }
    
    return render(request, "proyectos/crear_tarea.html", contexto,)


@login_required
def editar_tarea_view(request, proyecto_id, tarea_id):
    proyecto, participacion = obtener_proyecto_para_usuario(request.user, proyecto_id,)
    
    tarea = proyecto.tareas.filter(pk=tarea_id, eliminado=False,).first()
    
    if tarea is None:
        raise Http404("La tarea no existe.")
    
    if request.method == "POST":
        form = TareaForm(
            request.POST,
            instance=tarea,
            proyecto=proyecto,
            usuario=request.user,
        )
        
        if form.is_valid():
            try:
                editar_tarea(request.user, tarea, form.cleaned_data,)
            except ValidationError as error:
                form.add_error(None, error)
            else:
                return redirect("detalle_proyecto", proyecto_id=proyecto.id,)
        
    else:
        form = TareaForm(
            instance=tarea,
            proyecto=proyecto,
            usuario=request.user,
        )
        
    contexto = {
        "usuario": request.user,
        "proyecto": proyecto,
        "participacion": participacion,
        "tarea": tarea,
        "form": form,
    }
    
    return render(request, "proyectos/editar_tarea.html", contexto)


@login_required
def eliminar_tarea_view(request, proyecto_id, tarea_id):
    proyecto, participacion = obtener_proyecto_para_usuario(request.user, proyecto_id,)
    
    tarea = proyecto.tareas.filter(pk=tarea_id, eliminado=False,).first()
    
    if tarea is None:
        raise Http404("La tarea no existe.")
    
    if request.method == "POST":
        eliminar_tarea(request.user, tarea,)
        
        return redirect("detalle_proyecto", proyecto_id=proyecto.id,)
    
    return redirect("detalle_proyecto", proyecto_id=proyecto.id)

@login_required
def agregar_participante_view(request, proyecto_id):
    proyecto, participacion = obtener_proyecto_para_usuario(request.user, proyecto_id,)
    
    if participacion.rol != "encargado_principal":
        raise PermissionDenied("Sólo el encargado principal puede agregar participantes.")
    
    if request.method == "POST":
        form = ParticipacionForm(request.POST, proyecto=proyecto,)
        
        if form.is_valid():
            try:
                agregar_participante(
                    request.user,
                    proyecto,
                    form.cleaned_data["usuario"],
                    form.cleaned_data["rol"],
                )
            except ValidationError as error:
                form.add_error(None, error)
            else:
                return redirect("detalle_proyecto", proyecto_id=proyecto.id,)
        
    else:
        form = ParticipacionForm(proyecto=proyecto,)
        
    contexto = {
        "usuario": request.user,
        "proyecto": proyecto,
        "participacion": participacion,
        "form": form,
    }
    
    return render(request, "proyectos/agregar_participante.html", contexto,)


@login_required
def participantes_proyecto(request, proyecto_id):
    proyecto, participacion = obtener_proyecto_para_usuario(request.user, proyecto_id)
    
    participantes = proyecto.participaciones.filter(activo=True,).select_related("usuario").annotate(
        orden_rol=Case(
            When(rol="encargado_principal", then=Value(1)),
            When(rol="ayudante", then=Value(2)),
            When(rol="colaborador", then=Value(3)),
            output_field=IntegerField(),
        )
    ).order_by(
        "orden_rol",
        Lower("usuario__username"),
        
    )
    
    contexto = {
        "usuario": request.user,
        "proyecto": proyecto,
        "participacion": participacion,
        "participantes": participantes,
    }
    
    return render(request, "proyectos/participantes_proyecto.html", contexto)


@login_required
def cambiar_rol_participacion_view(request, proyecto_id, participacion_id):
    proyecto, participacion_editor = obtener_proyecto_para_usuario(request.user, proyecto_id,)
    
    if participacion_editor.rol != "encargado_principal":
        raise PermissionDenied("Sólo el encargado principal puede cambiar roles.")
    
    participacion_objetivo = proyecto.participaciones.filter(pk=participacion_id, activo=True,).select_related("usuario").first()
    
    if participacion_objetivo is None:
        raise Http404("La participación no existe.")
    
    if participacion_objetivo == participacion_editor:
        raise PermissionDenied("El encargado principal no puede cambiar su propio rol. Para ver solución ver FAQs.")
    
    if request.method == "POST":
        form = CambiarRolForm(request.POST)
        
        if form.is_valid():
            try:
                cambiar_rol_participacion(
                    request.user,
                    participacion_objetivo,
                    form.cleaned_data["rol"],
                )
            except ValidationError as error:
                form.add_error(None, error)
            else:
                return redirect("participantes_proyecto", proyecto_id=proyecto.id)
        
    else:
        form = CambiarRolForm(initial={"rol": participacion_objetivo.rol,})
        
        contexto = {
            "usuario": request.user,
            "proyecto": proyecto,
            "participacion": participacion_editor,
            "participacion_objetivo": participacion_objetivo,
            "form": form,
        }
        
        return render(request, "proyectos/cambiar_rol_participacion.html", contexto)
    
    
@login_required
def retirar_participante_view(request, proyecto_id, participacion_id):
    proyecto, participacion_editor = obtener_proyecto_para_usuario(request.user, proyecto_id)
    
    if participacion_editor.rol != "encargado_principal":
        raise ValidationError("Sólo el encargado principal puede retirar participantes.")
    
    participacion_objetivo = proyecto.participaciones.filter(pk=participacion_id, activo=True).select_related("usuario").first()
    
    if participacion_objetivo is None:
        raise Http404("La participación no existe.")
    
    if participacion_objetivo == participacion_editor:
        raise PermissionDenied("El encargado principal no puede retirarse mediante esta función.")
    
    if request.method == "POST":
        try:
            retirar_participante(
                request.user,
                participacion_objetivo,
            )
        except ValidationError as error:
            contexto = {
                "usuario": request.user,
                "proyecto": proyecto,
                "participacion": participacion_editor,
                "participacion_objetivo": participacion_objetivo,
                "error": error,
            }
            
            return render(request, "proyectos/retirar_participante.html", contexto)
        
        return redirect("participantes_proyecto", proyecto_id=proyecto.id)
    
    contexto = {
        "usuario": request.user,
        "proyecto": proyecto,
        "participacion": participacion_editor,
        "participacion_objetivo": participacion_objetivo,
    }
    
    return render(request, "proyectos/retirar_participante.html", contexto)
    
    
@login_required
def salir_proyecto_view(request, proyecto_id):
    proyecto, participacion = obtener_proyecto_para_usuario(request.user, proyecto_id)
    
    if request.method == "POST":
        
        if participacion.rol == "encargado_principal" and "confirmar_transferencia" not in request.POST:
            return render(
                request,
                "proyectos/confirmar_salida_encargado.html",
                {
                    "usuario": request.user,
                    "proyecto": proyecto,
                    "participacion": participacion,
                },
            )
        
        try:
            salir_proyecto(request.user, proyecto)
        except ValidationError as error:
            contexto = {
                "usuario": request.user,
                "proyecto": proyecto,
                "participacion": participacion,
                "error": error,
            }
            
            return render(request, "proyectos/salir_proyecto.html", contexto)
            
        return redirect("dashboard")
    
    contexto = {
        "usuario": request.user,
        "proyecto": proyecto,
        "participacion": participacion,
    }
    
    return render(request, "proyectos/salir_proyecto.html", contexto)


@login_required
def eliminar_proyecto_view(request, proyecto_id):
    proyecto, participacion = obtener_proyecto_para_usuario(request.user, proyecto_id)
    
    if participacion.rol != "encargado_principal":
        raise PermissionDenied("Sólo el encargado principal puede eliminar el proyecto.")
    
    if request.method == "POST":
        try:
            eliminar_proyecto(request.user, proyecto)
        except ValidationError as error:
            contexto = {
                "usuario": request.user,
                "proyecto": proyecto,
                "participacion": participacion,
                "error": error,
            }
            
            return render(request, "proyectos/eliminar_proyecto.html", contexto)
        
        return redirect("dashboard")
    
    contexto = {
        "usuario": request.user,
        "proyecto": proyecto,
        "participacion": participacion,
    }
    
    return render(request, "proyectos/eliminar_proyecto.html", contexto)


@login_required
def faq(request):
    contexto = {
        "usuario": request.user,
    }

    return render(request, "faq.html", contexto)