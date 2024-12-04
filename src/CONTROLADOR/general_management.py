# Description: General management class.
import user_management
class GeneralManager:
    def __init__(self):
        self.__general_manager = GeneralManager()
        
    @property
    def general_manager(self):
        return self.__general_manager
    
    def register_user(self, username, password, email):
        return user_management.user_manager().add_user(username, password, email)
        
    

