""
Nombre: Proyecto Convivencia Escolar.

Descripción:

El Proyecto Convivencia Escolar es una aplicación web diseñada para apoyar la gestión de la convivencia dentro de un establecimiento educacional. Su objetivo es facilitar la administración de información relacionada con estudiantes, profesores, cursos y situaciones vinculadas con la convivencia escolar.

## Tecnologías utilizadas

- **Python:** lenguaje utilizado para desarrollar la lógica y el funcionamiento del servidor.
- **Flask:** framework de Python utilizado para crear la aplicación web, definir las rutas y gestionar las solicitudes HTTP.
- **HTML5:** utilizado para construir las páginas de la aplicación.
- **CSS3:** utilizado para definir los estilos visuales mediante `static/css/style.css`.
- **Jinja2:** motor de plantillas utilizado por Flask para mostrar información dinámica en los archivos HTML.
- **Sesiones de Flask:** utilizadas para mantener la sesión del usuario después de verificar su código de acceso.
- **Entorno virtual de Python (`venv`):** utilizado para aislar las dependencias del proyecto.
- **Visual Studio Code:** editor de código utilizado para el desarrollo.

## Base de datos y almacenamiento de información

Actualmente, el proyecto no utiliza una base de datos persistente. La información se almacena temporalmente en estructuras de datos de Python:

- `PROFESORES`: diccionario que contiene la información de los profesores.
- `CURSOS`: diccionario que organiza los estudiantes según su curso.
- `CODIGOS_ACCESO`: diccionario que almacena temporalmente los códigos de verificación.

Los datos se generan y almacenan en memoria mientras se ejecuta la aplicación. Por este motivo, los cambios realizados y los registros creados se pierden al reiniciar el servidor.

La aplicación podría ampliarse en el futuro mediante una base de datos como MySQL o SQLite para conservar la información de manera permanente.

Método HTTP	Ruta	Funcionalidad
GET, POST	/	Muestra el inicio de sesión y recibe el correo del usuario para generar un código de acceso.
POST	/verificar	Comprueba el código de acceso ingresado y crea la sesión del usuario si es correcto.
GET	/panel	Muestra el panel principal con los cursos de básica y media.
GET	/curso/<nombre_curso>	Muestra los estudiantes y el profesor asociado a un curso.
GET	/curso/<nombre_curso>/estudiante/<estudiante_id>	Muestra la información detallada de un estudiante.
GET, POST	/profesores	Lista los profesores y permite registrar nuevos profesores.
GET	/profesor/<profesor_id>	Muestra los detalles de un profesor.
POST	/registrar_falta	Registra atrasos, situaciones de convivencia, atenciones de enfermería o suspensiones.
GET	/reportes	Muestra estadísticas generales, como el total de cursos y estudiantes.
GET	/configuracion	Muestra la página de configuración.
GET	/logout	Cierra la sesión del usuario.

proyecto-convivencia-escolar/
├── node_modules/
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── base.html
│   ├── configuracion.html
│   ├── curso.html
│   ├── estudiante.html
│   ├── index.html
│   ├── login.html
│   ├── profesor_detalle.html
│   ├── profesores.html
│   ├── reportes.html
│   └── verificar.html
├── venv/
├── app.py
└── README.md


node_modules/: contiene dependencias de Node.js instaladas para el proyecto, si se utilizan.

static/: almacena archivos estáticos, como hojas de estilo, imágenes y scripts.

static/css/style.css: contiene los estilos visuales de la aplicación.

templates/: contiene las plantillas HTML que se muestran al usuario.

base.html: plantilla base que puede compartirse entre las distintas páginas.

venv/: contiene el entorno virtual de Python y sus dependencias instaladas.

app.py: archivo principal que contiene la lógica del servidor y, posiblemente, las rutas de la aplicación.

README.md: archivo que contiene la documentación del proyecto.

Integrante 1: [Antonia Torres].

Integrante 2: [Josefa Rojas].

Integrante 3: [Noelia Jeria].

Integrante 4: [Felix Blanco].

Integrante 5: [Adonys Gomez].


""