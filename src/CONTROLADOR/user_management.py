# user_management.py
#import sqlite3
#from CONTROLADOR.db_manager import create_connection  # Asumiendo que existe en otro lugar
import json
import requests
import tkinter as tk
from tkinter import messagebox
import MODELO.user as user


class UserManager:
    _instance = None  # Variable de clase para guardar la instancia única

    def __new__(cls, db_file=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.user_list = []  # Lista de usuarios
        return cls._instance

    def add_user(self, username, password, email): #TODO ESTÁ BIEN?
        """Añadir un nuevo usuario a la lista de usuarios."""
        for u in self.user_list:
            repetido = u.user_with_name(username)
            if repetido:
                print("Ya hay un usuario con ese nombre")
                return False 
        self.user_list.append(user.User.new_user(username, password, email))
        return True
    
    def add_user_from_bd(self, username, password, email, role, status, idAdmin): #TODO ESTÁ BIEN?
        """Añadir un nuevo usuario a la lista de usuarios."""
        for u in self.user_list:
            repetido = u.user_with_name(username)
            if repetido:
                print("Ya hay un usuario con ese nombre")
                return False 
        self.user_list.append(user.User.new_user_from_bd(username=username, password=password, email=email, status=status, role=role, idAdmin=idAdmin))

    def authenticate_user(self, username, password):
        """Autenticar un usuario en la base de datos."""
        
        # Código de respuestas:
        # 0: Usuario autenticado
        # 1: Usuario autenticado como administrador
        # 2: Usuario no encontrado o credenciales incorrectas
        # 3: Usuario pendiente de aprobación
        for u in self.user_list:
            if u.its_me(username, password):
                if u.accepted_by_admin():
                    if u.is_admin(): # Credenciales correctas y es admin
                        return 1
                    else: return 0 # Credenciales correctas y es user
                else: return 3 # Usuario pendiente de aprobación
        return 2 # Usuario no encontrado o credenciales incorrectas
            

    def get_all_users(self):
        """Obtener lista de nombres de usuario"""
        return [u.get_username() for u in self.user_list]

    def delete_user(self, username):
        """Eliminar un usuario de la lista"""
        for u in self.user_list:
            if u.user_with_name(username):
                self.user_list.remove(u)
                return True
        return False

    #! Esto está mal
    def get_user_info(self, username):
        """Obtener la información actual del usuario desde la base de datos"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT username, email FROM Usuarios WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user:
            return {'username': user[0], 'email': user[1]}
        return None
    
    #! Esto está mal
    def get_user_id(self, username):
        """Obtiene el user_id a partir del nombre de usuario."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT user_id FROM Usuarios WHERE username = ?", (username,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    #! Esto está mal
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
    
    ###! ???? ESTO NO VA AQUÍ, VA EN OTRA CLASE--------------------------------------
    def create_movie_request(self, username, movie_title):
        """Crea una solicitud de película en la base de datos."""
        cursor = self.connection.cursor()

        user_id = self.get_user_id(username)

        cursor.execute("""
            INSERT INTO Peticiones (user_id, movie_title)
            VALUES (?, ?)
        """, (user_id, movie_title))

        self.connection.commit()
    
    def search_movie_omdb(self, movie_title):
        """Buscar la película en la API de OMDb"""
        url = f"http://www.omdbapi.com/?t={movie_title}&apikey=2d79f0e"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data['Response'] == 'True':
                return data  # Devolvemos los datos de la película
            else:
                return None  # No se encontró la película
        else:
            messagebox.showerror("Error", "No se pudo conectar con OMDb API.")
            return None
    ###! ----------------------------------------------------------------------------
        

    def close_connection(self):
        """Cerrar la conexión a la base de datos."""
        if self.connection:
            self.connection.close()
    
    def print_users(self):
        """Imprimir la lista de usuarios."""
        print("\nDatos cargados de la base de datos:\n")
        print("---------------------------------------------------------------------------------------------------------------------------------")
        for user in self.user_list:
            print(user.get_user_info())
            print("---------------------------------------------------------------------------------------------------------------------------------")




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
