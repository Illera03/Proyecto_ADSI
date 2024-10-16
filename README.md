# https://www.omdbapi.com/?apikey=2d79f0e&

# Proyecto ADSI

Este proyecto es una aplicación de escritorio para la gestión de un videoclub. A continuación se detalla la estructura del proyecto y la función de cada uno de sus componentes.

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
