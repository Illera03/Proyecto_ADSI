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
            
    ###---------------- Métodos para la funcionalidad de GESTIÓN DE USUARIOS -- JORGE ILLERA RIVERA----------------###
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
    
    def update_user_info(self, new_username, new_email, new_password = None):
        user_manager = UserManager()
        resul = False
        if new_password:
            resul = user_manager.update_user_info(new_username, new_email, new_password)
        else:
            resul = user_manager.update_user_info(new_username, new_email)
        if resul != "error":
            print("Usuario actualizado correctamente.")
            db_manager_instance = DbManager()
            if new_password:
                if db_manager_instance.update_user(resul, new_username, new_email, new_password):
                    print("Usuario actualizado en la base de datos.")
                    return True
                else:
                    print("Error al actualizar usuario en la base de datos.")
                    return False
            else:
                if db_manager_instance.update_user(resul, new_username, new_email):
                    print("Usuario actualizado en la base de datos.")
                    return True
                else:
                    print("Error al actualizar usuario en la base de datos.")
                    return False
        else:
            print("Error al actualizar usuario.")
            return False
                
    ###         -------ADMIN-------         ###

    def admin_get_user_info(self, username):
        user_manager = UserManager()
        return user_manager.admin_get_user_info(username)
    
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
            
    def rent_movie(self, user_id, movie_id, rent_date):
                alquiler_manager = AlquilerManager()
                if alquiler_manager.rent_movie(user_id, movie_id, rent_date):
                    print("Película alquilada correctamente.")
                    db_manager_instance = DbManager()
                    if db_manager_instance.save_rental(user_id, movie_id):
                        print("Alquiler guardado en la base de datos.")
                        return True
                    else:
                        print("Error al guardar alquiler en la base de datos.")
                        return False
                else:
                    print("Error al alquilar película.")
                    return False
    
    def admin_update_user_info(self, old_username, new_username, new_email, new_password = None):
        user_manager = UserManager()
        resul = False
        if new_password:
            resul = user_manager.admin_update_user_info(old_username, new_username, new_email, new_password)
        else:
            resul = user_manager.admin_update_user_info(old_username, new_username, new_email)
        if resul:
            print("Usuario actualizado correctamente.")
            db_manager_instance = DbManager()
            if new_password:
                if db_manager_instance.update_user(old_username, new_username, new_email, new_password):
                    print("Usuario actualizado en la base de datos.")
                    return True
                else:
                    print("Error al actualizar usuario en la base de datos.")
                    return False
            else:
                if db_manager_instance.update_user(old_username, new_username, new_email):
                    print("Usuario actualizado en la base de datos.")
                    return True
                else:
                    print("Error al actualizar usuario en la base de datos.")
                    return False
    
    def get_pending_users(self):
        user_manager = UserManager()
        return user_manager.get_pending_users()
    
    def accept_user(self, username):
        user_manager = UserManager()
        admin_username = user_manager.accept_user(username)
        if admin_username != -1:
            print("Usuario aceptado correctamente.")
            db_manager_instance = DbManager()
            
            if db_manager_instance.save_admin(admin_username, username):
                print("Admin guardado como aceptador del usuario en la base de datos.")
                
                if db_manager_instance.accept_user(username):
                    print("Usuario aceptado en la base de datos.")
                    return True
                else:
                    print("Error al aceptar usuario en la base de datos.")
                    return False
            else:
                print("Error al guardar al admin como aceptador del usuario en la base de datos.")
                return False
            
            
    def reject_user(self, username):
        user_manager = UserManager()
        admin_username = user_manager.reject_user(username)
        if admin_username != -1:
            print("Usuario aceptado correctamente.")
            db_manager_instance = DbManager()
            if db_manager_instance.save_admin(admin_username, username):
                print("Admin guardado como rechazador del usuario en la base de datos.")
                
                if db_manager_instance.reject_user(username):
                    print("Usuario rechazado en la base de datos.")
                    return True
                else:
                    print("Error al rechazar usuario en la base de datos.")
                    return False
            else:
                print("Error al guardar al admin como rechazador del usuario en la base de datos.")
                return False
    ###-------------------------------------------------------------------------------------###
    def rent_movie(self, user_id, movie_id):
            """Alquilar una película"""
            return AlquilerManager.rent_movie(user_id, movie_id,fecha_alquiler=datetime.date.today())
    def view_rented_movies(self):
        return AlquilerManager.view_rented_movies()