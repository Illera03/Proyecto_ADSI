class User:
    def __init__(self, username, password, email):
        self.__username = username
        self.__password = password
        self.__email = email
        if self.__username == "_admin_":
            self.__role = "admin"
            self.__status = "aceptado"
        else:
            self.__role = "user"
            self.__status = "pendiente"
        self.__idAdmin = None
        self.__whoAccepted = []

    @staticmethod
    def new_user(username, password, email):
        # Crea y devuelve una nueva instancia de la clase User
        return User(username, password, email)
    
    @classmethod
    def new_user_from_bd(cls, username, password, email, status, role, idAdmin):
        """Crea y devuelve una nueva instancia de la clase User con todos los valores personalizados."""
        instance = cls(username, password, email)
        instance.__status = status
        instance.__role = role
        instance.__idAdmin = idAdmin
        return instance

    def user_with_name(self, username):
        return self.__username == username

    def its_me(self, username, password):
        return self.__username == username and self.__password == password

    def accepted_by_admin(self):
        return self.__status == "aceptado"
    
    def get_user_info(self):
        return {
            "username": self.__username,
            "email": self.__email
            }

    def get_all_user_info(self):
        return {
            "username": self.__username,
            "email": self.__email,
            "password": self.__password,
            "status": self.__status,
            "role": self.__role,
            "idAdmin": self.__idAdmin
        }

    def update_user_info(self, new_username, new_email, new_password = None):
        self.__username = new_username
        self.__email = new_email
        if new_password:
            self.__password = new_password
        return True

    def accept_user(self):
        self.__status = "aceptado"
        return True
    
    def reject_user(self):
        print("Usuario rechazado: " + self.__username)
        self.__status = "rechazado"
        return True

    def pending_user(self):
        return self.__status == "pendiente"

    def get_username(self):
        return self.__username
    
    def is_admin(self):
        return self.__role == "admin"
    
    def add_accepted_user(self, user):
        self.__whoAccepted.append(user)
        print("Usuarios aceptados por: " + self.__username)
        print([u.get_username() for u in self.__whoAccepted])