### IMPORTANTE ###
# NECESARIO INSTALAR pytest: pip install pytest
# Para ejecutar las pruebas: pytest src/test_reseñas.py
# Por tanto debe estar en la carpeta src para que funcione correctamente.

from CONTROLADOR.general_management import GeneralManager
from CONTROLADOR.db_manager import DbManager
from CONTROLADOR.review_management import ReviewManager


import json

def test_register_review_success(general_manager, sample_user, sample_movie):
    """Prueba la creación de una reseña válida."""
    username = "test_user"
    movie = "test_movie"
    rating = 9.0
    comment = "Excelente"
    general_manager = GeneralManager()
    db_manager = DbManager()
    review_manager = ReviewManager()
    # Realizar prueba
    result = general_manager.register_Review(username, movie, rating, comment)
    assert  result == True
    if result:
        # Comprobar que la reseña se ha registrado en la base de datos
        assert db_manager.get_review(username, movie) == True
        # Comprobar que la reseña se ha registrado en el review_manager
        assert review_manager.get_review(username, movie) == True
        # Borramos dicha reseña de la lista de objetos y de la base de datos
        db_manager.delete_review(username, movie)
        review_manager.delete_review(username, movie)

def test_register_review_invalid_rating(general_manager, sample_user, sample_movie):
    """Prueba el registro de una reseña con una calificación inválida."""
    username = "test_user"
    movie = "test_movie"
    rating = 13.4  # Calificación inválida, fuera del rango 1-10
    comment = "Comentario válido"
    general_manager = GeneralManager()
    # Realizar prueba
    result = general_manager.register_Review(username, movie, rating, comment)
    assert result == False  # Esperamos que la función devuelva False al ser una calificación inválida

def test_register_review_without_rating(general_manager, sample_user, sample_movie):
    """Prueba la creación de una reseña sin calificación."""
    username = "test_user"
    movie = "test_movie"
    rating = None  # Sin calificación
    comment = "Comentario válido"
    general_manager = GeneralManager()
    # Realizar prueba
    result = general_manager.register_Review(username, movie, rating, comment)
    assert result == False  # Esperamos que la función devuelva False al no haber calificación
    # Asegurarnos de que la reseña no se ha registrado en la base de datos ni en el review manager
    db_manager = DbManager()
    review_manager = ReviewManager()
    assert db_manager.get_review(username, movie) == False
    assert review_manager.get_review(username, movie) == False

def test_register_review_without_comment(general_manager, sample_user, sample_movie):
    """Prueba la creación de una reseña sin comentario."""
    username = "test_user"
    movie = "test_movie"
    rating = 7.0
    comment = None  # Sin comentario
    general_manager = GeneralManager()
    # Realizar prueba
    result = general_manager.register_Review(username, movie, rating, comment)
    assert result == False  
    # Comprobar que la reseña no se ha registrado en la base de datos y el review manager
    db_manager = DbManager()
    review_manager = ReviewManager()
    assert db_manager.get_review(username, movie) == False
    assert review_manager.get_review(username, movie) == False

def test_modify_review_success(general_manager, sample_user, sample_movie):
    """Prueba la modificacion de una reseña válida."""
    username = "test_user"
    movie = "test_movie"
    rating = 9.3
    comment = "Excelente"
    general_manager = GeneralManager()
    db_manager = DbManager()
    review_manager = ReviewManager()
    # Realizar prueba añadiendo primero el registro a modificar
    general_manager.register_Review(username, movie, rating, comment)
    result = general_manager.modify_Review(username, movie, 2.67, "Excelente modificacion")
    assert  result == True
    if result:
        # Comprobar que la reseña se ha registrado en la base de datos
        assert db_manager.get_review(username, movie) == True
        # Comprobar que la reseña se ha registrado en el review_manager
        assert review_manager.get_review(username, movie) == True
        # Borramos dicha reseña de la lista de objetos y de la base de datos
        db_manager.delete_review(username, movie)
        review_manager.delete_review(username, movie)

def test_modify_review_invalid_rating(general_manager, sample_user, sample_movie):
    """Prueba la modificación de una reseña con una calificación inválida."""
    username = "test_user"
    movie = "test_movie"
    rating = 13.4  # Calificación inválida, fuera del rango 1-10
    comment = "Comentario válido"
    general_manager = GeneralManager()
    # Primero registramos una reseña para poder modificarla
    general_manager.register_Review(username, movie, 8.0, "Comentario inicial")
    # Realizar prueba de modificación con calificación inválida
    result = general_manager.modify_Review(username, movie, rating, comment)
    assert result == False  # Esperamos que la función devuelva False al ser una calificación inválida
    # Comprobar que la reseña no ha sido modificada en la base de datos ni en el review manager
    db_manager = DbManager()
    review_manager = ReviewManager()
    assert db_manager.get_review(username, movie) == True  # La reseña original sigue presente
    assert review_manager.get_review(username, movie) == True  # La reseña original sigue presente
    # Borrar la reseña después de la prueba
    db_manager.delete_review(username, movie)
    review_manager.delete_review(username, movie)

def test_modify_review_without_rating(general_manager, sample_user, sample_movie):
    """Prueba la modificación de una reseña sin calificación."""
    username = "test_user"
    movie = "test_movie"
    rating = None  # Sin calificación
    comment = "Comentario válido"
    general_manager = GeneralManager()
    # Primero registramos una reseña para poder modificarla
    general_manager.register_Review(username, movie, 8.0, "Comentario inicial")
    # Realizar prueba de modificación sin calificación
    result = general_manager.modify_Review(username, movie, rating, comment)
    assert result == False  # Esperamos que la función devuelva False al no haber calificación
    # Comprobar que la reseña no ha sido modificada en la base de datos ni en el review manager
    db_manager = DbManager()
    review_manager = ReviewManager()
    assert db_manager.get_review(username, movie) == True  # La reseña original sigue presente
    assert review_manager.get_review(username, movie) == True  # La reseña original sigue presente
    # Borrar la reseña después de la prueba
    db_manager.delete_review(username, movie)
    review_manager.delete_review(username, movie)

def test_modify_review_without_comment(general_manager, sample_user, sample_movie):
    """Prueba la modificación de una reseña sin comentario (el botón no debe habilitarse)."""
    username = "test_user"
    movie = "test_movie"
    rating = 7.0
    comment = None  # Sin comentario
    general_manager = GeneralManager()
    # Primero registramos una reseña para poder modificarla
    general_manager.register_Review(username, movie, 8.0, "Comentario inicial")
    # Realizar prueba de modificación sin comentario
    result = general_manager.modify_Review(username, movie, rating, comment)
    assert result == False  # Esperamos que la función devuelva False al no habilitarse el botón de modificar reseña
    # Comprobar que la reseña no ha sido modificada en la base de datos ni en el review manager
    db_manager = DbManager()
    review_manager = ReviewManager()
    assert db_manager.get_review(username, movie) == True  # La reseña original sigue presente
    assert review_manager.get_review(username, movie) == True  # La reseña original sigue presente
    # Borrar la reseña después de la prueba
    db_manager.delete_review(username, movie)
    review_manager.delete_review(username, movie)