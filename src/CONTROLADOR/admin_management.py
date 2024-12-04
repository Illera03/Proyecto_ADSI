# admin_management.py
import sqlite3
from db_manager import create_connection

class AdminManager:
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
    
    def get_pending_users(self):
        """Obtener una lista de usuarios pendientes de aceptación."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT username, email FROM Usuarios WHERE status = 'pendiente'")
        return cursor.fetchall()

    def accept_user(self, username):
        """Aceptar la solicitud de registro de un usuario."""
        cursor = self.connection.cursor()
        cursor.execute("UPDATE Usuarios SET status = 'aceptado' WHERE username = ?", (username,))
        self.connection.commit()

    def reject_user(self, username):
        """Rechazar la solicitud de registro de un usuario."""
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM Usuarios WHERE username = ?", (username,))
        self.connection.commit()
        
    def delete_user(self, username):
        """Eliminar un usuario de la base de datos"""
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM Usuarios WHERE username = ?", (username,))
        self.connection.commit()
        
    def get_all_users(self):
        """Obtener todos los usuarios de la base de datos"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT username, email FROM Usuarios")
        return cursor.fetchall() 