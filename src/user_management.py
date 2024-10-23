# user_management.py
import sqlite3
from db_manager import create_connection  # Asumiendo que existe en otro lugar

class UserManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = self.create_connection()  # Crear una conexión al inicializar

    def create_connection(self):
        """Crea una conexión a la base de datos SQLite"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
        return conn

    def register_user(self, username, password, email, role="user"):
        """Registrar un nuevo usuario en la base de datos."""
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO Usuarios (username, password, email, role) VALUES (?, ?, ?, ?)", 
                           (username, password, email, role))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def authenticate_user(self, username, password):
        """Autenticar un usuario en la base de datos."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT username, role FROM Usuarios WHERE username = ? AND password = ?", 
                       (username, password))
        user = cursor.fetchone()
        
        if user:
            return {"username": user[0], "role": user[1]}
        else:
            return None

    def get_user_info(self, username):
        """Obtener la información actual del usuario desde la base de datos"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT username, email FROM Usuarios WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user:
            return {'username': user[0], 'email': user[1]}
        return None

    def update_user_info(self, current_username, new_username, new_email, new_password=None):
        """Actualizar la información del usuario"""
        cursor = self.connection.cursor()
        if new_password:
            cursor.execute("UPDATE Usuarios SET username = ?, email = ?, password = ? WHERE username = ?",
                           (new_username, new_email, new_password, current_username))
        else:
            cursor.execute("UPDATE Usuarios SET username = ?, email = ? WHERE username = ?",
                           (new_username, new_email, current_username))
        self.connection.commit()
        return True

    def close_connection(self):
        """Cerrar la conexión a la base de datos."""
        if self.connection:
            self.connection.close()


# Ejemplo de uso
# if __name__ == "__main__":
#     user_manager = UserManager("data/video_club.db")
#     # Registra un nuevo usuario
#     success = user_manager.register_user("nuevo_usuario", "contraseña", "email@example.com")
#     if success:
#         print("Usuario registrado exitosamente.")
#     else:
#         print("Error al registrar el usuario: usuario o correo ya existen.")
    
#     # Autenticación de un usuario
#     if user_manager.authenticate_user("nuevo_usuario", "contraseña"):
#         print("Usuario autenticado.")
#     else:
#         print("Autenticación fallida.")
    
#     user_manager.close_connection()
