import json

import tkinter as tk
from tkinter import messagebox
from MODELO.review import Review
from CONTROLADOR.movie_management import MovieManager

class ReviewManager:
    review_list = []
    _instance = None  # Variable de clase para guardar la instancia única

    def __new__(cls, db_file=None):
        """Método para garantizar que solo haya una instancia de ReviewManager"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.review_list = []  # Lista de reseñas
        return cls._instance

    def add_review_from_bd(self, user_id, movie_id, rating, comment):
        """Añadir una nueva reseña a la lista de usuarios."""
        self.review_list.append(Review.new_review_from_bd(user_id=user_id, movie_id=movie_id, rating=rating, comment=comment))

    def add_review(self, user_id, movie_id, rating, comment):
        """Añadir una nueva reseña a la lista de reseñas."""
        new_review = Review.new_review(user_id, movie_id, rating, comment) 
        self.review_list.append(new_review)  # Agregamos el alquiler a la lista
        print("Reseña añadida:", new_review.get_review_info())  # Imprime la información de la reseña
        return True
    
    def update_review_info(self, user_id, movie_id, new_rating, new_comment):
        """Actualizar la información de la reseña actual"""
        # Buscar la reseña actual
        review = next((r for r in self.review_list if r.get_user_id() == user_id and r.get_movie_id() == movie_id), None)
        if not review:
            return "error"  # Reseña actual no encontrada
        # Actualizar la información del usuario
        review.update_review_info(new_rating, new_comment)
        return True
    
    def get_review(self, user_id, movie_id):
         """Obtiene la reseña de un usuario para una película específica."""
         for review in self.review_list:
            if review.get_user_id() == user_id and review.get_movie_id() == movie_id:
                return review  # Devuelve la reseña si existe
         return None  # Devuelve None si no hay reseña
    
    def update_movie_average(self, movie_id):
        """Actualizar el promedio de una película."""
        # Filtrar todas las reseñas de la película
        movie_reviews = [r for r in self.review_list if r.get_movie_id() == movie_id]
        if movie_reviews:
            # Obtenemos el objeto de la pelicula en cuestion
            movie_manager = MovieManager()
            movie = next((m for m in movie_manager.movieList if m.title == movie_id), None)
            if movie:
                 # Calcular el promedio de las reseñas
                total_rating = sum(r.get_movie_rating() for r in movie_reviews)
                average_rating = total_rating / len(movie_reviews)
                # Actualizar el promedio de la pelicula
                movie.nota_promedio = round(average_rating,2)
                print(f"Promedio actualizado para '{movie.title}': {movie.nota_promedio}")
            else:
                print(f"No se encontró la película con ID {movie_id}")
        else:
            print("No hay reseñas para esta película.")

    def get_others_reviews_for_movie(self, movie_id, user_id):
        """Recupera las reseñas de otros usuarios para una película """
        return [review for review in self.review_list if review.get_movie_id() == movie_id and review.get_user_id() != user_id]