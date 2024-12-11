import tkinter as tk
import sqlite3
from CONTROLADOR.db_manager import DbManager


class ReviewManager:

    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = self.create_connection()  # Crear una conexión al inicializar

    def create_connection(self):
        """Crea una conexión a la base de datos SQLite"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
        return conn
    
    def get_review_for_movie(self, user_id, movie_id):
        """Obtener la reseña de un usuario para una película"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT rating, comment FROM Reseñas WHERE user_id = ? AND movie_id = ?", (user_id, movie_id))
        review = cursor.fetchone()
        return review  # Devuelve una tupla con la reseña (rating, comment) o None si no existe

    def add_review(self, user_id, movie_id, rating, comment):
        """Añadir una reseña para una película"""
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO Reseñas (user_id, movie_id, rating, comment) 
            VALUES (?, ?, ?, ?)
        """, (user_id, movie_id, rating, comment))

        cursor.execute("""
            UPDATE Películas SET notaPromedio = (
                SELECT AVG(rating)
                FROM Reseñas
                WHERE movie_id = ?
                )
                WHERE movie_id = ?
           ;
        """, (movie_id, movie_id))

        self.connection.commit()

    def modify_review(self, user_id, movie_id, rating, comment):
        """Modificar una reseña existente para una película"""
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE Reseñas SET  rating = ?, comment = ? 
            WHERE user_id = ? AND movie_id = ?
        """, ( rating, comment, user_id, movie_id))
        cursor.execute("""
            UPDATE Películas SET notaPromedio = (
                SELECT AVG(rating)
                FROM Reseñas
                WHERE movie_id = ?
                )
                WHERE movie_id = ?
           ;
        """, (movie_id, movie_id))
        self.connection.commit()

    def get_all_reviews_of_a_movie(self, movie_id, user_id):
        """ Obtener las reseñas de otros usuarios para una película específica """
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT user_id, rating, comment
            FROM Reseñas
            WHERE movie_id = ? AND user_id != ?
        """, (movie_id, user_id))
        return cursor.fetchall()