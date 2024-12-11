# Description: General management class.
<<<<<<< HEAD
import CONTROLADOR.user_management as UserManager
import CONTROLADOR.db_manager as db_manager
import CONTROLADOR.alquiler_management as alquilerman
=======
from CONTROLADOR.user_management import UserManager
from CONTROLADOR.db_manager import DbManager

>>>>>>> c7f967029faf408622f4dd3ef7ef160c451daa65
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
<<<<<<< HEAD
            db_manager.db_manager().insert_user(username, password, email) # Insertar usuario en la base de datos

    def rent_movie(self, user_id, movie_id):
        """Alquilar una película"""
        return alquilerman.rent_movie(user_id, movie_id)
=======
            print("Usuario añadido correctamente.")
            # Usar la misma instancia de DbManager
            db_manager_instance = DbManager()
            if db_manager_instance.insert_user(username, password, email):
                print("Usuario insertado en la base de datos.")
            else:
                print("Error al insertar usuario en la base de datos.")
        else:
            print("Error al agregar usuario.")


>>>>>>> c7f967029faf408622f4dd3ef7ef160c451daa65
    
        
    

