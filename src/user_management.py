# user_management.py
import sqlite3
from tkinter import messagebox
from db_manager import create_connection

class UserManager:
    def __init__(self, db_file):
        self.connection = create_connection(db_file)

    def register_user(self, username, password, email):
        """Registrar un nuevo usuario en la base de datos."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO Usuarios (username, password, email)
                VALUES (?, ?, ?)
            ''', (username, password, email))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def authenticate_user(self, username, password):
        """Autenticar un usuario existente."""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT * FROM Usuarios WHERE username = ? AND password = ?
        ''', (username, password))
        user = cursor.fetchone()
        return user is not None

    def close_connection(self):
        """Cerrar la conexión a la base de datos."""
        if self.connection:
            self.connection.close()

# Ejemplo de uso
if __name__ == "__main__":
    user_manager = UserManager("data/video_club.db")
    # Registra un nuevo usuario
    success = user_manager.register_user("nuevo_usuario", "contraseña", "email@example.com")
    if success:
        print("Usuario registrado exitosamente.")
    else:
        print("Error al registrar el usuario: usuario o correo ya existen.")
    
    # Autenticación de un usuario
    if user_manager.authenticate_user("nuevo_usuario", "contraseña"):
        print("Usuario autenticado.")
    else:
        print("Autenticación fallida.")
    
    user_manager.close_connection()
