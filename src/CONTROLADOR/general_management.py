# Description: General management class.
from CONTROLADOR.user_management import UserManager
from CONTROLADOR.db_manager import DbManager
from CONTROLADOR.alquiler_management import AlquilerManager
import datetime

class GeneralManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if not self.__initialized:
            self.__initialized = True

    def register_user(self, username, password, email):
        user_manager = UserManager()
        bien = user_manager.add_user(username, password, email)
        if bien:
            print("Usuario añadido correctamente.")
            # Usar la misma instancia de DbManager
            db_manager_instance = DbManager()
            if db_manager_instance.insert_user(username, password, email):
                print("Usuario insertado en la base de datos.")
                return True
            else:
                print("Error al insertar usuario en la base de datos.")
                return False
        else:
            print("Error al agregar usuario.")
            return False

    def rent_movie(self, user_id, movie_id):
            """Alquilar una película"""
            return AlquilerManager.rent_movie(user_id, movie_id,fecha_alquiler=datetime.date.today())
    def view_rented_movies(self):
        return AlquilerManager.view_rented_movies()