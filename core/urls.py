from django.urls import path
from .views import inicio, dashboard, registro, crear_proyecto_view, detalle_proyecto, crear_tarea_view, editar_tarea_view, eliminar_tarea_view, agregar_participante_view, participantes_proyecto, cambiar_rol_participacion_view, salir_proyecto_view, retirar_participante_view, eliminar_proyecto_view, faq


urlpatterns = [
    path('', inicio, name='inicio'),
    path('dashboard/', dashboard, name='dashboard'),
    path('registro/', registro, name='registro'),
    path('proyectos/crear/', crear_proyecto_view, name='crear_proyecto'),
    path('proyectos/<int:proyecto_id>/', detalle_proyecto, name='detalle_proyecto'),
    path('proyectos/<int:proyecto_id>/tareas/crear/', crear_tarea_view, name='crear_tarea'),
    path('proyectos/<int:proyecto_id>/tareas/<int:tarea_id>/editar/', editar_tarea_view, name='editar_tarea'),
    path('proyectos/<int:proyecto_id>/tareas/<int:tarea_id>/eliminar/', eliminar_tarea_view, name='eliminar_tarea'),
    path('proyectos/<int:proyecto_id>/participantes/agregar/', agregar_participante_view, name='agregar_participante'),
    path('proyectos/<int:proyecto_id>/participantes/', participantes_proyecto, name='participantes_proyecto'),
    path('proyectos/<int:proyecto_id>/participantes/<int:participacion_id>/rol/', cambiar_rol_participacion_view, name='cambiar_rol_participacion'),
    path('proyectos/<int:proyecto_id>/salir', salir_proyecto_view, name='salir_proyecto'),
    path('proyectos/<int:proyecto_id>/participantes/<int:participacion_id>/retirar/', retirar_participante_view, name='retirar_participante'),
    path('proyectos/<int:proyecto_id>/eliminar', eliminar_proyecto_view, name='eliminar_proyecto'),
    path('faq/', faq, name='faq')
]
