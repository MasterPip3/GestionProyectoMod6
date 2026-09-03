

# Preguntas frecuentes

## ¿Qué puedo hacer dentro de un proyecto?

Puedes consultar la información del proyecto y participar en la gestión de sus tareas y participantes según los permisos correspondientes a tu rol.

## ¿Qué diferencia hay entre los roles?

El **Encargado principal** administra el proyecto y posee los permisos de gestión más amplios.

El **Ayudante** puede colaborar en la gestión del proyecto y crear y editar tareas.

El **Colaborador** puede crear sus propias tareas y editarlas, pero no puede eliminar tareas.

## ¿Cómo se calcula el progreso de un proyecto?

El progreso se calcula considerando el estado de las tareas y la importancia de cada una.

La importancia funciona como un peso dentro del cálculo.

Una tarea con importancia 10 tiene diez veces el peso de una tarea con importancia 1.

Los estados representan:

* Pendiente: 0%.
* En progreso: 50%.
* Completada: 100%.

La prioridad del proyecto y la urgencia de las tareas no modifican el cálculo.

## ¿Qué significan las estrellas de prioridad?

Las estrellas representan la prioridad del proyecto en una escala de 1 a 5.

La prioridad permite destacar y ordenar proyectos, pero no participa en el cálculo del progreso.

## ¿Qué diferencia existe entre prioridad, importancia y urgencia?

Son conceptos diferentes:

* **Prioridad:** corresponde al proyecto y utiliza una escala de 1 a 5.
* **Importancia:** corresponde a la tarea y determina su peso dentro del progreso.
* **Urgencia:** indica visualmente qué tan próxima está la fecha de término de una tarea.

La urgencia y la prioridad no modifican el cálculo del progreso.

## ¿Qué ocurre cuando una tarea se acerca a su fecha límite?

La tarea utiliza un indicador visual de urgencia.

La regla definida es:

* Más de 4 días restantes: verde.
* Entre 1 y 4 días restantes: amarillo.
* Tarea completada: indicador de completada.

## ¿Quién puede crear tareas?

El Encargado principal, el Ayudante y el Colaborador pueden crear tareas.

El Colaborador puede crear sus propias tareas y editarlas.

## ¿Quién puede eliminar una tarea?

Solamente el Encargado principal puede eliminar tareas.

La eliminación se realiza de manera lógica.

## ¿Qué ocurre cuando se elimina un proyecto o una tarea?

La aplicación utiliza eliminación lógica.

El registro no se elimina físicamente de la base de datos, sino que se marca como eliminado.

Los elementos eliminados dejan de mostrarse como elementos activos dentro de la aplicación.

## ¿Qué ocurre cuando un participante es retirado?

La participación se desactiva lógicamente.

El registro se conserva, pero deja de considerarse una participación activa dentro del proyecto.

## ¿Puede el encargado principal retirarse del proyecto?

No puede utilizar el flujo normal de retiro de participantes.

Para abandonar el proyecto debe utilizar el flujo específico de salida.

Si existe un Ayudante que pueda asumir el cargo, este pasa a ser el nuevo Encargado principal según las reglas definidas.

## ¿Puede el encargado principal cambiar su propio rol?

No.

El encargado principal no puede cambiar su propio rol mediante el flujo normal de cambio de rol.

Esto evita que el proyecto quede sin encargado principal.

## ¿Cómo se asigna el responsable de una tarea?

El responsable debe corresponder a una participación activa del proyecto.

Si existe una única participación activa disponible, la asignación puede realizarse automáticamente.

Cuando existen varias participaciones disponibles, se puede seleccionar explícitamente el responsable.

## ¿Qué ocurre con las fechas de las tareas?

Las fechas de una tarea deben mantenerse dentro del período definido para el proyecto.

La tarea no puede comenzar antes del inicio del proyecto ni terminar después del término del proyecto.

Además, la fecha de inicio no puede ser posterior a la fecha de término.

## ¿Qué enfoque se utiliza para las vistas?

El proyecto utiliza **Function-Based Views (FBV)**.

Las vistas se implementan mediante funciones de Python que reciben una solicitud HTTP, gestionan el flujo correspondiente y generan una respuesta.

La decisión de utilizar FBV responde al orden de aprendizaje del curso.

Este proyecto corresponde a la práctica de FBV y el siguiente proyecto será desarrollado utilizando CBV.

La decisión no se basa en considerar que FBV sea simplemente más sencillo ni que CBV sea técnicamente más complejo.

## ¿Por qué existe una capa de servicios?

La capa de servicios permite concentrar las reglas de negocio y separar esas responsabilidades de las views.

De esta manera, las views gestionan principalmente el flujo HTTP y los servicios se encargan de operaciones y validaciones relacionadas con el funcionamiento del sistema.

## ¿Por qué se utiliza eliminación lógica?

La eliminación lógica permite conservar los registros en lugar de eliminarlos físicamente.

Esto facilita mantener trazabilidad y permite disponer de la información en caso de que sea necesaria posteriormente.

## ¿La aplicación está pensada para producción?

No.

El proyecto tiene un alcance académico y está diseñado para ejecutarse localmente.

El objetivo principal es aplicar los conceptos estudiados durante el curso mediante una aplicación funcional.

## ¿Qué funcionalidades podrían agregarse en el futuro?

Entre las posibles extensiones se encuentran:

* Cronograma/Gantt.
* Exportación a Excel.
* Sistema de notificaciones.
* Buscador.
* Gestión avanzada de equipos.
* Modo claro.

Estas funcionalidades no forman parte del alcance actual.
