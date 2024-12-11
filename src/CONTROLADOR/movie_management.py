import tkinter as tk
import sqlite3
<<<<<<< HEAD:src/CONTROLADOR/movie_management.py
<<<<<<< HEAD:src/CONTROLADOR/movie_management.py
from db_manager import create_connection 
import MODELO.movie as movie
=======
from CONTROLADOR.db_manager import create_connection 
=======
from CONTROLADOR.db_manager import DbManager
>>>>>>> c7f967029faf408622f4dd3ef7ef160c451daa65:src/movie_management.py

>>>>>>> d29e0235096c27310cdcfe62c5f95991e650a833:src/movie_management.py

class MovieManager:

    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = self.create_connection()  # Crear una conexión al inicializar
        self. __movie_manager = MovieManager()
        self. __movieList = []

    def create_connection(self):
        """Crea una conexión a la base de datos SQLite"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
        return conn

    def get_all_movies(self):
        """Obtener todas las películas de la base de datos"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT movie_id, title, genre, release_year, director, notaPromedio FROM Películas") # Consulta para obtener todas las películas
        movies = cursor.fetchall()

        movie_list = []
        for movie in movies:
            movie_list.append({'id': movie[0], 'title': movie[1], 'year': movie[2]})
        return movie_list
    
    def rent_movie(self, user_id, movie_id):
        """Alquilar una película"""
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Alquileres (user_id, movie_id) VALUES (?, ?)", (user_id, movie_id))
        self.connection.commit()

    def get_user_rentals(self, user_id):
        """Obtener todas las películas que el usuario ha alquilado"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT movie_id, title, genre, release_year, director, notaPromedio FROM Películas
            JOIN Alquileres ON Películas.movie_id = Alquileres.movie_id
            WHERE user_id = ?
        """, (user_id,)) # Consulta para obtener solo las películas alquiladas por el usuario
        rentals = cursor.fetchall()
        rental_list = []
        for rental in rentals:
            rental_list.append({'id': rental[0], 'title': rental[1], 'year': rental[2]})
        return rental_list