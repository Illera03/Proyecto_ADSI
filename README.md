# Proyecto ADSI

Este proyecto es una aplicación de escritorio para la gestión de un videoclub. A continuación se detalla la estructura del proyecto y la función de cada uno de sus componentes.

Tecnologías utilizadas: Python + Tkinter y SQLite

API utilizada: https://www.omdbapi.com/?apikey=2d79f0e&

## Estructura del Proyecto

## Descripción de Componentes

- **/src/**: Carpeta que contiene todos los archivos fuente de la aplicación.
  - **/MODELO/**:
    - **user.py**: Módulo para los usuarios.
    - **review.py**
    - **alquiler.py**
    - **movie.py**
    - **request.py**
  
  - **/VISTA/**:
    - **ui_components.py**: Módulo que contiene todos los elementos de la interfaz gráfica.
  
  - **/CONTROLADOR/**:
    - **db_manager.py**: Módulo encargado de establecer la conexión con la base de datos SQLite y gestionar las operaciones de creación y actualización de tablas.
    - **user_management.py**: Módulo que gestiona todo lo relacionado con usuarios.
    - **general_management.py**: Módulo encargado de la gestión general.
    - **alquiler_management.py**
    - **request_management.py**
    - **review_management.py**
    
  
  - **main.py**: El punto de entrada de la aplicación. Aquí se inicializa y ejecuta la interfaz gráfica.
  - **tests**

  
- **/data/**: Carpeta que almacena los archivos de la base de datos.
  - **video_club.db**: Archivo de base de datos SQLite donde se almacenan los datos de usuarios, películas y reseñas.
  
## Asignación de funcionalidades

-  Gestión de usarios: Jorge Illera Rivera
-  Alquiler de películas: Iker Argulo
-  Puntuación de películas: Eider Valenzuela
-  Incorporación de nuevas películas: Ander Javier Corral

# Funcionalidades
## Gestión de Usuarios (hecho):
La funcionalidad de gestión de usuarios permitirá a los usuarios registrarse, iniciar sesión, y actualizar sus datos personales. Por otro lado, los administradores podrán aceptar las solicitudes de registro, eliminar cuentas de usuario y modificar los datos personales de cualquier cuenta.

## Alquiler de Películas (hecho):
Esta funcionalidad incluirá la gestión del catálogo virtual de películas, y el seguimiento del historial de alquileres. Los usuarios podrán buscar y alquilar películas directamente en la plataforma virtual. Una vez alquiladas, las películas estarán disponibles para ser vistas en la plataforma durante un período de 48 horas.

## Puntuación de Películas (hecho):
Los usuarios tendrán la opción de puntuar y reseñar las películas que han alquilado. Esta funcionalidad permitirá ver las puntuaciones promedio de las películas, ordenar el catálogo por valoración y visualizar los comentarios de otros usuarios. Además, los usuarios podrán modificar sus puntuaciones y comentarios en cualquier momento.

## Incorporación de Nuevas Películas (sin hacer):
Esta funcionalidad permitirá a los usuarios solicitar la incorporación de nuevas películas al catálogo del Video Club a través de un catálogo más amplio disponible mediante una API externa. Los usuarios podrán explorar este catálogo ampliado y hacer peticiones de las películas que les interesen. Los administradores tendrán la capacidad de validar o rechazar dichas peticiones. En caso de validación, los administradores podrán añadir las películas solicitadas al catálogo.


## NOTAS:
### Administradores:

Existe un administrador ya creado, por tanto no dejará crear otro porque tendría el mismo nombre de usuario.

**Credenciales:**

- __username__: \_admin\_

- __password__: test

En el caso de no existir, para registrar a un administrador, se debe introducir el nombre de usuario "\_admin\_", el email y la contraseña son indiferentes.

