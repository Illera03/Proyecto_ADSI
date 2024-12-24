import tkinter as tk
import sqlite3
import json
import requests
from tkinter import messagebox
import datetime
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

    def view_rented_movies(self, user_id):
        """Devuelve la lista de alquileres de un usuario en concreto"""
        user_rentals = [alquiler for alquiler in self.alquileres if alquiler.user_id == user_id]
        return user_rentals

    def add_alquiler_from_bd(self, user_id, movie_id, date):
        """Añadir un nuevo alquiler a la lista de alquileres desde la base de datos."""
        for a in self.alquileres:
            if a.user_id == user_id and a.movie_id == movie_id and a.date == date:
                print("Ya hay un alquiler con esos datos")
                return False
        # Crear un nuevo alquiler e agregarlo a la lista
        new_alquiler = Alquiler(user_id=user_id, movie_id=movie_id, rental_date=date)
        self.alquileres.append(new_alquiler)
        return True

    