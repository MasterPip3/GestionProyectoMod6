

# Bitácora de desarrollo — ProyectoModulo6

## 1. Inicio del proyecto

**Fecha:** 22/08/2026

### Estado inicial

* Python 3.14.6.
* Django 6.1.
* Proyecto Django: `config`.
* Aplicación inicial: `core`.
* Desarrollo orientado a ejecución local.
* Enfoque académico.

---

## 2. Decisión sobre el enfoque de Views

Se decidió utilizar **Function-Based Views (FBV)** para este proyecto.

La decisión responde al orden de aprendizaje del curso.

El objetivo es utilizar este proyecto para practicar FBV y utilizar CBV en un proyecto posterior.

La elección no se realizó considerando que uno de los dos enfoques sea técnicamente superior o que CBV sea simplemente más complejo.

---

## 3. Separación de responsabilidades

Se decidió incorporar una capa de servicios para separar las reglas de negocio de las views.

Las views se encargan principalmente de:

* Recibir solicitudes.
* Controlar el flujo HTTP.
* Preparar formularios.
* Preparar el contexto.
* Renderizar templates.
* Redireccionar.

La capa de servicios concentra:

* Reglas de negocio.
* Validación de permisos.
* Operaciones sobre proyectos.
* Operaciones sobre tareas.
* Gestión de participantes.
* Cálculo del progreso.
* Eliminación lógica.
* Navegación relacionada con proyectos.

Se mantuvo `services.py` como un único archivo mientras su tamaño y responsabilidad permitieran mantener una organización clara.

---

## 4. Roles

Se definieron tres roles:

1. Encargado principal.
2. Ayudante.
3. Colaborador.

El usuario que crea un proyecto se convierte automáticamente en encargado principal.

Cada usuario puede tener un único rol activo dentro de un proyecto.

---

## 5. Reglas del encargado principal

Se estableció que siempre debe existir un encargado principal mientras el proyecto tenga una participación activa correspondiente.

El encargado principal:

* Puede administrar participantes.
* Puede cambiar roles.
* Puede retirar participantes.
* Puede crear y editar tareas.
* Puede eliminar tareas.
* Puede eliminar el proyecto lógicamente.

No puede cambiar su propio rol mediante el flujo normal de cambio de rol.

Tampoco puede retirarse mediante la función normal de retiro de participantes.

Para abandonar un proyecto se definió un flujo específico.

---

## 6. Salida del encargado principal

Se estableció que, cuando el encargado principal abandona un proyecto y existe un ayudante disponible, este pasa a ocupar el rol de encargado principal.

Debido a la importancia de esta operación, se implementó una confirmación adicional antes de completar la transferencia.

---

## 7. Gestión de participantes

La participación se implementó mediante una entidad independiente relacionada con usuario y proyecto.

La participación posee un estado activo.

El retiro de un participante se realiza mediante desactivación lógica en lugar de eliminar el registro.

También se estableció que no se debe retirar al encargado principal mediante el flujo normal de retiro.

---

## 8. Gestión de tareas

Las tareas pertenecen a un proyecto y poseen un responsable correspondiente a una participación activa.

Se establecieron permisos por rol.

El encargado principal y el ayudante pueden crear tareas.

El colaborador puede crear sus propias tareas y editarlas.

El colaborador no puede eliminar tareas.

El encargado principal es el único rol autorizado para eliminar tareas.

---

## 9. Asignación de responsables

Se decidió que el responsable de una tarea debe corresponder a un participante activo del proyecto.

Cuando existe una única participación activa disponible, la asignación puede realizarse automáticamente.

Cuando existen varias participaciones disponibles, el responsable puede seleccionarse explícitamente.

---

## 10. Importancia de las tareas

Se estableció una escala de importancia de 1 a 10.

La importancia funciona como peso relativo para el cálculo del progreso.

Una tarea con importancia 10 pesa diez veces una tarea con importancia 1.

La importancia no representa la urgencia.

---

## 11. Prioridad de los proyectos

Se estableció una escala de prioridad de 1 a 5.

La prioridad se representa mediante estrellas.

La prioridad se utiliza para destacar y ordenar proyectos.

Se decidió mantenerla independiente del cálculo del progreso.

---

## 12. Cálculo del progreso

Se decidió utilizar un cálculo ponderado por la importancia de las tareas.

Los estados representan:

* Pendiente: 0%.
* En progreso: 50%.
* Completada: 100%.

La importancia de cada tarea actúa como peso.

La prioridad del proyecto y la urgencia de las tareas no intervienen en el cálculo.

El resultado se presenta con dos decimales.

---

## 13. Urgencia de tareas

Se definió un indicador visual independiente del progreso y de la prioridad.

Las reglas acordadas son:

* Más de 4 días restantes: verde.
* Entre 1 y 4 días restantes: amarillo.
* Tarea completada: indicador de completada.

---

## 14. Eliminación lógica

Se decidió utilizar eliminación lógica para proyectos y tareas.

El objetivo es evitar eliminar físicamente los registros y conservar información que pueda ser relevante para trazabilidad o futuras necesidades de auditoría.

Los elementos eliminados deben dejar de aparecer como elementos activos dentro de la aplicación.

Las participaciones también pueden desactivarse lógicamente.

---

## 15. Dashboard

Se definieron tres categorías:

* Encargado principal.
* Ayudante.
* Colaborador.

Cada categoría posee un visor independiente.

Las tarjetas muestran información resumida del proyecto:

* Nombre.
* Descripción.
* Fechas.
* Progreso.
* Rol.
* Prioridad.

La descripción se limita visualmente en la tarjeta y puede consultarse completa en el detalle del proyecto.

---

## 16. Carrusel

Se decidió utilizar un carrusel gestionado mediante JavaScript.

La regla visual es mostrar los proyectos en grupos de cinco.

Cada visor debe funcionar independientemente.

---

## 17. Diseño visual

Se estableció una identidad visual transversal para toda la aplicación:

* Modo oscuro.
* Estética tecnológica/Cyberpunk equilibrada.
* Inter.
* Lucide Icons.
* Bootstrap.
* Colores neón utilizados de forma controlada.
* Glow sutil.
* Bordes redondeados.
* Microanimaciones.
* Diseño responsivo.

Se decidió reutilizar las clases CSS existentes y evitar duplicaciones innecesarias.

---

## 18. Formularios

Se decidió utilizar formularios de Django y `ModelForm` cuando correspondía.

Para mantener control sobre la interfaz se dejó de depender visualmente de `form.as_p` y se implementó el recorrido manual de los campos visibles.

De esta manera se pueden controlar:

* Etiquetas.
* Campos.
* Mensajes de error.
* Ayuda.
* Estructura visual.

Las validaciones internas se mantienen aunque determinados textos de ayuda técnica se oculten visualmente.

---

## 19. Django Admin

Se registraron los modelos principales en Django Admin.

Posteriormente se personalizó el panel mediante clases `ModelAdmin`.

La personalización incluye columnas, filtros y búsqueda.

Modelos administrados:

* Proyecto.
* Tarea.
* Participación.

---

## 20. Seguridad

Se utilizaron mecanismos proporcionados por Django:

* Autenticación.
* Protección CSRF.
* Restricción de vistas mediante autenticación.
* Validaciones de formularios.
* Validaciones de negocio en servicios.
* Control de permisos por rol.

Se mantuvo la validación de reglas importantes en la capa de servicios para evitar depender exclusivamente de la interfaz.

---

## 21. Documentación

Se definieron tres elementos de documentación:

### README

Explica:

* Objetivo.
* Tecnologías.
* Arquitectura.
* Instalación.
* Funcionamiento.
* Reglas de negocio.
* Alcance.
* Estado.

### Bitácora

Registra decisiones y evolución del proyecto.

### FAQ

Explica conceptos y decisiones que puedan generar dudas durante la revisión.

---

## 22. Alcance académico

Se decidió mantener el proyecto dentro de un alcance académico y local.

No se incorporarán como requisitos:

* Despliegue de producción.
* Infraestructura empresarial.
* Arquitecturas distribuidas.
* Funcionalidades innecesarias para el objetivo del curso.

Las extensiones como Gantt, exportación a Excel y notificaciones quedan como posibilidades futuras.

---

## 23. Estado final de la etapa de desarrollo

Antes de la etapa de pruebas se deben completar:

1. Preparación de una entrega limpia.
2. Eliminación de datos de prueba.
3. Implementación de pruebas automatizadas.

Después de estas etapas se realizará la revisión final del código.
