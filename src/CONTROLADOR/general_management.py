# Description: General management class.
import CONTROLADOR.user_management as UserManager
import CONTROLADOR.db_manager as DbManager

class GeneralManager:
    _instance = None  # Variable de clase para la instancia única

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False  # Evitar múltiples inicializaciones
        return cls._instance

    def __init__(self):
        if not self.__initialized:  # Verificar si ya fue inicializado
            self.__initialized = True
            # Aquí podrías agregar más inicializaciones si fuera necesario

    def register_user(self, username, password, email):
        # Llamar a UserManager para agregar usuario
        user_manager = UserManager()
        bien = user_manager.add_user(username, password, email)
        if bien:
            # Si el usuario fue añadido correctamente, insertarlo en la base de datos
            db_manager_instance = DbManager("data/video_club.db")
            db_manager_instance.insert_user(username, password, email)

    
        
    

