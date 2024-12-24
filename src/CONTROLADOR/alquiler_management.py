import tkinter as tk
import sqlite3

import datetime

class AlquilerManager:
    
    def __init__(self, dbPath):
        self. alquileres = []

    def rent_movie(self, user_id, movie_id,date):
        """Alquilar una película"""
        from MODELO.alquiler import Alquiler
        alq =  Alquiler.nuevo_alquiler(user_id, movie_id, date)
        self.alquileres.append(alq)
        from CONTROLADOR.db_manager import DbManager
        db_manager_instance = DbManager()
        if db_manager_instance.insert_alquiler(user_id, movie_id, date): 
            print("Alquiler insertado en la base de datos.") 
        else:
            print("Error al insertar alquiler en la base de datos.")
        return alq
    
    def view_rented_movies(self):
        return self.alquileres
    def add_alquiler_from_bd(self, user_id, movie_id, date):
        from MODELO.alquiler import Alquiler
        """Añadir un nuevo alquiler a la lista de alquileres desde la base de datos."""
        for a in self.alquileres:
            if a.user_id == user_id and a.movie_id == movie_id and a.date == date:
                print("Ya hay un alquiler con esos datos")
                return False
        new_alquiler = Alquiler(user_id=user_id, movie_id=movie_id, date=date)
        self.alquileres.append(new_alquiler)
        return True
    
    