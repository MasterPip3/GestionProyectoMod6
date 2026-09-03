# ProyectoModulo6

Aplicación web de gestión de proyectos, tareas y participantes desarrollada con Django como proyecto académico.

Repositorio:

https://github.com/MasterPip3/GestionProyectoMod6.git

---

## 1. Descripción

ProyectoModulo6 permite gestionar proyectos de trabajo, sus tareas y los participantes asociados.

La aplicación incorpora autenticación de usuarios, administración de proyectos, gestión de tareas, roles dentro de cada proyecto, cálculo de progreso ponderado, indicadores visuales y eliminación lógica.

El proyecto está desarrollado con un enfoque académico y está destinado a ejecutarse localmente.

---

## 2. Objetivos

El proyecto busca aplicar los principales conceptos de desarrollo web con Django estudiados durante el curso, incluyendo:

* Autenticación y registro de usuarios.
* Autorización según roles.
* Modelos y relaciones mediante el ORM de Django.
* Formularios y validaciones.
* Function-Based Views (FBV).
* Separación de lógica mediante una capa de servicios.
* Herencia de templates.
* Django Admin.
* Protección CSRF.
* Operaciones CRUD.
* Eliminación lógica.
* Interfaz dinámica mediante JavaScript.
* Diseño responsivo.

---

## 3. Tecnologías

* Python 3.14.6
* Django 6.1
* SQLite
* HTML
* CSS
* JavaScript
* Bootstrap
* Lucide Icons
* Tipografía Inter

La aplicación utiliza SQLite para su ejecución local.

---

## 4. Instalación

### 4.1. Requisitos

Se requiere tener instalado:

* Python 3.14.6 o una versión compatible con el proyecto.
* Git, si se desea clonar el repositorio.

### 4.2. Clonar el repositorio

Desde una terminal:

```bash
git clone https://github.com/MasterPip3/GestionProyectoMod6.git
```

Ingresar a la carpeta:

```bash
cd GestionProyectoMod6
```

### 4.3. Crear el entorno virtual

```bash
python -m venv venv
```

En Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

En Windows CMD:

```cmd
venv\Scripts\activate
```

### 4.4. Instalar Django

En caso de instalar las dependencias manualmente:

```bash
pip install "Django==6.1"
```

### 4.5. Aplicar las migraciones

Desde la carpeta que contiene `manage.py`:

```bash
python manage.py migrate
```

### 4.6. Crear un usuario administrador

Para acceder al panel de administración de Django:

```bash
python manage.py createsuperuser
```

Seguir las instrucciones mostradas por Django.

### 4.7. Ejecutar el servidor

```bash
python manage.py runserver
```

La aplicación estará disponible localmente en:

```text
http://127.0.0.1:8000/
```

La página principal corresponde a la raíz del sitio.

El panel de administración se encuentra en:

```text
http://127.0.0.1:8000/admin/
```

---

## 5. Arquitectura

El proyecto utiliza una separación de responsabilidades basada en Django y una capa de servicios para concentrar la lógica de negocio.

### Views

Las views reciben las solicitudes HTTP, controlan el flujo de cada operación y preparan el contexto que será enviado a los templates.

El proyecto utiliza **Function-Based Views (FBV)**.

### Services

La capa de servicios concentra las reglas de negocio y las operaciones que requieren coordinación entre modelos.

Entre sus responsabilidades se encuentran:

* Crear proyectos.
* Obtener proyectos para el dashboard.
* Crear tareas.
* Editar tareas.
* Eliminar tareas lógicamente.
* Agregar participantes.
* Cambiar roles.
* Retirar participantes.
* Salir de proyectos.
* Transferir el rol de encargado principal cuando corresponde.
* Eliminar proyectos lógicamente.
* Validar permisos y reglas de negocio.
* Calcular el progreso de los proyectos.
* Obtener información necesaria para la navegación.

### Models

Los modelos representan las entidades principales del sistema y sus relaciones.

Las entidades principales son:

* `Proyecto`
* `Tarea`
* `Participacion`

### Forms

Los formularios utilizan `forms.Form`, `forms.ModelForm` y las herramientas de autenticación proporcionadas por Django.

Los formularios realizan validaciones de entrada y permiten controlar los campos que se presentan al usuario.

### Templates

Los templates representan la información preparada por las views.

Se utiliza herencia mediante `base.html`.

### Static

Los archivos estáticos contienen principalmente:

* CSS.
* JavaScript.

---

## 6. Autenticación y autorización

La autenticación utiliza el sistema incorporado de Django.

Los usuarios pueden:

* Registrarse.
* Iniciar sesión.
* Cerrar sesión.

Las vistas internas requieren autenticación.

La autorización dentro de un proyecto depende de la participación activa del usuario y del rol que tenga asignado.

Las validaciones de permisos también se realizan en la capa de servicios para evitar depender exclusivamente de la interfaz.

---

## 7. Roles

Cada usuario posee un único rol activo dentro de un proyecto.

Los roles son:

1. Encargado principal.
2. Ayudante.
3. Colaborador.

### Encargado principal

El encargado principal puede:

* Agregar participantes.
* Cambiar roles.
* Retirar participantes.
* Crear tareas.
* Editar tareas.
* Eliminar tareas.
* Eliminar el proyecto lógicamente.

El encargado principal no puede cambiar su propio rol mediante el flujo normal de cambio de rol.

Tampoco puede retirarse mediante la función destinada a retirar participantes.

Si desea abandonar el proyecto, debe utilizar el flujo específico de salida.

Cuando corresponde y existe un ayudante, este pasa a ser el nuevo encargado principal.

### Ayudante

El ayudante puede:

* Crear tareas.
* Editar tareas.
* Participar en la gestión del proyecto según los permisos definidos.

Si el encargado principal abandona el proyecto bajo las condiciones establecidas, el ayudante puede asumir el rol de encargado principal.

### Colaborador

El colaborador puede:

* Crear sus propias tareas.
* Editar sus tareas.
* Participar en el trabajo del proyecto.

El colaborador no puede eliminar tareas.

---

## 8. Proyectos

Cada proyecto posee:

* Nombre.
* Descripción.
* Fecha de inicio.
* Fecha de término.
* Prioridad.
* Progreso.
* Estado de eliminación lógica.

El usuario que crea un proyecto se convierte automáticamente en su encargado principal.

La fecha de inicio se establece automáticamente con la fecha actual al crear el proyecto.

La fecha de término debe respetar las validaciones establecidas para el proyecto.

### Prioridad

La prioridad utiliza una escala de 1 a 5.

Se representa visualmente mediante estrellas.

La prioridad sirve para destacar y ordenar proyectos, pero no participa en el cálculo del progreso.

---

## 9. Tareas

Cada tarea pertenece a un proyecto y tiene un responsable correspondiente a una participación activa dentro del proyecto.

Sus principales atributos son:

* Nombre.
* Descripción.
* Fecha de inicio.
* Fecha de término.
* Importancia.
* Estado.
* Responsable.
* Eliminación lógica.

La importancia utiliza una escala de 1 a 10.

Una tarea con importancia 10 tiene diez veces el peso de una tarea con importancia 1 dentro del cálculo del progreso.

### Fechas

Las fechas de las tareas deben respetar los límites establecidos por el proyecto:

* La fecha de inicio de la tarea no puede ser anterior al inicio del proyecto.
* La fecha de término de la tarea no puede superar el término del proyecto.
* La fecha de inicio no puede ser posterior a la fecha de término.

---

## 10. Estados y progreso

Los estados de las tareas son:

* Pendiente.
* En progreso.
* Completada.

El progreso del proyecto se calcula de manera ponderada utilizando la importancia de las tareas.

La equivalencia utilizada es:

* Pendiente → 0%.
* En progreso → 50%.
* Completada → 100%.

La importancia actúa como peso relativo.

La prioridad del proyecto y la urgencia de una tarea no modifican este cálculo.

El progreso se muestra con dos decimales en la interfaz.

---

## 11. Urgencia de las tareas

La urgencia es independiente de:

* La prioridad del proyecto.
* La importancia de la tarea.
* El cálculo del progreso.

La regla definida para el indicador visual es:

* Más de 4 días restantes → verde.
* Entre 1 y 4 días restantes → amarillo.
* Tarea completada → indicador de completada.

---

## 12. Eliminación lógica

Los proyectos y tareas utilizan eliminación lógica.

En lugar de eliminar físicamente el registro de la base de datos, se modifica su estado de eliminación.

Los elementos eliminados no deben aparecer como elementos activos dentro de la aplicación.

Los participantes también pueden ser retirados mediante desactivación lógica de su participación.

Esta estrategia permite conservar los registros y facilita futuras necesidades de trazabilidad.

---

## 13. Dashboard

El dashboard constituye la página principal para los usuarios autenticados.

Los proyectos se organizan en tres categorías:

* Encargado principal.
* Ayudante.
* Colaborador.

Cada categoría posee su propio visor.

Las tarjetas muestran:

* Nombre del proyecto.
* Descripción resumida.
* Fecha de inicio.
* Fecha de término.
* Progreso.
* Rol.
* Prioridad mediante estrellas.

Las descripciones extensas se limitan visualmente en las tarjetas. La información completa se consulta ingresando al detalle del proyecto.

El diseño contempla un carrusel JavaScript con grupos de hasta cinco proyectos.

---

## 14. Participantes

Los participantes se administran mediante la entidad `Participacion`.

Una participación relaciona:

* Usuario.
* Proyecto.
* Rol.
* Estado activo.

Un usuario no puede tener más de una participación activa en el mismo proyecto.

El encargado principal es creado automáticamente al crear el proyecto.

El sistema contempla flujos específicos para:

* Agregar participantes.
* Cambiar roles.
* Retirar participantes.
* Salir del proyecto.
* Transferir el rol de encargado principal.

---

## 15. Django Admin

Los modelos principales se encuentran registrados en Django Admin.

El panel fue personalizado mediante clases `ModelAdmin`.

La personalización contempla:

* Columnas visibles.
* Filtros.
* Búsqueda.

Los modelos administrados son:

* Proyecto.
* Tarea.
* Participación.

---

## 16. Seguridad

La aplicación utiliza mecanismos de seguridad proporcionados por Django, entre ellos:

* Sistema de autenticación.
* Protección CSRF.
* Restricción de vistas mediante autenticación.
* Validación de formularios.
* Validación adicional en la capa de servicios.
* Control de permisos según rol.

Las reglas importantes de negocio no dependen únicamente de los elementos visuales de la interfaz.

---

## 17. Interfaz

La interfaz utiliza un diseño oscuro de inspiración tecnológica y Cyberpunk, manteniendo una aplicación visualmente simple y organizada.

Características principales:

* Fondo oscuro.
* Superficies oscuras.
* Texto claro.
* Colores neón utilizados de forma controlada.
* Glow sutil.
* Bordes ligeramente redondeados.
* Microanimaciones.
* Tipografía Inter.
* Iconos Lucide.
* Bootstrap.

La interfaz contempla comportamiento responsivo para escritorio, tableta y móvil.

---

## 18. Formularios

Los formularios mantienen una estructura visual común.

Se utilizan formularios de Django y `ModelForm` cuando corresponde.

Las validaciones permanecen activas aunque algunos textos de ayuda técnica se oculten visualmente para mantener una interfaz limpia.

Los formularios incluyen protección CSRF en las operaciones POST.

---

## 19. FAQ

La aplicación incluye una sección de preguntas frecuentes accesible desde la navegación interna.

La FAQ explica aspectos como:

* Funcionamiento de proyectos.
* Roles.
* Tareas.
* Progreso.
* Prioridad.
* Urgencia.
* Eliminación lógica.
* Permisos.
* Enfoque FBV.

---

## 20. Decisión académica sobre FBV

Este proyecto utiliza **Function-Based Views (FBV)**.

Esta decisión responde al orden de aprendizaje definido para el curso.

Este proyecto corresponde a la práctica de FBV.

El siguiente proyecto será desarrollado utilizando CBV para practicar ambos enfoques en proyectos diferentes.

La elección de FBV no se basa en considerar que CBV sea técnicamente más complejo ni en que FBV sea simplemente más sencillo.

---

## 21. Alcance

ProyectoModulo6 tiene un alcance académico y local.

El objetivo es demostrar la aplicación práctica de los conceptos estudiados durante el curso mediante una aplicación funcional de gestión de proyectos.

No forman parte del alcance actual:

* Despliegue de producción.
* Configuración de infraestructura de producción.
* Integración con servicios externos.
* Arquitecturas distribuidas.
* Funcionalidades empresariales avanzadas.

---

## 22. Extensiones futuras

Como posibles extensiones se consideran:

* Cronograma/Gantt.
* Exportación a Excel.
* Sistema de notificaciones.
* Buscador.
* Gestión avanzada de equipos.
* Modo claro.
* Otras funcionalidades que puedan incorporarse posteriormente.

Estas extensiones no forman parte del alcance actual.

---

## 23. Estado del proyecto

El proyecto se encuentra en etapa de consolidación final.

Las funcionalidades principales se encuentran implementadas y se están completando algunos comportamientos pendientes antes de ejecutar la batería definitiva de pruebas.

Pendientes principales:

* Preparación de una base de datos limpia para la entrega.
* Pruebas automatizadas.

---

## 24. Documentación

El proyecto incluye:

* `README.md`: documentación general e instalación.
* `BITACORA.md`: registro de decisiones y evolución del desarrollo.
* `FAQ`: preguntas frecuentes y explicación de decisiones relevantes.

La documentación se mantiene alineada con el alcance académico del proyecto.
