
https://github.com/MasterPip3/GestionProyectoMod6.git


# ProyectoModulo6

Aplicación web de gestión de proyectos y tareas desarrollada con Django.

# Gestión de proyectos

Aplicación web desarrollada con Django para la gestión de proyectos, tareas y participantes.

El proyecto permite a los usuarios registrarse, autenticarse, crear y gestionar proyectos, administrar tareas y participantes y consultar el progreso de los proyectos según las reglas definidas para cada rol.

> **Estado:** Desarrollo en curso. Este documento corresponde a una versión provisional y será consolidado antes de la entrega final.

---

## 1. Objetivo del proyecto

Desarrollar una aplicación web de gestión de proyectos que permita organizar proyectos, tareas y participantes de forma centralizada.

La aplicación contempla:

* Registro y autenticación de usuarios.
* Creación y gestión de proyectos.
* Gestión de tareas asociadas a proyectos.
* Asignación de responsables.
* Gestión de participantes y roles.
* Cálculo de progreso de los proyectos.
* Indicadores visuales de prioridad y urgencia.
* Restricciones de acceso según el rol del usuario.
* Eliminación lógica de proyectos y tareas.
* Navegación entre proyectos.
* Interfaz responsiva orientada principalmente a escritorio.

---

## 2. Tecnologías

* Python 3.14.6
* Django 6.1
* SQLite para desarrollo
* MySQL para producción
* HTML
* CSS
* JavaScript
* Bootstrap
* Lucide Icons
* Tipografía Inter

---

## 3. Arquitectura

El proyecto utiliza una separación por responsabilidades.

### Views

Las views reciben las solicitudes HTTP, coordinan la operación correspondiente y preparan el contexto necesario para las plantillas.

### Services

La lógica de negocio se concentra en la capa de servicios.

Entre las responsabilidades de esta capa se encuentran:

* Crear proyectos.
* Crear y gestionar tareas.
* Agregar participantes.
* Cambiar roles.
* Retirar participantes.
* Salir de proyectos.
* Eliminar proyectos lógicamente.
* Validar permisos y reglas de negocio.
* Obtener información necesaria para el dashboard y la navegación.

### Templates

Los templates se encargan de representar la información entregada por las views.

Se utiliza herencia de templates mediante `base.html`.

### Static

Los recursos estáticos contienen principalmente:

* CSS.
* JavaScript.
* Otros recursos necesarios para la interfaz.

---

## 4. Autenticación y autorización

La autenticación utiliza el sistema incorporado de Django.

Los usuarios pueden:

* Crear una cuenta.
* Iniciar sesión.
* Cerrar sesión.

Las vistas internas requieren autenticación.

La autorización relacionada con los proyectos se determina mediante la participación activa del usuario y su rol dentro del proyecto.

---

## 5. Roles de proyecto

Cada usuario posee un único rol dentro de un proyecto.

Los roles definidos son:

1. Encargado principal
2. Ayudante
3. Colaborador

### Encargado principal

Es el responsable principal del proyecto.

Puede:

* Agregar participantes.
* Cambiar roles.
* Retirar participantes.
* Eliminar el proyecto lógicamente.
* Eliminar tareas.

El encargado principal no puede simplemente retirarse mediante la función de retiro de participantes.

Cuando corresponda abandonar un proyecto, se utiliza el flujo específico definido para salir del proyecto.

### Ayudante

Puede participar en la gestión del proyecto de acuerdo con los permisos definidos.

Si el encargado principal abandona el proyecto bajo las condiciones establecidas, el ayudante pasa a ocupar el rol de encargado principal.

### Colaborador

Puede participar en la gestión de tareas según los permisos definidos.

No puede eliminar tareas.

---

## 6. Proyectos

Cada proyecto contiene, entre otros datos:

* Nombre.
* Descripción.
* Fecha de inicio.
* Fecha de término.
* Prioridad.
* Progreso.
* Estado de eliminación lógica.

La prioridad del proyecto utiliza una escala de 1 a 5 y se representa visualmente mediante estrellas.

La prioridad sirve para destacar y ordenar proyectos y no participa directamente en el cálculo del progreso.

---

## 7. Tareas

Las tareas pertenecen a un proyecto.

Sus principales atributos incluyen:

* Nombre.
* Descripción.
* Fecha de inicio.
* Fecha de término.
* Importancia.
* Estado.
* Responsable.
* Estado de eliminación lógica.

La importancia de la tarea utiliza una escala de 1 a 10.

La importancia determina el peso de la tarea dentro del cálculo del progreso ponderado.

---

## 8. Cálculo de progreso

El progreso del proyecto se determina a partir del avance de sus tareas y considerando la importancia de cada una.

Estados definidos:

* Pendiente: 0%.
* En progreso: 50% del valor correspondiente a su importancia.
* Completada: 100% del valor correspondiente a su importancia.

La importancia de una tarea funciona como peso relativo: una tarea con importancia 10 tiene diez veces el peso de una tarea con importancia 1.

La prioridad del proyecto no interviene en este cálculo.

---

## 9. Urgencia de las tareas

La urgencia es independiente de la importancia.

Se representa mediante un indicador visual tipo semáforo.

Las tareas pendientes presentan:

* Verde: más de 4 días restantes.
* Amarillo: entre 1 y 4 días restantes.
* Las tareas completadas utilizan un indicador diferenciado.

La urgencia no modifica el peso de la tarea dentro del progreso.

---

## 10. Eliminación lógica

La eliminación de proyectos y tareas se realiza mediante eliminación lógica en lugar de eliminación física.

Esto permite conservar los registros y facilita futuras necesidades de auditoría o registro histórico.

Los elementos eliminados no deben aparecer como elementos activos dentro de la aplicación.

Un proyecto eliminado tampoco puede continuar siendo gestionado normalmente.

---

## 11. Dashboard

El dashboard constituye la página principal de los usuarios autenticados.

Los proyectos se organizan en tres categorías:

* Proyectos donde el usuario es encargado principal.
* Proyectos donde el usuario es ayudante.
* Proyectos donde el usuario es colaborador.

Cada categoría dispone de su propio visor de proyectos.

Los visores utilizan un carrusel de navegación visual.

La interacción definida es:

* Hasta 5 proyectos: se mantiene un único visor.
* Más de 5 proyectos: se muestran grupos de 5.
* El desplazamiento es manual.
* Cada visor funciona independientemente.
* En móvil se conserva el comportamiento horizontal del visor.
* Las tarjetas se muestran verticalmente dentro de cada página del carrusel.

El carrusel corresponde a una decisión de interfaz y su interacción se gestiona mediante JavaScript.

---

## 12. Tarjetas de proyecto

Las tarjetas muestran únicamente la información definida para el dashboard.

La tarjeta contiene:

* Etiqueta de proyecto.
* Nombre.
* Descripción resumida.
* Fechas.
* Progreso.
* Rol correspondiente.
* Prioridad mediante estrellas.

La descripción se limita visualmente para evitar que textos extensos deformen la tarjeta. Para consultar la descripción completa, el usuario debe ingresar al proyecto.

Toda la tarjeta es clickeable y conduce al detalle del proyecto.

---

## 13. Interfaz visual

La aplicación utiliza un diseño:

* Oscuro.
* Moderno.
* Tecnológico.
* Simple.
* Orientado a organización, energía y acción.

La paleta utiliza tonos oscuros acompañados de colores neón de forma controlada.

Se utiliza:

* Fondo oscuro.
* Superficies en gris oscuro.
* Texto blanco.
* Colores neón para elementos destacados.
* Glow sutil.
* Bordes ligeramente redondeados.
* Microanimaciones.

La tipografía principal es **Inter**.

Los iconos utilizan **Lucide**.

---

## 14. Navbar

Las páginas internas utilizan una barra de navegación horizontal.

La estructura principal es:

**Gestión de proyectos — Dashboard — Proyectos**

y en el lado derecho:

**usuario: usuario — Logout**

En pantallas pequeñas la navegación se transforma en un menú hamburguesa.

El modo claro queda documentado como una posible extensión futura, pero la implementación actual utiliza exclusivamente modo oscuro.

---

## 15. Formularios

Los formularios comparten un estilo visual común.

Características definidas:

* Centrado horizontal y vertical.
* Diseño orientado a una pantalla simple.
* Padding lateral mínimo del 10%.
* Campos centrados.
* Campos de igual ancho.
* Etiquetas con mayor peso visual que los inputs.
* Descripción con mayor altura que los campos normales.
* Sin expansión vertical inesperada de los inputs.
* Responsividad escritorio → tableta → móvil.
* Focus automático en el primer campo.
* Botones con formato común.
* Botones de eliminación visualmente diferenciados.

Las reglas de validación permanecen activas internamente aunque determinados mensajes de ayuda técnica no se muestran visualmente para mantener una interfaz limpia.

---

## 16. Seguridad

El proyecto utiliza mecanismos proporcionados por Django, entre ellos:

* Sistema de autenticación.
* Protección CSRF.
* Restricción de vistas mediante autenticación.
* Validaciones en formularios.
* Validaciones adicionales en la capa de servicios.
* Control de permisos según rol.

Las validaciones de seguridad y negocio no dependen exclusivamente de la interfaz.

---

## 17. Responsividad

La aplicación está diseñada principalmente para escritorio, pero contempla tres rangos:

1. Escritorio.
2. Tableta.
3. Móvil.

Se mantiene el contenido centrado y se evita el desplazamiento horizontal general de la página.

Cuando el contenido supera la altura disponible, se permite desplazamiento vertical.

Los visores de proyectos mantienen su interacción horizontal específica.

---

## 18. Decisión sobre FBV

Este proyecto utiliza **Function-Based Views (FBV)**.

La decisión de utilizar FBV no se debe a que el proyecto sea considerado más sencillo ni a que CBV sea técnicamente más complejo.

La decisión responde al orden de aprendizaje del curso:

* Este proyecto corresponde a la práctica de FBV.
* El siguiente proyecto será desarrollado utilizando CBV.

De esta manera se busca practicar explícitamente ambos enfoques en proyectos diferentes y respetar el orden en que fueron enseñados durante el curso.

---

## 19. Mejoras y extensiones futuras

Quedan consideradas como posibles extensiones:

* Modo claro seleccionable por el usuario.
* Gestión avanzada de equipos.
* Buscador.
* Cronograma/Gantt.
* Exportación a Excel.
* Sistema de notificaciones.
* Otras funcionalidades que puedan incorporarse posteriormente.

Estas extensiones no forman parte de los requisitos actuales salvo que sean incorporadas explícitamente durante el desarrollo.

---

## 20. Estado del proyecto

El proyecto se encuentra en etapa de implementación de la interfaz definitiva.

Las funcionalidades principales de:

* autenticación;
* proyectos;
* tareas;
* participantes;
* roles;
* navegación;
* salida de proyectos;
* retiro de participantes;
* eliminación lógica;

se encuentran en proceso de consolidación y pruebas.

La interfaz se está implementando directamente orientada al producto final, evitando HTML visual provisional.

---

## 21. Documentación complementaria

El proyecto contempla además:

* README.
* Bitácora de desarrollo.
* FAQ/tutorial.

La bitácora registrará decisiones relevantes tomadas durante el desarrollo.

La FAQ/tutorial explicará conceptos y decisiones que puedan generar dudas durante la revisión del proyecto.

<!--
* DECISIÓN ACADÉMICA IMPORTANTE:
La utilización explícita de FBV en este proyecto se debe a que corresponde a la práctica de FBV del curso. El siguiente proyecto será desarrollado con CBV por el orden en que fueron aprendidos ambos enfoques, NO porque FBV haya sido considerado más sencillo o CBV más complejo.
-->
