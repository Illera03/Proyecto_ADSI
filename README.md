https://www.omdbapi.com/?apikey=2d79f0e&

# Proyecto ADSI

Este proyecto es una aplicación de escritorio para la gestión de un videoclub. A continuación se detalla la estructura del proyecto y la función de cada uno de sus componentes.

Tecnologías utilizadas: Python + Tkinter y SQLite

## Estructura del Proyecto

## Descripción de Componentes

- **/src/**: Carpeta que contiene todos los archivos fuente de la aplicación.

  - **main.py**: El punto de entrada de la aplicación. Aquí se inicializa y ejecuta la interfaz gráfica.
  - **db_manager.py**: Módulo encargado de establecer la conexión con la base de datos SQLite y gestionar las operaciones de creación y actualización de tablas.
  - **user_management.py**: Módulo que gestiona el registro de nuevos usuarios y su autenticación.
  - **movie_management.py**: Módulo responsable de la gestión del catálogo de películas, así como del alquiler de las mismas.
  - **review_management.py**: Módulo que permite a los usuarios dejar reseñas sobre las películas.
  - **request_management.py**: Módulo que permite a los usuarios solicitar películas que no están disponibles en el catálogo.
  - **admin_management.py**: Módulo que contiene funcionalidades exclusivas para administradores, como la gestión de usuarios y solicitudes.
  - **ui_components.py**: Módulo que contiene todos los elementos de la interfaz gráfica.

- **/data/**: Carpeta que almacena los archivos de la base de datos.
  - **video_club.db**: Archivo de base de datos SQLite donde se almacenan los datos de usuarios, películas y reseñas.
  
## Asignación de funcionalidades

-  Gestión de usarios: Jorge Illera
-  Alquiler de películas: Iker Argulo
-  Puntuación de películas: Eider Valenzuela
-  Incorporación de nuevas películas: Ander Javier Corral

# Funcionalidades
## Gestión de Usuarios:
La funcionalidad de gestión de usuarios permitirá a los usuarios registrarse, iniciar sesión, y actualizar sus datos personales. Por otro lado, los administradores podrán aceptar las solicitudes de registro, eliminar cuentas de usuario y modificar los datos personales de cualquier cuenta.

## Alquiler de Películas:
Esta funcionalidad incluirá la gestión del catálogo virtual de películas, y el seguimiento del historial de alquileres. Los usuarios podrán buscar y alquilar películas directamente en la plataforma virtual. Una vez alquiladas, las películas estarán disponibles para ser vistas en la plataforma durante un período de 48 horas.

## Puntuación de Películas:
Los usuarios tendrán la opción de puntuar y reseñar las películas que han alquilado. Esta funcionalidad permitirá ver las puntuaciones promedio de las películas, ordenar el catálogo por valoración y visualizar los comentarios de otros usuarios. Además, los usuarios podrán modificar sus puntuaciones y comentarios en cualquier momento.

## Incorporación de Nuevas Películas:
Esta funcionalidad permitirá a los usuarios solicitar la incorporación de nuevas películas al catálogo del Video Club a través de un catálogo más amplio disponible mediante una API externa. Los usuarios podrán explorar este catálogo ampliado y hacer peticiones de las películas que les interesen. Los administradores tendrán la capacidad de validar o rechazar dichas peticiones. En caso de validación, los administradores podrán añadir las películas solicitadas al catálogo.


## NOTAS:
### Administradores:
Para registrar a un administrador, se debe introducir el nombre de usuario "\_admin\_", el email y la contraseña son indiferentes.

Existe un administrador ya creado: 

__username__: \_admin\_

__password__: test


## CAMBIOS POR HACER:
LAS TABLAS: PETICIONES Y PELÍCULAS NO TIENEN LOS MISMOS CAMPOS QUE EN EL MODELO DE DOMINIO (HAY QUE CAMBIARLO)
