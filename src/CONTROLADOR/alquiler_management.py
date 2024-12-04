import tkinter as tk
import sqlite3
from db_manager import create_connection 
from MODELO.alquiler import Alquiler
import MODELO.alquiler as alquiler

class AlquilerManager:
    
    def __init__(self, dbPath):
        self. alquileres = []
    