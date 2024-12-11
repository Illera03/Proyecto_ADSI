class User:
    def __init__(self, username, password, email):
        self.__username = username
        self.__password = password
        self.__email = email
        self.__status = "pendiente"
        if self.__username == "_admin_":
            self.__role = "admin"
        else:
            self.__role = "user"
        self.__idAdmin = None

    @staticmethod
    def new_user(username, password, email):
        # Crea y devuelve una nueva instancia de la clase User
        return User(username, password, email)

    def user_with_name(self, username):
        return self.__username == username

    def its_me(self, username, password):
        return self.__username == username and self.__password == password

    def accepted_by_admin(self):
        return self.__status == "aceptada"

    def get_user_info(self):
        return {
            "username": self.__username,
            "email": self.__email,
            "password": self.__password
        }

    def update_user_info(self, new_username, new_password, new_email):
        self.__username = new_username
        self.__password = new_password
        self.__email = new_email
        return True

    def change_status(self):
        self.__status = "aceptada" if self.__status == "pendiente" else "pendiente"
        return True

    def pending_user(self):
        return self.__status == "pendiente"

    def get_username(self):
        return self.__username
