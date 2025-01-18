### IMPORTANTE ###
# NECESARIO INSTALAR pytest: pip install pytest
# Para ejecutar las pruebas: pytest src/test_reseñas.py
# Por tanto debe estar en la carpeta src para que funcione correctamente.

from CONTROLADOR.general_management import GeneralManager
from CONTROLADOR.db_manager import DbManager
from CONTROLADOR.review_management import ReviewManager

import json

# El usuario selecciona en "Crear Reseña"
    # se muestran las peliculas alquiladas por el usuario que aun no tienen reseña
    # cuando clica en "Crear Reseña" se le mostrara un formulario y reseñas de otros usuarios en caso de que los hubiera


#  El usuario seleccione en "Modificar Reseña"
    # se muestran las peliculas alquiladas por el usuario que ya tienen reseña


# El usuario selecciona "Guardar Reseña"
    # El campo de calificacion tiene un dato erroneo
    # El campo de comentario esta vacio
    # Ambos campos son correctos
