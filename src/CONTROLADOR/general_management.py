# Description: General management class.
import CONTROLADOR.user_management as UserManager
import CONTROLADOR.db_manager as db_manager
import CONTROLADOR.alquiler_management as alquilerman
class GeneralManager:
    def __init__(self):
        self.__general_manager = GeneralManager()
        
    @property
    def general_manager(self):
        return self.__general_manager
    
    def register_user(self, username, password, email):
        bien = UserManager.user_manager().add_user(username, password, email) # Añadir usuario a la lista de usuarios
        if bien:
            db_manager.db_manager().insert_user(username, password, email) # Insertar usuario en la base de datos

    def rent_movie(self, user_id, movie_id):
        """Alquilar una película"""
        return alquilerman.rent_movie(user_id, movie_id)
    
        
    

