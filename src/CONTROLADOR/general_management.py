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
            
    ###---------------- Métodos para la funcionalidad de GESTIÓN DE USUARIOS ----------------###
    ###         -------USUARIOS-------         ###
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
    def authenticate_user(self, username, password):
        user_manager = UserManager()
        return user_manager.authenticate_user(username, password)  
    
    def get_user_info(self):
        user_manager = UserManager()
        return user_manager.get_user_info()
    
    def get_all_users(self):
        user_manager = UserManager()
        return user_manager.get_all_users()
    ###         -------ADMIN-------         ###
    def delete_user(self, username):
        user_manager = UserManager()
        if user_manager.delete_user(username):
            print("Usuario eliminado correctamente.")
            db_manager_instance = DbManager()
            if db_manager_instance.delete_user(username):
                print("Usuario eliminado de la base de datos.")
                return True
            else:
                print("Error al eliminar usuario de la base de datos.")
                return False

    
    ###-------------------------------------------------------------------------------------###
    def rent_movie(self, user_id, movie_id):
            """Alquilar una película"""
            return AlquilerManager.rent_movie(user_id, movie_id,fecha_alquiler=datetime.date.today())
    def view_rented_movies(self):
        return AlquilerManager.view_rented_movies()