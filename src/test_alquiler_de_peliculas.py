
### IMPORTANTE ###
# NECESARIO INSTALAR pytest: pip install pytest
# Para ejecutar las pruebas: pytest src/test_gestion_de_usuarios.py
# Por tanto debe estar en la carpeta src para que funcione correctamente.


from CONTROLADOR.general_management import GeneralManager
from CONTROLADOR.db_manager import DbManager
from CONTROLADOR.alquiler_management import AlquilerManager
from MODELO.alquiler import Alquiler
from datetime import datetime, timedelta, date


# Usuario alquila una pelicula concreta que no tenía alquilada

def test_rent_movie(): #FUNCIONA
    # Arrange
    username = "test_user"
    movie = "test_movie1"
    
    
    general_manager = GeneralManager()
    
    # Act
    result = general_manager.rent_movie(username, movie)
    
    # Assert
    assert result == True
    
    if result:
        # Comprobar que el alquiler se ha registrado en la base de datos
        user = DbManager.exists_rental(username, movie)
        assert user == True
        
        # Comprobar que el usuario se ha registrado en el user_manager
        exist = AlquilerManager.existeAlquiler(username, movie)
        assert exist == True
    # Cleanup: borrar el alquiler
    DbManager.delete_rental(username, movie)
    AlquilerManager.borrarAlquiler(username, movie)


# Usuario alquila una pelicula que ya tenía alquilada

def test_rent_same_movie():  # FUNCIONA
    # Arrange
    username = "test_user"
    movie = "test_movie2"
    
    general_manager = GeneralManager()
    
    # Act & Assert
    # Primer intento de alquiler
    result_first = general_manager.rent_movie(username, movie)
    assert result_first == True  # El primer alquiler debería ser exitoso
    
    if result_first:
        # Comprobar que el alquiler se ha registrado en la base de datos
        user = DbManager.exists_rental(username, movie)
        assert user == True
        
        # Comprobar que el alquiler se ha registrado en el AlquilerManager
        exist = AlquilerManager.existeAlquiler(username, movie)
        assert exist == True
    
    # Segundo intento de alquiler con la misma película
    result_second = general_manager.rent_movie(username, movie)
    assert result_second == False  # El segundo alquiler debería fallar
    
    # Cleanup: borrar el alquiler
    DbManager.delete_rental(username, movie)
    AlquilerManager.borrarAlquiler(username, movie)

# Usuario ve una pelicula que ya tenía alquilada y no ha caducado

def test_view_movie(): #FUNCIONA
    # Arrange
    username = "test_user"
    movie = "test_movie1"
    
    
    general_manager = GeneralManager()
    
    # Act
    general_manager.rent_movie(username, movie)
    result = general_manager.view_movie(username, movie)
    
    # Assert
    assert result == True
    
     # Cleanup: borrar el alquiler
    DbManager.delete_rental(username, movie)
    AlquilerManager.borrarAlquiler(username, movie)

# Usuario ve una pelicula que ya tenía alquilada y no ha caducado dos veces.

def test_view_same_movie_twice():  # FUNCIONA
    # Arrange
    username = "test_user"
    movie = "test_movie1"
    
    general_manager = GeneralManager()
    
    # Act
    # Alquilar la película primero
    general_manager.rent_movie(username, movie)
    
    # Primer intento de ver la película
    result_first = general_manager.view_movie(username, movie)
    assert result_first == True  # Debería permitir ver la película
    
    # Segundo intento de ver la misma película
    result_second = general_manager.view_movie(username, movie)
    assert result_second == True  # También debería permitir ver la película nuevamente
    
    # Cleanup: borrar el alquiler
    DbManager.delete_rental(username, movie)
    AlquilerManager.borrarAlquiler(username, movie)

# Usuario ve una pelicula que ya tenía alquilada y ha caducado.

def test_view_expired_movie():
    # Arrange
    username = "test_user"
    movie = "test_movie1"
    rental_date = datetime(2024, 12, 12, 12, 0, 0)  # Fecha fija para el alquiler

    # Crear instancia de GeneralManager y añadir un alquiler
    general_manager = GeneralManager()
    nuevo_alquiler = Alquiler.nuevo_alquiler(username, movie, rental_date)
    general_manager.alquiler_manager.alquileres.append(nuevo_alquiler)

    # Act
    result = general_manager.view_movie(username, movie)

    # Assert
    assert result == False  # Debería devolver False ya que el alquiler está caducado

    # Cleanup: borrar el alquiler
    DbManager.delete_rental(username, movie)
    AlquilerManager.borrarAlquiler(username, movie)


