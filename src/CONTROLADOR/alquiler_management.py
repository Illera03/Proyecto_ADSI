import tkinter as tk
import sqlite3
from db_manager import create_connection 
from MODELO.alquiler import Alquiler
import datetime

class AlquilerManager:
    
    def __init__(self, dbPath):
        self. alquileres = []

    def rent_movie(self, user_id, movie_id):
        """Alquilar una película"""
        alq=  Alquiler(user_id, movie_id, fecha_alquiler=datetime.date.today())
        return alq
    
    