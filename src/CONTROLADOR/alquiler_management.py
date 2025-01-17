import tkinter as tk
import sqlite3
from tkinter import messagebox
from datetime import datetime, timedelta, date
from MODELO.alquiler import Alquiler

class AlquilerManager:
    _instance = None  # Atributo de clase para la instancia única

    def __new__(cls, db_file=None):
        """Método para garantizar que solo haya una instancia de AlquilerManager"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.alquileres = []  # Lista de alquileres
        return cls._instance

    def add_rent(self, user_id, movie, date):
        """Añadir un nuevo alquiler a la lista de alquileres."""
        new_rent = Alquiler.nuevo_alquiler(user_id, movie, date)  # Asumimos que 'nuevo_alquiler' es un método estático
        self.alquileres.append(new_rent)  # Agregamos el alquiler a la lista
        return True

    def add_alquiler_from_bd(self, user_id, movie_id, date):
        """Añadir un nuevo alquiler a la lista de alquileres desde la base de datos."""
        for a in self.alquileres:
            if a.user_id == user_id and a.movie_id == movie_id and a.rental_date == date:
                print("Ya hay un alquiler con esos datos")
                return False
        # Crear un nuevo alquiler e agregarlo a la lista
        new_alquiler = Alquiler(user_id=user_id, movie_id=movie_id, rental_date=date)
        self.alquileres.append(new_alquiler)
        return True

    def view_movie(self, user_id, tituloPeli):
        # Obtener la fecha y hora actual sin microsegundos
        now = datetime.now().replace(microsecond=0)
        for a in self.alquileres:
            if a.esUserYMovie(user_id, tituloPeli):

                # Verificar si a.rental_date es una cadena y convertirla a datetime
                if isinstance(a.rental_date, str):
                    # Ajusta el formato según cómo esté representada la fecha en el string
                    a.rental_date = datetime.strptime(a.rental_date, "%Y-%m-%d %H:%M:%S")
                
                # Si es un date, conviértelo a datetime
                elif isinstance(a.rental_date, date) and not isinstance(a.rental_date, datetime):
                    a.rental_date = datetime.combine(a.rental_date, datetime.min.time())
                
                diferencia = now - a.rental_date
                print(f"Diferencia: {diferencia}, Tiempo límite: {timedelta(hours=48)}")
                
                # Comprobar si han pasado más de 48 horas desde la fecha de alquiler
                if diferencia > timedelta(hours=48):
                    return False
        return True
    
    def existeAlquiler(self, user_id, movie_id):
        for a in self.alquileres:
            if a.esUserYMovie(user_id, movie_id):
                return True
        return False
    
    def borrarAlquiler(self, user_id, movie_id):
        for a in self.alquileres:
            if a.esUserYMovie(user_id, movie_id):
                self.alquileres.remove(a)
                return True  # Indica que se borró con éxito
        return False  # Indica que no se encontró el alquiler
    
    def get_rented_movies(self, user_id):
        """Obtiene todas las películas alquiladas por un usuario específico"""
        rented_movies = []
        for alquiler in self.alquileres:
            if alquiler.user_id == user_id:
                rented_movies.append(alquiler)  # Añadimos el alquiler a la lista
        return rented_movies