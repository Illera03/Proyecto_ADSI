import sqlite3
from tkinter import messagebox
#from CONTROLADOR.db_manager import create_connection
from MODELO.request import Request

class RequestManager:
    requestList = []
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Inicializamos la lista de peticiones solo una vez
            cls._instance.requestList = []
        return cls._instance
    
    def get_all_requests(self):
        """Obtener todas las peticiones"""
        return self.requestList
    
    def add_request(self, movieId, userId, status):
        """Añadir una nueva peticion a la lista de peticiones."""
        for r in self.requestList:
            self.requestList.append(Request.new_request(movieId, userId, status))

    def print_requests(self):
        """Imprimir la lista de peticiones."""
        print("\nLista de peticiones:\n")
        print("---------------------------------------------------------------------------------------------------------------------------------")
        for request in self.requestList:
            print(f"Pelicula: {request.movie.get_title()}, Usuario: {request.user.get_username()}, Estado: {request.status}")
            print("---------------------------------------------------------------------------------------------------------------------------------")

    def search_movie_omdb(self, movie_title):
        """Buscar la película en la API de OMDb"""
        url = f"http://www.omdbapi.com/?t={movie_title}&apikey=2d79f0e"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data['Response'] == 'True':
                return data  # Devolvemos los datos de la película
            else:
                return None  # No se encontró la película
        else:
            messagebox.showerror("Error", "No se pudo conectar con OMDb API.")
            return None