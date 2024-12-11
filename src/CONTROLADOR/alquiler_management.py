import tkinter as tk
import sqlite3
from MODELO.alquiler import Alquiler
import datetime
from CONTROLADOR.db_manager import DbManager
class AlquilerManager:
    
    def __init__(self, dbPath):
        self. alquileres = []

    def rent_movie(self, user_id, movie_id,date):
        """Alquilar una película"""
        alq =  Alquiler.nuevo_alquiler(user_id, movie_id, date)
        self.alquileres.append(alq)
        db_manager_instance = DbManager()
        if db_manager_instance.insert_alquiler(user_id, movie_id, date): 
            print("Alquiler insertado en la base de datos.") 
        else:
            print("Error al insertar alquiler en la base de datos.")
        return alq
    
    def view_rented_movies(self):
        return self.alquileres
    
    
    