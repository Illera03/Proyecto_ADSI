class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.status = "pendiente"
        if self.username == "_admin_":
            self.role = "admin"
        else:
            self.role = "user"
        self.idAdmin = None

    def __str__(self):
        return f"User: {self.name}, {self.age}"

    def user_with_name(self, username):
        return self.username == username

    def new_user(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        return True

    def its_me(self, username, password):
        return self.username == username and self.password == password

    def accepted_by_admin(self):
        return self.estado_peticion == "aceptada"

    def get_user_info(self):
        return {
            "name": self.name,
            "age": self.age,
            "username": self.username,
            "email": self.email,
            "estado_peticion": self.estado_peticion
        }

    def update_user_info(self, new_username, new_password, new_email):
        self.username = new_username
        self.password = new_password
        self.email = new_email
        return True

    def change_status(self):
        self.estado_peticion = "aceptada" if self.estado_peticion == "pendiente" else "pendiente"
        return True

    def pending_user(self):
        return self.estado_peticion == "pendiente"

    def get_username(self):
        return self.username