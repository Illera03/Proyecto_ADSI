import tkinter as tk
from MODELO.alquiler import Alquiler
import MODELO.movie as movie
import json

class MovieManager:
    _instance = None  # Atributo de clase para almacenar la única instancia

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            # Inicializamos la lista de películas solo una vez
            cls._instance.movieList = []
            cls._instance.initialize_movies()
        return cls._instance

    def initialize_movies(self):
        """Inicializar la lista de películas"""
        self.movieList.append(movie.Movie.new_movie(1, "Titanic", "Drama", 1997, "James Cameron", 4.5))
        self.movieList.append(movie.Movie.new_movie(2, "The Godfather", "Crime", 1972, "Francis Ford Coppola", 4.9))
        self.movieList.append(movie.Movie.new_movie(3, "The Dark Knight", "Action", 2008, "Christopher Nolan", 4.8))
        self.movieList.append(movie.Movie.new_movie(4, "Pulp Fiction", "Crime", 1994, "Quentin Tarantino", 4.7))
        self.movieList.append(movie.Movie.new_movie(5, "Schindler's List", "Biography", 1993, "Steven Spielberg", 4.9))
        self.movieList.append(movie.Movie.new_movie(6, "The Lord of the Rings: The Return of the King", "Adventure", 2003, "Peter Jackson", 4.9))
        self.movieList.append(movie.Movie.new_movie(7, "Fight Club", "Drama", 1999, "David Fincher", 4.8))
        self.movieList.append(movie.Movie.new_movie(8, "Forrest Gump", "Drama", 1994, "Robert Zemeckis", 4.8))
        self.movieList.append(movie.Movie.new_movie(9, "Inception", "Sci-Fi", 2010, "Christopher Nolan", 4.7))
        self.movieList.append(movie.Movie.new_movie(10, "The Matrix", "Sci-Fi", 1999, "Lana Wachowski, Lilly Wachowski", 4.7))
        self.movieList.append(movie.Movie.new_movie(11, "Goodfellas", "Biography", 1990, "Martin Scorsese", 4.7))
        self.movieList.append(movie.Movie.new_movie(12, "The Empire Strikes Back", "Action", 1980, "Irvin Kershner", 4.8))
        self.movieList.append(movie.Movie.new_movie(13, "One Flew Over the Cuckoo's Nest", "Drama", 1975, "Milos Forman", 4.8))
        self.movieList.append(movie.Movie.new_movie(14, "Interstellar", "Adventure", 2014, "Christopher Nolan", 4.6))
        self.movieList.append(movie.Movie.new_movie(15, "City of God", "Crime", 2002, "Fernando Meirelles, Kátia Lund", 4.6))
        self.movieList.append(movie.Movie.new_movie(16, "Se7en", "Crime", 1995, "David Fincher", 4.6))
        self.movieList.append(movie.Movie.new_movie(17, "The Silence of the Lambs", "Crime", 1991, "Jonathan Demme", 4.6))
        self.movieList.append(movie.Movie.new_movie(18, "It's a Wonderful Life", "Drama", 1946, "Frank Capra", 4.6))
        self.movieList.append(movie.Movie.new_movie(19, "Life Is Beautiful", "Comedy", 1997, "Roberto Benigni", 4.6))
        self.movieList.append(movie.Movie.new_movie(20, "The Usual Suspects", "Crime", 1995, "Bryan Singer", 4.6))
        self.movieList.append(movie.Movie.new_movie(21, "Léon: The Professional", "Crime", 1994, "Luc Besson", 4.6))
        self.movieList.append(movie.Movie.new_movie(22, "Saving Private Ryan", "Drama", 1998, "Steven Spielberg", 4.6))
        self.movieList.append(movie.Movie.new_movie(23, "Spirited Away", "Animation", 2001, "Hayao Miyazaki", 4.6))
        self.movieList.append(movie.Movie.new_movie(24, "The Green Mile", "Crime", 1999, "Frank Darabont", 4.6))
        self.movieList.append(movie.Movie.new_movie(25, "Parasite", "Comedy", 2019, "Bong Joon Ho", 4.6))

    def get_all_movies(self):
        """Obtener todas las películas"""
        return self.movieList

    def get_user_rentals(self, user_id):
        """Obtener todas las películas que el usuario ha alquilado"""
        return 0
