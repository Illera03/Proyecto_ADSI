import sqlite3
from tkinter import messagebox
from CONTROLADOR.db_manager import create_connection

class RequestManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = create_connection(db_file)

    def create_movie_request(self, username, movie_title):
        """Insertar una nueva solicitud de película en la tabla Peticiones"""
        # Obtener el ID del usuario a partir del nombre de usuario
        cursor = self.connection.cursor()
        cursor.execute("SELECT user_id FROM Usuarios WHERE username = ?", (username,))
        user_id = cursor.fetchone()

        if user_id:
            cursor.execute("""
                INSERT INTO Peticiones (user_id, movie_title)
                VALUES (?, ?)
            """, (user_id[0], movie_title))
            self.connection.commit()
        else:
            messagebox.showerror("Error", "No se pudo encontrar el usuario en la base de datos.")
