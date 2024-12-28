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
            cls._instance.current_user = None  # Usuario actualmente logueado
        return cls._instance

    def add_user(self, username, password, email):
        """Añadir un nuevo usuario a la lista de usuarios."""
        for u in self.user_list:
            repetido = u.user_with_name(username)
            if repetido:
                print("Ya hay un usuario con ese nombre")
                return False 
        self.user_list.append(user.User.new_user(username, password, email))
        return True
    
    def add_user_from_bd(self, username, password, email, role, status): 
        """Añadir un nuevo usuario a la lista de usuarios."""
        for u in self.user_list:
            repetido = u.user_with_name(username)
            if repetido:
                print("Ya hay un usuario con ese nombre")
                return False 
        self.user_list.append(user.User.new_user_from_bd(username=username, password=password, email=email, status=status, role=role))

    def authenticate_user(self, username, password):
        """Autenticar un usuario en la base de datos."""
        
        # Código de respuestas:
        # 0: Usuario autenticado
        # 1: Usuario autenticado como administrador
        # 2: Usuario no encontrado o credenciales incorrectas
        # 3: Usuario pendiente de aprobación
        # 4: Usuario rechazado
        for u in self.user_list:
            if u.its_me(username, password):
                if u.accepted_by_admin():
                    self.current_user = username  # Actualizar el usuario logueado
                    if u.is_admin(): # Credenciales correctas y es admin
                        return 1
                    else: return 0 # Credenciales correctas y es user
                elif u.pending_user():
                    return 3 # Usuario pendiente de aprobación
                else:
                    return 4 # Usuario rechazado
        return 2 # Usuario no encontrado o credenciales incorrectas
            

    def get_all_users(self):
        """Obtener lista de nombres de usuario"""
        return [u.get_username() for u in self.user_list]

    def delete_user(self, username):
        """Eliminar un usuario de la lista"""
        if username == self.current_user:
            return False  # No se puede eliminar a si mismo.
        for u in self.user_list:
            if u.user_with_name(username):
                self.user_list.remove(u)
                return True
        return False

    def get_user_info(self):
        """Obtener información del usuario actual"""
        for u in self.user_list:
            if u.user_with_name(self.current_user):
                return u.get_user_info()
        return None
    
    def admin_get_user_info(self, username):
        """Obtener información de un usuario específico"""
        for u in self.user_list:
            if u.user_with_name(username):
                return u.get_all_user_info()
        return None
    
    def update_user_info(self, new_username, new_email, new_password=None):
        """Actualizar la información del usuario actual"""

        # Verificar si el nuevo nombre de usuario ya está en uso
        if new_username != self.current_user:
            for u in self.user_list:
                if u.user_with_name(new_username):
                    return "error"  # Nombre de usuario ya en uso

        # Buscar al usuario actual
        user = next((u for u in self.user_list if u.user_with_name(self.current_user)), None)
        if not user:
            return "error"  # Usuario actual no encontrado

        # Actualizar la información del usuario
        user.update_user_info(new_username, new_email, new_password)
        old_username = self.current_user
        self.current_user = new_username  # Actualizar el nombre de usuario actual
        print(new_username)
        return old_username
    
    def admin_update_user_info(self, old_username, new_username, new_email, new_password=None):
        """Actualizar la información del usuario actual"""

        # Verificar si el nuevo nombre de usuario ya está en uso
        if new_username != old_username:
            for u in self.user_list:
                if u.user_with_name(new_username):
                    return "error"  # Nombre de usuario ya en uso

        # Buscar al usuario actual
        user = next((u for u in self.user_list if u.user_with_name(old_username)), None)
        if not user:
            return "error"  # Usuario actual no encontrado

        # Actualizar la información del usuario
        user.update_user_info(new_username, new_email, new_password)
        print(new_username)
        return True

    def get_pending_users(self):
        """Obtener lista de usuarios pendientes de aprobación"""
        return [u.get_username() for u in self.user_list if u.pending_user()]
    
    def accept_user(self, username):
        """Aceptar un usuario pendiente de aprobación"""
        for u in self.user_list:
            if u.user_with_name(username):
                u.accept_user()
                for admin in self.user_list:
                    if admin.user_with_name(self.current_user): # Buscar al admin actual (que es el usuario logueado)
                        admin.add_accepted_user(u) # Agregar al usuario aceptado a la lista de usuarios aceptados por el admin
                        return self.current_user
        return -1  # Usuario no encontrado
    
    def reject_user(self, username):
        """Rechazar un usuario pendiente de aprobación"""
        for u in self.user_list:
            if u.user_with_name(username):
                u.reject_user()
                return self.current_user
        return -1
    
    def print_users(self):
        """Imprimir la lista de usuarios."""
        print("\nDatos cargados de la base de datos:\n")
        print("---------------------------------------------------------------------------------------------------------------------------------")
        for user in self.user_list:
            print(user.get_all_user_info())
            print("---------------------------------------------------------------------------------------------------------------------------------")
    
    #Métodos para pruebas
    
    def exists_user(self, username):
        """Verificar si un usuario existe en la lista"""
        for u in self.user_list:
            if u.user_with_name(username):
                return True
        return False    
    
    def empty_user_list(self):
        """Vaciar la lista de usuarios"""
        self.user_list = []
    def change_current_user(self, username):
        """Cambiar el usuario actual"""
        self.current_user = username
    
    def get_user(self, username):
        """Obtener un usuario específico"""
        for u in self.user_list:
            if u.user_with_name(username):
                return u.get_all_user_info()
        return None        
            
    #! ---------------------------------------------------------------------------------------------------------------------------------------------------------        
    #! Esto está mal
    def get_user_id(self, username):
        """Obtiene el user_id a partir del nombre de usuario."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT user_id FROM Usuarios WHERE username = ?", (username,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    
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
    
    ###! ----------------------------------------------------------------------------
        
    # ! Esto también está mal
    def close_connection(self):
        """Cerrar la conexión a la base de datos."""
        if self.connection:
            self.connection.close()
    
